import csv

EXPORT_COLUMNS=("employee_code","full_name","email","phone","department","designation","joining_date","status","salary")

def export_csv(rows,path):
    with open(path,"w",newline="",encoding="utf-8-sig") as f:
        writer=csv.writer(f); writer.writerow([x.replace("_"," ").title() for x in EXPORT_COLUMNS])
        writer.writerows([[r.get(x) if hasattr(r,"get") else r[x] for x in EXPORT_COLUMNS] for r in rows])

def employee_html(row):
    import html
    fields=[("Employee ID","employee_code"),("Full name","full_name"),("Email","email"),("Phone","phone"),("Department","department"),("Designation","designation"),("Joining date","joining_date"),("Status","status"),("Salary","salary"),("Address","address"),("Notes","notes")]
    body="".join(f"<tr><th>{html.escape(label)}</th><td>{html.escape(str(row[key] or ''))}</td></tr>" for label,key in fields)
    return "<!doctype html><meta charset='utf-8'><title>Employee profile</title><style>body{font:16px Arial;max-width:760px;margin:40px auto;color:#17233b}h1{color:#153158}table{border-collapse:collapse;width:100%}td,th{padding:12px;border:1px solid #ccd4df;text-align:left}th{width:32%;background:#eef2f7}@media print{button{display:none}}</style><h1>Employee Management System</h1><h2>Employee Profile</h2><p>Generated locally</p><button onclick='window.print()'>Print</button><table>"+body+"</table>"
