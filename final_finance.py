from flask import Flask, request, session, redirect, render_template_string

app = Flask(__name__)
app.secret_key = 'final_finance_2026'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form.get('username', 'admin')
        return redirect('/')
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🦅 دخول نوح المالي</title>
        <style>
            body { font-family:Tahoma; background:#0a0a2e; color:#fff; display:flex; justify-content:center; align-items:center; height:100vh; }
            .box { background:#1a1a3e; padding:40px; border-radius:25px; border:2px solid #FFD700; text-align:center; box-shadow:0 0 40px rgba(255,215,0,0.4); }
            h2 { color:#FFD700; }
            input { display:block; width:100%; padding:12px; margin:10px 0; background:#222; border:1px solid #FFD700; color:#fff; border-radius:10px; }
            button { width:100%; padding:12px; background:#FFD700; border:none; border-radius:10px; font-weight:bold; cursor:pointer; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>🦅 نوح المالي</h2>
            <form method="POST">
                <input type="text" name="username" placeholder="المستخدم (أي اسم)">
                <input type="password" name="password" placeholder="كلمة المرور (أي شيء)">
                <button type="submit">🚀 دخول</button>
            </form>
        </div>
    </body>
    </html>
    ''')

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')
    return f"<h1 style='text-align:center;color:#FFD700;font-family:Tahoma;'>🦅 مرحباً {session['user']} في نوح المالي</h1>"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

import sqlite3

DB = 'new_finance.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        balance REAL DEFAULT 0
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/accounts', methods=['GET','POST'])
def accounts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO accounts (name, type) VALUES (?,?)",
                  (request.form['name'], request.form['type']))
        conn.commit()
    c.execute("SELECT * FROM accounts")
    rows = c.fetchall()
    conn.close()
    return f"<h2>📚 الحسابات</h2><table border='1'><tr><th>ID</th><th>الاسم</th><th>النوع</th></tr>" + "".join(f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>" for r in rows) + "</table>"

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM accounts")
    accounts = c.fetchone()[0]
    conn.close()
    return f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>🦅 نوح المالي</title>
    <style>
        body {{ font-family:Tahoma; background:linear-gradient(135deg,#0a0a2e,#1a0a3e); color:#fff; padding:30px; }}
        h1 {{ text-align:center; color:#FFD700; font-size:2.5rem; }}
        .stats {{ display:flex; gap:20px; justify-content:center; margin:40px 0; }}
        .card {{ background:#1a1a3e; padding:30px; border-radius:20px; border:2px solid #FFD700; text-align:center; }}
        .card h2 {{ font-size:2.5rem; color:#FFD700; }}
        .nav {{ display:flex; flex-wrap:wrap; gap:10px; justify-content:center; }}
        .nav a {{ background:#1a1a3e; color:#fff; padding:15px 25px; border-radius:25px; text-decoration:none; border:1px solid #FFD700; }}
        .nav a:hover {{ background:#FFD700; color:#000; }}
    </style></head>
    <body>
        <h1>🦅 لوحة نوح المالية</h1>
        <div class="stats">
            <div class="card"><h2>{accounts}</h2>حسابات</div>
        </div>
        <div class="nav">
            <a href="/accounts">📚 الحسابات</a>
            <a href="/logout">🚪 خروج</a>
        </div>
    </body></html>
    """
