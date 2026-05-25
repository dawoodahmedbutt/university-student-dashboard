import os
from typing import List, Dict, Optional, Any
import streamlit as st

import pandas as pd
import requests


# Configuration: set this env var or edit the value below to point to your backend
BASE_URL = os.environ.get("DASHBOARD_API_BASE_URL", "http://127.0.0.1:8000")

# Map logical operations to backend endpoint paths. You can edit these to match
# your real backend routes. Use `{course_id}`, `{id}` or `{student_id}` placeholders
# where appropriate; they will be formatted automatically.
ENDPOINTS = {
    "courses": "/director/coursesdropdown",
    "modules_for_course": "/director/moduledropdown/{course_id}",
    "list_students": "/students/getall",
    "create_student": "/CRUD/student/create",
    "update_student": "/CRUD/student/update/{id}",
    "delete_student_crud": "/CRUD/student/delete/{student_id}",
    "list_courses": "/CRUD/course/getall",
    "create_course": "/CRUD/course/create",
    "update_course": "/CRUD/course/update/{id}",
    "delete_course": "/CRUD/course/delete/{id}",
    "list_modules": "/CRUD/module/getall/{course_id}",
    "create_module": "/CRUD/module/create/{course_id}",
    "update_module": "/CRUD/module/update/{id}",
    "delete_module": "/CRUD/module/delete/{id}",
    "director_summary": "/director/summary/{course_id}",
    "director_averages": "/director/Averages",
    "course_comparison": "/director/course_comparison",
    "module_comparison": "/director/module_comparison/{course_id}",
    "attendance_vs_performance": "/director/barplot/{course_id}",
    "grade_distribution": "/director/gradedistribution/{course_id}/{module_id}",
    "student_risk": "/director/Studentrisk/{course_id}/{module_id}",
    "wellbeing_overview": "/wellbeing/overview",
    "wellbeing_getall": "/wellbeing/getall",
    "wellbeing_create": "/wellbeing/create",
    "stress_avg_plot": "/wellbeing/stress_avg_plot",
    "priority_actions": "/wellbeing/priority_actions",
    "wellbeing_trends": "/wellbeing/trends/{student_id}",
    "burnout_scatter": "/wellbeing/burnout_scatter",
    "sessions_for_module": "/explorer/sessions/{course_id}/{module_id}",
}

# Short timeout for HTTP requests to keep UI responsive when backend is slow
TIMEOUT = int(os.environ.get("DASHBOARD_API_TIMEOUT", "2"))


def _build_url(path: str) -> str:
    return BASE_URL + path


