"""
agent.py — Gemini LLM orchestration layer with function calling.
Takes a plain-text user message, calls the right /api/agent/* tools,
and returns a natural-language answer.
"""

import json
import os
import google.generativeai as genai
from tools import TOOL_FUNCTIONS

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

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
- Never reveal sensitive financial data (bank accounts, Aadhaar, PAN) — this data is not in your tools anyway.
- If you cannot find the information, say so clearly and suggest how to refine the search.
- Format phone numbers clearly. Use emoji sparingly but effectively (📞 for phone, 🎓 for students, 👨‍🏫 for staff).
- For attendance, always mention the percentage prominently.
""".strip()

# ---------------------------------------------------------------------------
# Tool schema definitions for Gemini
# ---------------------------------------------------------------------------
TOOL_DECLARATIONS = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="get_school_stats",
            description=(
                "Get overall school statistics: total students, total staff, "
                "class-wise breakdown, gender distribution, and current academic year."
            ),
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={},
            ),
        ),
        genai.protos.FunctionDeclaration(
            name="search_students",
            description=(
                "Search for students by name or admission number. "
                "Filter by class_name (e.g. 'Class 5'), section (e.g. 'A'), "
                "or status (active/promoted/left/detained)."
            ),
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "query": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Student name or admission number to search for",
                    ),
                    "class_name": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Class name filter e.g. 'Class 5' or 'Class 8'",
                    ),
                    "section": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Section filter e.g. 'A', 'B'",
                    ),
                    "status": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Status filter: active, promoted, left, or detained",
                    ),
                    "limit": genai.protos.Schema(
                        type=genai.protos.Type.INTEGER,
                        description="Max number of results (default 10)",
                    ),
                },
            ),
        ),
        genai.protos.FunctionDeclaration(
            name="get_student_detail",
            description=(
                "Get complete details for a student by their database ID, "
                "including guardians, health info, and transport details."
            ),
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "student_id": genai.protos.Schema(
                        type=genai.protos.Type.INTEGER,
                        description="The student's numeric database ID",
                    ),
                },
                required=["student_id"],
            ),
        ),
        genai.protos.FunctionDeclaration(
            name="get_student_attendance",
            description=(
                "Get attendance summary for a specific student. "
                "Returns total days, present, absent, late, and attendance percentage."
            ),
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "admission_no": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Student's admission number (preferred)",
                    ),
                    "student_id": genai.protos.Schema(
                        type=genai.protos.Type.INTEGER,
                        description="Student's database ID (alternative to admission_no)",
                    ),
                },
            ),
        ),
        genai.protos.FunctionDeclaration(
            name="search_staff",
            description=(
                "Search for staff members by name, email, or department. "
                "Returns designation, department, and email."
            ),
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "query": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Staff name or keyword to search for",
                    ),
                    "department": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Department to filter by e.g. 'Science', 'Maths'",
                    ),
                    "limit": genai.protos.Schema(
                        type=genai.protos.Type.INTEGER,
                        description="Max number of results (default 10)",
                    ),
                },
            ),
        ),
    ]
)

# ---------------------------------------------------------------------------
# Main agent function
# ---------------------------------------------------------------------------

def ask(user_message: str) -> str:
    """
    Send a user message through the Gemini agent loop.
    Returns the final natural-language answer as a string.
    """
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT,
        tools=[TOOL_DECLARATIONS],
    )

    chat = model.start_chat(enable_automatic_function_calling=False)

    # First turn — user message
    response = chat.send_message(user_message)

    # Agentic loop — keep calling tools until Gemini gives a final text response
    max_iterations = 5
    for _ in range(max_iterations):
        # Check if response has function calls
        fn_calls = []
        for part in response.candidates[0].content.parts:
            if hasattr(part, "function_call") and part.function_call.name:
                fn_calls.append(part.function_call)

        if not fn_calls:
            # No more tool calls — extract final text
            break

        # Execute each function call and collect results
        fn_results = []
        for fn_call in fn_calls:
            fn_name = fn_call.name
            fn_args = dict(fn_call.args) if fn_call.args else {}

            if fn_name in TOOL_FUNCTIONS:
                result = TOOL_FUNCTIONS[fn_name](**fn_args)
            else:
                result = {"error": f"Unknown tool: {fn_name}"}

            fn_results.append(
                genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name=fn_name,
                        response={"result": json.dumps(result, default=str)},
                    )
                )
            )

        # Send tool results back to Gemini
        response = chat.send_message(fn_results)

    # Extract final text answer
    try:
        return response.text.strip()
    except Exception:
        return "Sorry, I couldn't generate a response. Please try again."
