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

MODEL = "llama-3.3-70b-versatile"  # Current Groq production model with tool calling

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
1. **GROUNDING IS CRITICAL**: Only use information provided by the tools. NEVER invent names, admission numbers, attendance percentages, or any other data.
2. **MISSING DATA**: If a tool returns no results (e.g., an empty list or 'count: 0'), say clearly: "I couldn't find any student/staff matching that description in our records." Do NOT suggest they might exist under a different name unless you have tool output to support it.
3. **ERROR HANDLING**: If a tool returns an error (e.g., 'API error 404' or 'Connection error'), explain it in simple human language:
   - 404: "I couldn't find that record in the database."
   - 500: "There seems to be a technical issue with the school server. Please try again in a few minutes."
   - Other: "I'm having trouble reaching the school database right now."
4. **LANGUAGE**: Always respond in the same language the user used (Hindi or English).
5. **CONCISENESS**: Be concise. Avoid unnecessary filler sentences.
6. **MULTIPLE RESULTS**: If a student search returns multiple results, list them briefly and ask which one the user means.
7. **PRIVACY**: Never reveal sensitive financial data (bank accounts, Aadhaar, PAN).
8. **ATTENDANCE**: For attendance, always mention the percentage prominently. Use 📊 emoji.
9. **EMOJIS**: Use emoji sparingly but effectively (📞 for phone, 🎓 for students, 👨‍🏫 for staff).
10. **STRICTNESS**: If you are unsure or the data is not present in the tool output, admit you don't know."""

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
                    "limit": {"type": "integer", "description": "Max results (default 50)"},
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
                    "limit": {"type": "integer", "description": "Max results (default 50)"},
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

def ask(
    user_message: str,
    role: str = "staff",
    authorized_student_ids: list = None,
    authorized_student_names: list = None,
    user_name: str = "User",
) -> str:
    """
    Send a user message through the Groq LLM with tool calling loop.
    Role controls what data the agent is allowed to surface:
      - staff    → unrestricted
      - guardian → only authorized_student_ids
      - unknown  → no personal data
    """
    # Build role-specific system prompt suffix
    if role == "guardian" and authorized_student_ids:
        names = ", ".join(authorized_student_names or [str(i) for i in authorized_student_ids])
        role_context = (
            f"\n\nIMPORTANT: This user ({user_name}) is a parent/guardian. "
            f"You MUST only show information for these specific students: {names} "
            f"(database IDs: {authorized_student_ids}). "
            "If they ask about any other student, politely decline. "
            "When they say 'my child' or 'mere bache', they mean one of these students."
        )
    elif role == "unknown":
        role_context = (
            f"\n\nIMPORTANT: This user ({user_name}) is not verified in the school records. "
            "You may only answer general questions about school statistics (total students, classes). "
            "Do NOT search for or reveal any individual student or staff information. "
            "If they ask for personal data, politely explain they need to be registered."
        )
    else:
        role_context = f"\n\nThis user ({user_name}) is a verified school staff member with full access."

    system = SYSTEM_PROMPT + role_context

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]

    try:
        return _run_loop(messages, role=role, authorized_ids=authorized_student_ids or [])
    except Exception as e:
        if "tool_use_failed" in str(e) or "tool_call" in str(e).lower():
            try:
                fallback = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    max_tokens=512,
                )
                return fallback.choices[0].message.content.strip()
            except Exception:
                pass
        raise


def _run_loop(messages: list, role: str = "staff", authorized_ids: list = None) -> str:
    authorized_ids = authorized_ids or []
    max_iterations = 5
    for _ in range(max_iterations):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            parallel_tool_calls=False,
            max_tokens=1024,
        )

        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            return msg.content.strip() if msg.content else "No response generated."

        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            try:
                fn_args = json.loads(tool_call.function.arguments or "{}")
            except json.JSONDecodeError:
                fn_args = {}

            # Guardian access control — block student lookups for non-authorized IDs
            if role == "guardian" and authorized_ids:
                if fn_name == "get_student_detail":
                    sid = fn_args.get("student_id")
                    if sid and int(sid) not in authorized_ids:
                        result = {"error": "Access denied. You can only view your own child's data."}
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result),
                        })
                        continue
                elif fn_name == "get_student_attendance":
                    sid = fn_args.get("student_id")
                    if sid and int(sid) not in authorized_ids:
                        result = {"error": "Access denied. You can only view your own child's attendance."}
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result),
                        })
                        continue

            # Unknown role — block all personal data tools
            if role == "unknown" and fn_name in (
                "search_students", "get_student_detail", "get_student_attendance", "search_staff"
            ):
                result = {"error": "Access denied. Please verify your identity first."}
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                })
                continue

            if fn_name in TOOL_FUNCTIONS:
                result = TOOL_FUNCTIONS[fn_name](**fn_args)

                # For guardians: filter search_students results to only authorized IDs
                if role == "guardian" and authorized_ids and fn_name == "search_students":
                    if "results" in result:
                        result["results"] = [r for r in result["results"] if r["id"] in authorized_ids]
                        result["count"] = len(result["results"])
            else:
                result = {"error": f"Unknown tool: {fn_name}"}

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, default=str),
            })

    return "Sorry, I wasn't able to complete the request. Please try rephrasing."