def _fetch_json(path: str, params: Optional[Dict[str, Any]] = None, timeout: int = TIMEOUT) -> Optional[Any]:
    """GET JSON from the backend. Returns parsed JSON on success, None on failure.

    This helper prints errors and returns None so callers can decide how to handle
    backend unavailability.
    """
    url = _build_url(path)
    if not url:
        print("[dashboard_api] BASE_URL is not set. Set DASHBOARD_API_BASE_URL environment variable.")
        return None

    try:
        r = requests.get(url, params=params or {}, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[dashboard_api] GET {url} failed: {e}")
        return None


def _request_json(method: str, path: str, json_payload: Optional[Dict] = None, timeout: int = TIMEOUT) -> Optional[Any]:
    url = _build_url(path)
    if not url:
        print("[dashboard_api] BASE_URL is not set. Set DASHBOARD_API_BASE_URL environment variable.")
        return None

    try:
        if method.upper() == "POST":
            r = requests.post(url, json=json_payload or {}, timeout=timeout)
        elif method.upper() == "PUT":
            r = requests.put(url, json=json_payload or {}, timeout=timeout)
        elif method.upper() == "DELETE":
            r = requests.delete(url, timeout=timeout)
        else:
            raise ValueError("Unsupported method")

        r.raise_for_status()
        if r.status_code == 204 or not r.content:
            return {}
        return r.json()
    except Exception as e:
        print(f"[dashboard_api] {method} {url} failed: {e}")
        return None


# -------------------------
# Public API functions (all call backend endpoints)
# -------------------------


@st.cache_data(ttl=30)
def list_students(course_id: Optional[int] = None) -> pd.DataFrame:
    """Fetch all students from /students/getall endpoint.
    
    Returns a DataFrame with columns: student_id, first_name, last_name, address, 
    course_id, year_of_study, email, course_name
    """
    path = ENDPOINTS.get("list_students", "/students/getall")
    payload = _fetch_json(path)
    if payload is None:
        return pd.DataFrame()
    
    df = pd.DataFrame(payload)
    
    # Filter by course_id if provided
    if course_id is not None and 'course_id' in df.columns:
        df = df[df['course_id'] == course_id]
    
    return df



def create_student(student: Dict) -> Dict:
    path = ENDPOINTS.get("create_student", "/students")
    payload = _request_json("POST", path, json_payload=student)
    return payload or {}


def update_student(student_id: int, updates: Dict) -> Dict:
    path = ENDPOINTS.get("update_student", "/CRUD/student/update/{id}").format(id=student_id)
    payload = _request_json("PUT", path, json_payload=updates)
    return payload or {}


def delete_student(student_id: int) -> bool:
    path = ENDPOINTS.get("delete_student", "/students/{id}").format(id=student_id)
    res = _request_json("DELETE", path)
    return res is not None


def delete_student_crud(student_id: int) -> bool:
    """Call the backend CRUD delete endpoint and return boolean success.

    The backend route provided is expected to be like
    `/CRUD/student/delete/{student_id}`. We perform a DELETE request and
    normalize the backend response to a boolean True (success) or False.
    """
    path = ENDPOINTS.get("delete_student_crud", "/CRUD/student/delete/{student_id}").format(student_id=student_id)
    payload = _request_json("DELETE", path, json_payload={})
    # Normalize to boolean: backend may return a JSON boolean, or an object
    if payload is None:
        return False
    if isinstance(payload, bool):
        return payload
    if isinstance(payload, dict):
        succ = payload.get("success")
        if succ is True or (isinstance(succ, str) and succ.lower() == "true"):
            return True
        # some backends return the updated student object on success
        if payload.get("student") or payload.get("updated"):
            return True
        return False
    # Fallback: truthiness
    return bool(payload)


@st.cache_data(ttl=300)
def get_courses() -> List[Dict]:
    path = ENDPOINTS.get("courses", "/director/coursesdropdown")
    # path = "/director/coursesdropdown"
    payload = _fetch_json(path)
    if payload is None:
        return []
    # Normalize various possible backend keys
    out = []
    for c in payload:
        if isinstance(c, dict):
            name = c.get("name") or c.get("course_name") or c.get("course")
            out.append({"id": c.get("id"), "name": name})
        else:
            out.append(c)
    return out


@st.cache_data(ttl=300)
def get_modules_for_course(course_id: int) -> List[Dict]:
    path = ENDPOINTS.get("modules_for_course", "/director/modules/{course_id}").format(course_id=course_id)
    payload = _fetch_json(path)
    if payload is None:
        return []
    return payload


@st.cache_data(ttl=30)
def get_director_summary(course_id: Optional[int], module_id: Optional[int], date_range) -> Dict:
    path = ENDPOINTS.get("director_summary", "/director/summary/{course_id}").format(course_id=course_id or "")
    params = {}
    if module_id is not None:
        params["module_id"] = module_id
    if date_range:
        params["date_range"] = date_range

    payload = _fetch_json(path, params=params)
    return payload or {}


@st.cache_data(ttl=300)
def get_director_averages(course_id: Optional[int] = None, module_id: Optional[int] = None) -> Dict:
    """Fetch attendance and performance averages.
    
    Args:
        course_id: Optional course ID. If None, returns overall averages.
        module_id: Optional module ID. Only used if course_id is provided.
    
    Returns:
        Dict with 'attendance' and 'performance' keys.
    """
    path = ENDPOINTS.get("director_averages", "/director/Averages")
    
    # Build query parameters
    params = {}
    if course_id is not None:
        params["course_id"] = course_id
    if module_id is not None:
        params["module_id"] = module_id
    
    payload = _fetch_json(path, params=params if params else None)
    if payload is None:
        return {"attendance": 0, "performance": 0}
    return payload


@st.cache_data(ttl=60)
def get_course_comparison() -> pd.DataFrame:
    path = ENDPOINTS.get("course_comparison", "/director/course_comparison")
    payload = _fetch_json(path)
    if payload is None:
        return pd.DataFrame()
    return pd.DataFrame(payload)


@st.cache_data(ttl=60)
def get_module_comparison(course_id: int) -> pd.DataFrame:
    path = ENDPOINTS.get("module_comparison", "/director/module_comparison/{course_id}").format(course_id=course_id)
    payload = _fetch_json(path)
    if payload is None:
        return pd.DataFrame()
    return pd.DataFrame(payload)


@st.cache_data(ttl=15)
def get_attendance_vs_performance(course_id: Optional[int], module_id: Optional[int] = None, date_range=None) -> pd.DataFrame:
    """Fetch attendance vs performance data for a course.
    
    Returns a DataFrame with columns: module_name, attendance, performance
    """
    if course_id is None:
        return pd.DataFrame()
    
    path = ENDPOINTS.get("attendance_vs_performance", "/director/barplot/{course_id}").format(course_id=course_id)
    payload = _fetch_json(path)
    if payload is None:
        return pd.DataFrame()
    
    # Payload is list of dicts with module_name, attendance, performance
    return pd.DataFrame(payload)


@st.cache_data(ttl=300)
def get_grade_distribution(course_id: int, module_id: int) -> Dict:
    """Fetch grade distribution for a specific module in a course.
    
    Returns a dictionary mapping student IDs to grades.
    Example: {"26": 68.5, "27": 75.5, ...}
    """
    path = ENDPOINTS.get("grade_distribution", "/director/gradedistribution/{course_id}/{module_id}")
    path = path.format(course_id=course_id, module_id=module_id)
    payload = _fetch_json(path)
    if payload is None:
        return {}
    return payload


@st.cache_data(ttl=300)
def get_student_risk_matrix(course_id: int, module_id: int) -> Dict:
    """Fetch student risk matrix for a specific module in a course.
    
    Returns a dictionary mapping student IDs to their risk information.
    Example: {"1": {"first_name": "James", "last_name": "Smith", "attendance": 75.0, ...}}
    """
    path = ENDPOINTS.get("student_risk", "/director/Studentrisk/{course_id}/{module_id}")
    path = path.format(course_id=course_id, module_id=module_id)
    payload = _fetch_json(path)
    if payload is None:
        return {}
    return payload


@st.cache_data(ttl=30)
def get_wellbeing_overview(date_range, search: Optional[str], risk_filter: str) -> Dict:
    path = ENDPOINTS.get("wellbeing_overview", "/wellbeing/overview")
    params = {"date_range": date_range, "search": search, "risk_filter": risk_filter}
    payload = _fetch_json(path, params=params)
    return payload or {}


@st.cache_data(ttl=30)
def get_wellbeing_all(course_id: Optional[int] = None) -> pd.DataFrame:
    """Fetch all wellbeing records from /wellbeing/getall endpoint.
    
    Args:
        course_id: Optional course ID to filter wellbeing records by course.
                  If None, fetches all records from /wellbeing/getall without parameters.
    """
    path = ENDPOINTS.get("wellbeing_getall", "/wellbeing/getall")
    # For "All Courses" (course_id=None), don't add query parameters
    # For specific course, add course_id parameter
    # Use 10 second timeout for large dataset (3000+ records)
    if course_id is None:
        payload = _fetch_json(path, params=None, timeout=10)
    else:
        payload = _fetch_json(path, params={"course_id": course_id}, timeout=10)
    
    if payload is None:
        return pd.DataFrame()
    return pd.DataFrame(payload)


@st.cache_data(ttl=30)
def get_stress_avg_plot() -> pd.DataFrame:
    """Fetch average stress levels by course from /wellbeing/stress_avg_plot endpoint."""
    path = ENDPOINTS.get("stress_avg_plot", "/wellbeing/stress_avg_plot")
    payload = _fetch_json(path)
    if payload is None:
        return pd.DataFrame()
    return pd.DataFrame(payload)


def create_wellbeing_record(wellbeing_data: Dict) -> Dict:
    """Create a new wellbeing record via POST /wellbeing/create."""
    path = ENDPOINTS.get("wellbeing_create", "/wellbeing/create")
    return _request_json("POST", path, json_payload=wellbeing_data) or {}


@st.cache_data(ttl=30)
def get_priority_actions(date_range, search: Optional[str], risk_filter: str) -> pd.DataFrame:
    path = ENDPOINTS.get("priority_actions", "/wellbeing/priority_actions")
    params = {"date_range": date_range, "search": search, "risk_filter": risk_filter}
    payload = _fetch_json(path, params=params)
    if payload is None:
        return pd.DataFrame()
    return pd.DataFrame(payload)


@st.cache_data(ttl=30)
def get_wellbeing_trends(student_id: Optional[int], date_range) -> pd.DataFrame:
    path = ENDPOINTS.get("wellbeing_trends", "/wellbeing/trends/{student_id}").format(student_id=student_id or "")
    params = {"date_range": date_range}
    payload = _fetch_json(path, params=params)
    if payload is None:
        return pd.DataFrame()
    return pd.DataFrame(payload)


@st.cache_data(ttl=30)
def get_burnout_scatter(date_range, search: Optional[str], risk_filter: str) -> pd.DataFrame:
    path = ENDPOINTS.get("burnout_scatter", "/wellbeing/burnout_scatter")
    params = {"date_range": date_range, "search": search, "risk_filter": risk_filter}
    payload = _fetch_json(path, params=params)
    if payload is None:
        return pd.DataFrame()
    return pd.DataFrame(payload)


@st.cache_data(ttl=300)
def get_sessions_for_module(course_id: int, module_id: int) -> pd.DataFrame:
    path = ENDPOINTS.get("sessions_for_module", "/explorer/sessions/{course_id}/{module_id}").format(course_id=course_id, module_id=module_id)
    payload = _fetch_json(path)
    if payload is None:
        return pd.DataFrame()
    return pd.DataFrame(payload)


# -------------------------
# Course CRUD operations
# -------------------------

@st.cache_data(ttl=30)
def list_courses() -> pd.DataFrame:
    """Fetch all courses from /CRUD/course/getall endpoint."""
    path = ENDPOINTS.get("list_courses", "/CRUD/course/getall")
    payload = _fetch_json(path)
    if payload is None:
        return pd.DataFrame()
    return pd.DataFrame(payload)


def create_course(course_data: Dict) -> Dict:
    """Create a new course via POST /CRUD/course/create."""
    path = ENDPOINTS.get("create_course", "/CRUD/course/create")
    return _request_json("POST", path, json_payload=course_data) or {}


def update_course(course_id: int, updates: Dict) -> Dict:
    """Update a course via PUT /CRUD/course/update/{id}."""
    path = ENDPOINTS.get("update_course", "/CRUD/course/update/{id}").format(id=course_id)
    return _request_json("PUT", path, json_payload=updates) or {}


def delete_course(course_id: int) -> bool:
    """Delete a course via DELETE /CRUD/course/delete/{id}."""
    path = ENDPOINTS.get("delete_course", "/CRUD/course/delete/{id}").format(id=course_id)
    result = _request_json("DELETE", path)
    if result is None:
        return False
    if isinstance(result, dict):
        success = result.get("success")
        if success is True or (isinstance(success, str) and success.lower() == "true"):
            return True
        if result.get("message") and "deleted" in result.get("message", "").lower():
            return True
    return bool(result)


# -------------------------
# Module CRUD operations
# -------------------------

@st.cache_data(ttl=30)
def list_modules(course_id: int) -> pd.DataFrame:
    """Fetch all modules for a specific course from /CRUD/module/getall/{course_id} endpoint."""
    path = ENDPOINTS.get("list_modules", "/CRUD/module/getall/{course_id}").format(course_id=course_id)
    payload = _fetch_json(path)
    if payload is None:
        return pd.DataFrame()
    return pd.DataFrame(payload)


def create_module(module_data: Dict, course_id) -> Dict:
    """Create a new module via POST /CRUD/module/create."""
    path = ENDPOINTS.get("create_module", "/CRUD/module/create/{cid}").format(course_id=course_id)
    return _request_json("POST", path, json_payload=module_data) or {}


def update_module(module_id: int, updates: Dict) -> Dict:
    """Update a module via PUT /CRUD/module/update/{id}."""
    path = ENDPOINTS.get("update_module", "/CRUD/module/update/{id}").format(id=module_id)
    return _request_json("PUT", path, json_payload=updates) or {}


def delete_module(module_id: int) -> bool:
    """Delete a module via DELETE /CRUD/module/delete/{id}."""
    path = ENDPOINTS.get("delete_module", "/CRUD/module/delete/{id}").format(id=module_id)
    result = _request_json("DELETE", path)
    if result is None:
        return False
    if isinstance(result, dict):
        success = result.get("success")
        if success is True or (isinstance(success, str) and success.lower() == "true"):
            return True
        if result.get("message") and "deleted" in result.get("message", "").lower():
            return True
    return bool(result)
