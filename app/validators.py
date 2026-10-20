import re
from datetime import date

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_RE = re.compile(r"^[+()\-\d .]{7,25}$")

def validate_employee(data):
    for key in ("full_name", "email", "phone", "department_id", "designation", "joining_date", "status"):
        if not str(data.get(key, "")).strip():
            raise ValueError(f"{key.replace('_', ' ').title()} is required.")
    if not EMAIL_RE.fullmatch(data["email"].strip()):
        raise ValueError("Enter a valid email address.")
    if not PHONE_RE.fullmatch(data["phone"].strip()):
        raise ValueError("Enter a valid phone number (7–25 characters).")
    try:
        joining = date.fromisoformat(data["joining_date"])
        if joining > date.today(): raise ValueError
        if data.get("date_of_birth"):
            dob = date.fromisoformat(data["date_of_birth"])
            if dob >= date.today(): raise ValueError
    except ValueError:
        raise ValueError("Dates must use YYYY-MM-DD; joining date cannot be in the future and birth date must be in the past.")
    try:
        if float(data.get("salary", 0)) < 0: raise ValueError
    except (TypeError, ValueError):
        raise ValueError("Salary must be a non-negative number.")
    if data["status"] not in ("Active", "On Leave", "Resigned"):
        raise ValueError("Choose a valid employment status.")
