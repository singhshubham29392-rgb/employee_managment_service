import csv, tempfile, unittest
from pathlib import Path
from app.database import Database
from app.auth import create_admin, authenticate
from app.services.employee_service import EmployeeService
from app.services.department_service import DepartmentService
from app.services.report_service import export_csv

class SystemTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.db=Database(Path(self.tmp.name)/"test.sqlite3"); self.es=EmployeeService(self.db); self.ds=DepartmentService(self.db)
        self.department=self.ds.list()[0]
        self.data={"full_name":"Ada Example","email":"ada@example.org","phone":"+1 555 010 2020","gender":"","date_of_birth":"","address":"","department_id":self.department["id"],"designation":"Analyst","joining_date":"2020-01-10","status":"Active","salary":"52000","emergency_contact":"","notes":""}
    def tearDown(self): self.tmp.cleanup()
    def test_database_initializes_and_seeds_departments(self): self.assertGreaterEqual(len(self.ds.list()),5)
    def test_admin_hash_auth(self):
        create_admin(self.db,"adminuser","correct-horse-12"); self.assertTrue(authenticate(self.db,"adminuser","correct-horse-12")); self.assertFalse(authenticate(self.db,"adminuser","wrong-password"))
    def test_employee_create_search_update_delete(self):
        eid=self.es.save(self.data); self.assertEqual(len(self.es.list("Ada")),1); self.data["designation"]="Lead"; self.es.save(self.data,eid); self.assertEqual(self.es.get(eid)["designation"],"Lead"); self.es.delete(eid); self.assertEqual(self.es.stats()["total"],0)
    def test_required_validation_and_duplicate_email(self):
        d=self.data.copy(); d["full_name"]=""
        with self.assertRaises(ValueError): self.es.save(d)
        self.es.save(self.data)
        with self.assertRaises(Exception): self.es.save(self.data)
    def test_department_in_use_and_duplicate(self):
        with self.assertRaises(ValueError): self.ds.save(self.department["name"])
        eid=self.es.save(self.data)
        with self.assertRaises(ValueError): self.ds.delete(self.department["id"])
        self.es.delete(eid)
    def test_csv_and_dashboard(self):
        self.es.save(self.data)
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"employees.csv"; export_csv(self.es.list(),path)
            with path.open(encoding="utf-8-sig") as f: rows=list(csv.reader(f))
            self.assertEqual(len(rows),2); self.assertEqual(rows[1][1],"Ada Example")
        self.assertEqual(self.es.stats()["active"],1); self.assertEqual(self.es.stats()["total"],1)

if __name__=="__main__": unittest.main()
