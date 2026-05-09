"""
agent.py — Gemini LLM orchestration using the newer google-genai SDK (v1 API).
Uses gemini-2.0-flash with automatic function calling.
"""

import json
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", ""))

# ---------------------------------------------------------------------------
# System Prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are the DVM School ERP Assistant — a helpful, accurate, and concise school data assistant.

You help school staff quickly look up:
- Student information (name, class, section, guardian contacts)
- Attendance records
- Staff directory
- School statistics

Rules:
- Always respond in the same language the user used (Hindi or English).
- Be concise. Avoid unnecessary filler sentences.
- If a student search returns multiple results, list them briefly and ask which one.
- Never reveal sensitive financial data (bank accounts, Aadhaar, PAN).
- If you cannot find the information, say so clearly and suggest how to refine the search.
- Format phone numbers clearly. Use emoji sparingly but effectively (📞 for phone, 🎓 for students, 👨‍🏫 for staff).
- For attendance, always mention the percentage prominently.
""".strip()

# ---------------------------------------------------------------------------
# Import tool functions
# ---------------------------------------------------------------------------
from tools import (
    get_school_stats,
    search_students,
    get_student_detail,
    get_student_attendance,
    search_staff,
    TOOL_FUNCTIONS,
)

# ---------------------------------------------------------------------------
# Tool declarations for Gemini
# ---------------------------------------------------------------------------
TOOLS = [
    types.Tool(function_declarations=[
        types.FunctionDeclaration(
            name="get_school_stats",
            description=(
                "Get overall school statistics: total students, total staff, "
                "class-wise breakdown, gender distribution, and current academic year."
            ),
        ),
        types.FunctionDeclaration(
            name="search_students",
            description=(
                "Search for students by name or admission number. "
                "Filter by class_name (e.g. 'Class 5'), section (e.g. 'A'), "
                "or status (active/promoted/left/detained)."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "query": types.Schema(type="STRING", description="Student name or admission number"),
                    "class_name": types.Schema(type="STRING", description="e.g. 'Class 5'"),
                    "section": types.Schema(type="STRING", description="e.g. 'A'"),
                    "status": types.Schema(type="STRING", description="active / promoted / left / detained"),
                    "limit": types.Schema(type="INTEGER", description="Max results (default 10)"),
                },
            ),
        ),
        types.FunctionDeclaration(
            name="get_student_detail",
            description="Get complete details for a student by database ID, including guardians and profile.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "student_id": types.Schema(type="INTEGER", description="Student's numeric database ID"),
                },
                required=["student_id"],
            ),
        ),
        types.FunctionDeclaration(
            name="get_student_attendance",
            description="Get attendance summary for a student. Provide admission_no or student_id.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "admission_no": types.Schema(type="STRING", description="Student's admission number (preferred)"),
                    "student_id": types.Schema(type="INTEGER", description="Student's database ID"),
                },
            ),
        ),
        types.FunctionDeclaration(
            name="search_staff",
            description="Search for staff members by name, email, or department.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "query": types.Schema(type="STRING", description="Staff name or keyword"),
                    "department": types.Schema(type="STRING", description="Department filter e.g. 'Science'"),
                    "limit": types.Schema(type="INTEGER", description="Max results (default 10)"),
                },
            ),
        ),
    ])
]

CONFIG = types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT,
    tools=TOOLS,
)

# ---------------------------------------------------------------------------
# Main agent function
# ---------------------------------------------------------------------------

def ask(user_message: str) -> str:
    """
    Send a user message through the Gemini agent loop with function calling.
    Returns the final natural-language answer as a string.
    """
    contents = [types.Content(role="user", parts=[types.Part(text=user_message)])]

    max_iterations = 5
    for _ in range(max_iterations):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=CONFIG,
        )

        candidate = response.candidates[0]
        contents.append(candidate.content)  # add assistant turn to history

        # Collect function calls from all parts
        fn_calls = [
            part.function_call
            for part in candidate.content.parts
            if part.function_call is not None
        ]

        if not fn_calls:
            # No tool calls — return final text
            try:
                return response.text.strip()
            except Exception:
                return "Sorry, I couldn't generate a response. Please try again."

        # Execute each function call and collect results
        fn_result_parts = []
        for fn_call in fn_calls:
            fn_name = fn_call.name
            fn_args = dict(fn_call.args) if fn_call.args else {}

            if fn_name in TOOL_FUNCTIONS:
                result = TOOL_FUNCTIONS[fn_name](**fn_args)
            else:
                result = {"error": f"Unknown tool: {fn_name}"}

            fn_result_parts.append(
                types.Part(
                    function_response=types.FunctionResponse(
                        name=fn_name,
                        response={"result": json.dumps(result, default=str)},
                    )
                )
            )

        # Add tool results as a user turn
        contents.append(types.Content(role="user", parts=fn_result_parts))

    return "Sorry, I wasn't able to complete the request. Please try rephrasing."
