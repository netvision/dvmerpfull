"""
tools.py — Thin wrappers around /api/agent/* endpoints.
Each function is registered as a Gemini tool so the LLM can call them autonomously.
"""

import os
import requests

AGENT_BASE_URL = os.getenv("AGENT_BASE_URL", "http://localhost:8000/api/agent")
AGENT_API_KEY = os.getenv("AGENT_API_KEY", "")


def _get(path: str, params: dict = None) -> dict:
    """Make an authenticated GET request to the agent API."""
    try:
        resp = requests.get(
            f"{AGENT_BASE_URL}{path}",
            params=params or {},
            headers={"X-API-Key": AGENT_API_KEY},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        try:
            error_detail = e.response.json()
            if isinstance(error_detail, dict) and "detail" in error_detail:
                return {"error": f"API error {e.response.status_code}: {error_detail['detail']}"}
        except Exception:
            pass
        return {"error": f"API error {e.response.status_code}: {e.response.text[:200]}"}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}


# ---------------------------------------------------------------------------
# Tool functions — called by the LLM via function calling
# ---------------------------------------------------------------------------

def get_school_stats() -> dict:
    """
    Get overall school statistics: total students, staff count,
    class-wise student breakdown, gender distribution, and current academic year.
    Call this for questions like:
    - "How many students are there?"
    - "What is the strength of Class 5?"
    - "How many male vs female students?"
    - "Give me school overview"
    """
    return _get("/stats")


def search_students(
    query: str = None,
    class_name: str = None,
    section: str = None,
    status: str = None,
    limit: int = 50,
) -> dict:
    """
    Search for students by name or admission number.
    Optionally filter by class name (e.g. "Class 5"), section (e.g. "A"), or status.
    Call this when the user asks about a student by name or wants to find students in a class.
    status can be: active, promoted, left, detained
    """
    params = {"limit": limit}
    if query:      params["q"] = query
    if class_name: params["class_name"] = class_name
    if section:    params["section"] = section
    if status:     params["status"] = status
    return _get("/students", params)


def get_student_detail(student_id: int) -> dict:
    """
    Get complete details for a student by their database ID.
    Includes personal info, guardians, profile data (health, transport).
    Call this after finding a student via search_students to get full details.
    """
    return _get(f"/students/{student_id}")


def get_student_attendance(
    admission_no: str = None,
    student_id: int = None,
) -> dict:
    """
    Get attendance summary for a specific student.
    Provide either the admission_no (preferred) or student_id.
    Returns: total days, present count, absent count, attendance percentage.
    Call this for questions like:
    - "What is Arjun's attendance?"
    - "How many days was student 2024/101 absent?"
    """
    params = {}
    if admission_no: params["admission_no"] = admission_no
    if student_id:   params["student_id"] = student_id
    return _get("/attendance", params)


def search_staff(
    query: str = None,
    department: str = None,
    limit: int = 50,
) -> dict:
    """
    Search for staff members by name, email, or department.
    Call this for questions like:
    - "Who is the Maths teacher?"
    - "Find staff in Science department"
    - "Contact details for Priya ma'am"
    """
    params = {"limit": limit}
    if query:      params["q"] = query
    if department: params["department"] = department
    return _get("/staff", params)


# ---------------------------------------------------------------------------
# Registry — used by agent.py to build Gemini tool declarations
# ---------------------------------------------------------------------------

TOOL_FUNCTIONS = {
    "get_school_stats": get_school_stats,
    "search_students": search_students,
    "get_student_detail": get_student_detail,
    "get_student_attendance": get_student_attendance,
    "search_staff": search_staff,
}
