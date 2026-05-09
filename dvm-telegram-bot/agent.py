"""
agent.py — LLM orchestration using Groq (free, fast Llama 3.3 70B).
Groq's API is OpenAI-compatible and supports tool/function calling.
Free tier: 14,400 requests/day, 30 RPM.
"""

import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

MODEL = "llama3-groq-70b-8192-tool-use-preview"  # Fine-tuned specifically for OpenAI-compatible tool use

# ---------------------------------------------------------------------------
# System Prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are the DVM School ERP Assistant — a helpful, accurate, and concise school data assistant.

You help school staff quickly look up:
- Student information (name, class, section, guardian contacts)
- Attendance records
- Staff directory
- School statistics

Rules:
- Always respond in the same language the user used (Hindi or English).
- Be concise. Avoid unnecessary filler sentences.
- If a student search returns multiple results, list them briefly and ask which one the user means.
- Never reveal sensitive financial data (bank accounts, Aadhaar, PAN).
- If you cannot find the information, say so clearly and suggest how to refine the search.
- Use emoji sparingly but effectively (📞 for phone, 🎓 for students, 👨‍🏫 for staff).
- For attendance, always mention the percentage prominently."""

# ---------------------------------------------------------------------------
# Tool definitions (OpenAI function calling format)
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_school_stats",
            "description": (
                "Get overall school statistics: total students, total staff, "
                "class-wise breakdown, gender distribution, and current academic year. "
                "Call this for questions like: how many students, class strength, school overview."
            ),
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_students",
            "description": (
                "Search for students by name or admission number. "
                "Optionally filter by class_name (e.g. 'Class 5'), section (e.g. 'A'), "
                "or status (active/promoted/left/detained)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Student name or admission number"},
                    "class_name": {"type": "string", "description": "Class name e.g. 'Class 5'"},
                    "section": {"type": "string", "description": "Section e.g. 'A'"},
                    "status": {"type": "string", "description": "active / promoted / left / detained"},
                    "limit": {"type": "integer", "description": "Max results (default 10)"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_student_detail",
            "description": "Get complete details for a student by their database ID, including guardians and profile.",
            "parameters": {
                "type": "object",
                "properties": {
                    "student_id": {"type": "integer", "description": "Student's numeric database ID"},
                },
                "required": ["student_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_student_attendance",
            "description": (
                "Get attendance summary for a specific student. "
                "Provide either admission_no (preferred) or student_id."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "admission_no": {"type": "string", "description": "Student's admission number"},
                    "student_id": {"type": "integer", "description": "Student's database ID"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_staff",
            "description": "Search for staff members by name, email, or department.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Staff name or keyword"},
                    "department": {"type": "string", "description": "Department filter e.g. 'Science'"},
                    "limit": {"type": "integer", "description": "Max results (default 10)"},
                },
                "required": [],
            },
        },
    },
]

# ---------------------------------------------------------------------------
# Import tool executor functions
# ---------------------------------------------------------------------------
from tools import TOOL_FUNCTIONS


# ---------------------------------------------------------------------------
# Main agent function
# ---------------------------------------------------------------------------

def ask(user_message: str) -> str:
    """
    Send a user message through the Groq LLM with tool calling loop.
    Returns the final natural-language answer as a string.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    max_iterations = 5
    for _ in range(max_iterations):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            parallel_tool_calls=False,  # Prevents malformed multi-call generation
            max_tokens=1024,
        )

        msg = response.choices[0].message
        messages.append(msg)  # add assistant turn to history

        # No tool calls — return the text response
        if not msg.tool_calls:
            return msg.content.strip() if msg.content else "No response generated."

        # Execute each tool call
        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            try:
                fn_args = json.loads(tool_call.function.arguments or "{}")
            except json.JSONDecodeError:
                fn_args = {}

            if fn_name in TOOL_FUNCTIONS:
                result = TOOL_FUNCTIONS[fn_name](**fn_args)
            else:
                result = {"error": f"Unknown tool: {fn_name}"}

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, default=str),
            })

    return "Sorry, I wasn't able to complete the request. Please try rephrasing."
