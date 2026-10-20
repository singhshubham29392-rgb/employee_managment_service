from app.validators import validate_employee

FIELDS = ("full_name","email","phone","gender","date_of_birth","address","department_id","designation","joining_date","status","salary","emergency_contact","notes")

class EmployeeService:
    def __init__(self, db): self.db = db
    def list(self, query="", department="", status="", designation=""):
        sql = "SELECT e.*,d.name department FROM employees e JOIN departments d ON d.id=e.department_id WHERE 1=1"
        args=[]
        if query:
            q=f"%{query.strip()}%"; sql += " AND (e.employee_code LIKE ? OR e.full_name LIKE ? OR e.email LIKE ? OR e.phone LIKE ?)"; args += [q]*4
        if department: sql += " AND d.name=?"; args.append(department)
        if status: sql += " AND e.status=?"; args.append(status)
        if designation: sql += " AND e.designation LIKE ?"; args.append(f"%{designation}%")
        sql += " ORDER BY e.id DESC"
        with self.db.connect() as c: return c.execute(sql,args).fetchall()
    def get(self, employee_id):
        with self.db.connect() as c: return c.execute("SELECT * FROM employees WHERE id=?",(employee_id,)).fetchone()
    def save(self, data, employee_id=None):
        validate_employee(data)
        values=[data.get(k, "") for k in FIELDS]
        values[0]=data["full_name"].strip(); values[1]=data["email"].strip().lower(); values[2]=data["phone"].strip(); values[6]=int(data["department_id"]); values[9]=data["status"]; values[10]=float(data.get("salary") or 0)
        with self.db.connect() as c:
            if employee_id:
                c.execute("UPDATE employees SET "+",".join(k+"=?" for k in FIELDS)+",updated_at=CURRENT_TIMESTAMP WHERE id=?", values+[employee_id]); return employee_id
            cur=c.execute("INSERT INTO employees(employee_code,"+",".join(FIELDS)+") VALUES(?,"+",".join("?" for _ in FIELDS)+")", ["EMP-"+__import__("secrets").token_hex(4).upper()]+values)
            c.execute("UPDATE employees SET employee_code=? WHERE id=?",(f"EMP-{cur.lastrowid:05d}",cur.lastrowid)); return cur.lastrowid
    def delete(self, employee_id):
        with self.db.connect() as c: c.execute("DELETE FROM employees WHERE id=?",(employee_id,))
    def stats(self):
        with self.db.connect() as c:
            counts={r["status"]:r["n"] for r in c.execute("SELECT status,COUNT(*) n FROM employees GROUP BY status")}
            return {"total":sum(counts.values()),"active":counts.get("Active",0),"leave":counts.get("On Leave",0),"resigned":counts.get("Resigned",0),"departments":c.execute("SELECT COUNT(*) FROM departments").fetchone()[0],"recent":c.execute("SELECT employee_code,full_name,joining_date FROM employees ORDER BY created_at DESC LIMIT 5").fetchall(),"by_department":c.execute("SELECT d.name,COUNT(e.id) n FROM departments d LEFT JOIN employees e ON e.department_id=d.id GROUP BY d.id ORDER BY d.name").fetchall()}
