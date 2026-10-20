from pathlib import Path
import os

APP_NAME = "Employee Management System"
DATA_DIR = Path(os.environ.get("EMPLOYEE_MGMT_DATA", Path.home() / ".employee_management_system"))
DB_PATH = DATA_DIR / "employees.sqlite3"
LOG_PATH = DATA_DIR / "application.log"
DATE_FORMAT = "%Y-%m-%d"
