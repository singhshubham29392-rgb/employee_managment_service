import hashlib, hmac, secrets

ITERATIONS = 600_000

def create_admin(db, username, password):
    username = username.strip()
    if len(username) < 3: raise ValueError("Username must be at least 3 characters.")
    if len(password) < 10: raise ValueError("Password must be at least 10 characters.")
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS)
    try:
        with db.connect() as c: c.execute("INSERT INTO admins(username,salt,password_hash,iterations) VALUES(?,?,?,?)", (username,salt,digest,ITERATIONS))
    except Exception as e:
        if "UNIQUE" in str(e): raise ValueError("That username already exists.")
        raise

def authenticate(db, username, password):
    with db.connect() as c: row = c.execute("SELECT salt,password_hash,iterations FROM admins WHERE username=?", (username.strip(),)).fetchone()
    if not row: return False
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), row["salt"], row["iterations"])
    return hmac.compare_digest(candidate, row["password_hash"])
