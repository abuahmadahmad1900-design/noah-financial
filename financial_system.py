import sqlite3, hashlib, shutil, csv, io, os
from flask import Flask, render_template_string, request, session, redirect, Response
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'noah2026'
DB = 'noah.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT);
    CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, name TEXT, type TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS suppliers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS purchase_orders (id INTEGER PRIMARY KEY, supplier_id INTEGER, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER);
    CREATE TABLE IF NOT EXISTS bank_moves (id INTEGER PRIMARY KEY, date TEXT, desc TEXT, amount REAL);
    CREATE TABLE IF NOT EXISTS zakat (id INTEGER PRIMARY KEY, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS debts (id INTEGER PRIMARY KEY, name TEXT, amount REAL, type TEXT);
    CREATE TABLE IF NOT EXISTS budgets (id INTEGER PRIMARY KEY, name TEXT, amount REAL);
    CREATE TABLE IF NOT EXISTS assets (id INTEGER PRIMARY KEY, name TEXT, value REAL);
    CREATE TABLE IF NOT EXISTS currencies (id INTEGER PRIMARY KEY, code TEXT, rate REAL);
    ''')
    hashed = hashlib.sha256('123456'.encode()).hexdigest()
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', ?)", (hashed,))
    conn.commit()
    conn.close()

init_db()

PAGE_STYLE = '''
<style>
    body { 
    font-family:Tahoma; 
    background: linear-gradient(180deg, #0a0a2e, #1a0a3e, #0a0a2e);
    color:#eee; 
    padding:20px; 
    direction:rtl; 
    min-height:100vh;
    animation: bg-shift 10s ease infinite;
}
@keyframes bg-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
a { 
    color:#4af; 
    text-decoration:none; 
    margin:5px;
    transition: all 0.3s;
}
a:hover {
    color:#FFD700;
    text-shadow: 0 0 10px rgba(255,215,0,0.8);
}
input, select, button { 
    padding:8px; 
    margin:5px; 
    background:#222; 
    color:#eee; 
    border:1px solid #555; 
    border-radius:5px;
    transition: all 0.3s;
}
input:focus, select:focus {
    border-color: #FFD700;
    box-shadow: 0 0 15px rgba(255,215,0,0.3);
}
button { 
    background: linear-gradient(45deg, #FFD700, #FF8C00);
    color:#000; 
    cursor:pointer;
    font-weight: bold;
    border: none;
}
button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(255,215,0,0.4);
}
table { 
    width:100%; 
    border-collapse:collapse; 
    margin-top:15px;
}
th, td { 
    border:1px solid #444; 
    padding:8px; 
    text-align:center;
    transition: all 0.3s;
}
tr:hover td {
    background: rgba(255,215,0,0.05);
}
th { 
    background: linear-gradient(145deg, #1a1a4e, #0d0d2e); 
    color:#FFD700;
    text-shadow: 0 0 5px rgba(255,215,0,0.5);
}
.container { 
    background: rgba(20,20,50,0.8);
    padding:20px; 
    border-radius:20px;
    border: 1px solid rgba(255,215,0,0.3);
    box-shadow: 0 0 30px rgba(255,215,0,0.1);
    backdrop-filter: blur(10px);
}
.nav { 
    background: linear-gradient(145deg, #1a1a4e, #0d0d2e);
    padding:15px; 
    border-radius:15px; 
    margin-bottom:15px;
    border: 1px solid rgba(0,200,255,0.3);
    box-shadow: 0 0 20px rgba(0,200,255,0.1);
}
    a { color:#4af; text-decoration:none; margin:5px; }
    input, select, button { padding:8px; margin:5px; background:#222; color:#eee; border:1px solid #555; border-radius:5px; }
    button { background:#4af; color:#000; cursor:pointer; }
    table { width:100%; border-collapse:collapse; margin-top:15px; }
    th, td { border:1px solid #444; padding:8px; text-align:center; }
    th { background:#333; color:#4af; }
    .container { background:#1a1a1a; padding:20px; border-radius:10px; }
    .nav { background:#1a1a3e; padding:10px; border-radius:5px; margin-bottom:15px; }
</style>
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
        user = c.fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect('/')
        return redirect('/login?error=1')
    return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>نوح - الدخول</title></head>
    <body style="font-family:Tahoma;background:#0a0a2e;color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;">
        <div style="background:#1a1a3e;padding:40px;border-radius:20px;border:1px solid #FFD700;">
            <h1 style="text-align:center;color:#FFD700;">🦅 نوح</h1>
            <form method="POST">
                <input type="text" name="username" placeholder="المستخدم" required style="display:block;width:100%;padding:10px;margin:10px 0;border-radius:10px;border:1px solid #555;background:#222;color:#fff;">
                <input type="password" name="password" placeholder="كلمة المرور" required style="display:block;width:100%;padding:10px;margin:10px 0;border-radius:10px;border:1px solid #555;background:#222;color:#fff;">
                <button style="width:100%;padding:12px;background:#FFD700;border:none;border-radius:10px;font-weight:bold;cursor:pointer;">دخول</button>
            </form>
        </div>
    </body></html>'''

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/')
def index():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM accounts"); accounts = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM suppliers"); suppliers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM invoices"); invoices = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products"); products = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM bank_moves"); bank_moves = c.fetchone()[0]
    conn.close()

    return f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🦅 نوح - السحر المالي</title>
        <style>
            * {{ margin:0; padding:0; box-sizing:border-box; }}
            body {{
                font-family: Tahoma, sans-serif;
                background: linear-gradient(135deg, #0a0a2e, #1a0a3e, #0a1a2e, #0a0a2e);
                background-size: 400% 400%;
                animation: bg-shift 10s ease infinite;
                color: #fff;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            @keyframes bg-shift {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            .container {{
                width: 100%;
                max-width: 1100px;
                background: rgba(20,20,50,0.85);
                backdrop-filter: blur(15px);
                border-radius: 30px;
                padding: 40px;
                border: 2px solid rgba(255,215,0,0.5);
                box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 40px rgba(255,215,0,0.3), 0 0 80px rgba(0,200,255,0.2);
                animation: glow 3s ease-in-out infinite alternate;
            }}
            @keyframes glow {{
                from {{ box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 20px rgba(255,215,0,0.2); }}
                to {{ box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 50px rgba(255,215,0,0.6), 0 0 100px rgba(0,200,255,0.3); }}
            }}
            h1 {{
                text-align: center;
                font-size: 3rem;
                background: linear-gradient(45deg, #FFD700, #FF8C00, #FFD700);
                background-size: 300% 300%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gradient-shift 3s ease infinite;
                margin-bottom: 10px;
            }}
            @keyframes gradient-shift {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            .subtitle {{
                text-align: center;
                color: #ccc;
                margin-bottom: 40px;
                font-size: 1.1rem;
                letter-spacing: 1px;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            .stat-card {{
                background: linear-gradient(145deg, #1a1a4e, #0d0d2e);
                border-radius: 20px;
                padding: 30px 20px;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.15);
                transition: all 0.3s;
                cursor: pointer;
                animation: float-card 3s ease-in-out infinite;
            }}
            .stat-card:nth-child(2) {{ animation-delay: 0.3s; }}
            .stat-card:nth-child(3) {{ animation-delay: 0.6s; }}
            .stat-card:nth-child(4) {{ animation-delay: 0.9s; }}
            .stat-card:nth-child(5) {{ animation-delay: 1.2s; }}
            .stat-card:nth-child(6) {{ animation-delay: 1.5s; }}
            @keyframes float-card {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-8px); }}
            }}
            .stat-card:hover {{
                transform: translateY(-12px) rotate(2deg) scale(1.05);
                border-color: #00c8ff;
                box-shadow: 0 15px 40px rgba(0,200,255,0.5);
            }}
            .stat-card .icon {{
                font-size: 3rem;
                margin-bottom: 15px;
                animation: bounce 2s ease-in-out infinite;
            }}
            @keyframes bounce {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-10px); }}
            }}
            .stat-card .value {{
                font-size: 2.5rem;
                font-weight: 900;
                text-shadow: 0 0 20px rgba(0,200,255,0.8), 0 0 40px rgba(255,215,0,0.4);
            }}
            .stat-card .label {{
                color: #ccc;
                font-size: 0.9rem;
                margin-top: 8px;
            }}
            .highlight {{
                background: linear-gradient(145deg, #2a2a5e, #1a1a3e);
                border-radius: 25px;
                padding: 40px;
                text-align: center;
                margin-bottom: 30px;
                border: 2px solid rgba(255,215,0,0.5);
                position: relative;
                overflow: hidden;
            }}
            .highlight::before {{
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,215,0,0.1), transparent 70%);
                animation: pulse-bg 3s ease-in-out infinite;
            }}
            @keyframes pulse-bg {{
                0%, 100% {{ transform: scale(1); opacity: 0.5; }}
                50% {{ transform: scale(1.3); opacity: 1; }}
            }}
            .highlight h2 {{
                color: #FFD700;
                margin-bottom: 15px;
                position: relative;
                z-index: 1;
            }}
            .highlight .amount {{
                font-size: 3.5rem;
                font-weight: 900;
                background: linear-gradient(45deg, #FFD700, #FF8C00, #FFD700);
                background-size: 200% 200%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gradient-shift 2s ease infinite;
                position: relative;
                z-index: 1;
            }}
            .nav-links {{
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                justify-content: center;
            }}
            .nav-links a {{
                background: linear-gradient(145deg, #222255, #111133);
                color: #fff;
                padding: 14px 25px;
                border-radius: 30px;
                text-decoration: none;
                font-size: 0.9rem;
                border: 1px solid rgba(255,255,255,0.2);
                transition: all 0.3s;
                position: relative;
                overflow: hidden;
            }}
            .nav-links a:hover {{
                background: #00c8ff;
                color: #000;
                transform: scale(1.1);
                box-shadow: 0 0 30px rgba(0,200,255,0.6);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🦅 نوح - السحر المالي</h1>
            <p class="subtitle">النظام المالي الأسطوري</p>

            <div class="stats-grid">
                <div class="stat-card"><div class="icon">📚</div><div class="value">{accounts}</div><div class="label">الحسابات</div></div>
                <div class="stat-card"><div class="icon">👥</div><div class="value">{customers}</div><div class="label">العملاء</div></div>
                <div class="stat-card"><div class="icon">📦</div><div class="value">{suppliers}</div><div class="label">الموردون</div></div>
                <div class="stat-card"><div class="icon">🧾</div><div class="value">{invoices}</div><div class="label">الفواتير</div></div>
                <div class="stat-card"><div class="icon">📦</div><div class="value">{products}</div><div class="label">المنتجات</div></div>
                <div class="stat-card"><div class="icon">🏦</div><div class="value">{bank_moves}</div><div class="label">حركات بنكية</div></div>
            </div>

            <div class="highlight">
                <h2>💰 إجمالي الإيرادات</h2>
                <div class="amount">{revenue}</div>
            </div>

            <div class="nav-links">
                <a href="/accounts">📚 الحسابات</a>
                <a href="/customers">👥 العملاء</a>
                <a href="/suppliers">📦 الموردون</a>
                <a href="/invoices">🧾 الفواتير</a>
                <a href="/products">📦 المنتجات</a>
                <a href="/bank">🏦 البنك</a>
                <a href="/zakat">🕌 الزكاة</a>
                <a href="/debts">💳 الديون</a>
                <a href="/budgets">📋 الميزانيات</a>
                <a href="/assets">🏢 الأصول</a>
                <a href="/currencies">💱 العملات</a>
                <a href="/ai_center">🧠 25 عقل ذكي</a>
                <a href="/all_systems">📊 50 نظام</a>
                <a href="/self_dev">🧬 تطوير ذاتي</a>
                <a href="/all_systems">📊 كل الأنظمة</a>
                <a href="/logout">🚪 خروج</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/all_systems')
def all_systems():
    if 'user' not in session: return redirect('/login')
    systems = [
        ("/accounts", "📚", "الحسابات"),
        ("/customers", "👥", "العملاء"),
        ("/suppliers", "📦", "الموردون"),
        ("/invoices", "🧾", "الفواتير"),
        ("/products", "📦", "المنتجات"),
        ("/bank", "🏦", "البنك"),
        ("/zakat", "🕌", "الزكاة"),
        ("/debts", "💳", "الديون"),
        ("/budgets", "📋", "الميزانيات"),
        ("/assets", "🏢", "الأصول"),
        ("/currencies", "💱", "العملات"),
    ]
    content = '<h2 style="text-align:center;color:#FFD700;">📊 كل الأنظمة العاملة</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;">'
    for path, icon, name in systems:
        content += f'<a href="{path}" style="background:#1a1a3e;padding:20px;border-radius:10px;text-align:center;"><div style="font-size:2rem;">{icon}</div>{name}</a>'
    content += '</div><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/accounts', methods=['GET','POST'])
def accounts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO accounts (name, type) VALUES (?,?)", (request.form['name'], request.form['type']))
        conn.commit()
    c.execute("SELECT * FROM accounts")
    rows = c.fetchall(); conn.close()
    content = '<h2>📚 الحسابات</h2><form method="POST"><input name="name" placeholder="اسم الحساب" required><select name="type"><option>أصول</option><option>خصوم</option><option>إيرادات</option><option>مصاريف</option></select><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>النوع</th><th>الرصيد</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/customers', methods=['GET','POST'])
def customers():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO customers (name, phone) VALUES (?,?)", (request.form['name'], request.form['phone']))
        conn.commit()
    c.execute("SELECT * FROM customers")
    rows = c.fetchall(); conn.close()
    content = '<h2>👥 العملاء</h2><form method="POST"><input name="name" placeholder="اسم العميل" required><input name="phone" placeholder="الهاتف"><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>الهاتف</th><th>الرصيد</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/suppliers', methods=['GET','POST'])
def suppliers():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO suppliers (name, phone) VALUES (?,?)", (request.form['name'], request.form['phone']))
        conn.commit()
    c.execute("SELECT * FROM suppliers")
    rows = c.fetchall(); conn.close()
    content = '<h2>📦 الموردون</h2><form method="POST"><input name="name" placeholder="اسم المورد" required><input name="phone" placeholder="الهاتف"><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>الهاتف</th><th>الرصيد</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/invoices', methods=['GET','POST'])
def invoices():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (?,?,?)", (request.form['customer_id'], request.form['amount'], request.form['date']))
        conn.commit()
    c.execute("SELECT * FROM invoices")
    rows = c.fetchall(); conn.close()
    content = '<h2>🧾 الفواتير</h2><form method="POST"><input name="customer_id" placeholder="عميل ID" required><input name="amount" placeholder="مبلغ" required><input name="date" type="date" required><button>إصدار</button></form><table><tr><th>ID</th><th>العميل</th><th>المبلغ</th><th>التاريخ</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/products', methods=['GET','POST'])
def products():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO products (name, price, stock) VALUES (?,?,?)", (request.form['name'], request.form['price'], request.form['stock']))
        conn.commit()
    c.execute("SELECT * FROM products")
    rows = c.fetchall(); conn.close()
    content = '<h2>📦 المنتجات</h2><form method="POST"><input name="name" placeholder="اسم المنتج" required><input name="price" placeholder="السعر" required><input name="stock" placeholder="المخزون" required><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>السعر</th><th>المخزون</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/bank', methods=['GET','POST'])
def bank():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES (?,?,?)", (request.form['date'], request.form['desc'], request.form['amount']))
        conn.commit()
    c.execute("SELECT * FROM bank_moves")
    rows = c.fetchall(); conn.close()
    content = '<h2>🏦 البنك</h2><form method="POST"><input name="date" type="date" required><input name="desc" placeholder="الوصف" required><input name="amount" placeholder="المبلغ" required><button>إضافة</button></form><table><tr><th>ID</th><th>التاريخ</th><th>الوصف</th><th>المبلغ</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/zakat', methods=['GET','POST'])
def zakat():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO zakat (amount, date) VALUES (?,?)", (request.form['amount'], request.form['date']))
        conn.commit()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0")
    total = c.fetchone()[0]
    c.execute("SELECT * FROM zakat")
    rows = c.fetchall(); conn.close()
    nisab = 85 * 60
    due = total * 0.025 if total >= nisab else 0
    content = f'<h2>🕌 الزكاة</h2><p>💰 النقود: {total}</p><p>📏 النصاب: {nisab}</p><p style="color:#FFD700;font-size:1.5rem;">🧮 المستحقة: {due:.2f}</p><form method="POST"><input name="amount" placeholder="مبلغ" required><input name="date" type="date" required><button>تسجيل</button></form><table><tr><th>ID</th><th>مبلغ</th><th>تاريخ</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/debts', methods=['GET','POST'])
def debts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO debts (name, amount, type) VALUES (?,?,?)", (request.form['name'], request.form['amount'], request.form['type']))
        conn.commit()
    c.execute("SELECT * FROM debts")
    rows = c.fetchall(); conn.close()
    content = '<h2>💳 الديون</h2><form method="POST"><input name="name" placeholder="اسم" required><input name="amount" placeholder="مبلغ" required><select name="type"><option>علينا</option><option>لنا</option></select><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>مبلغ</th><th>نوع</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/budgets', methods=['GET','POST'])
def budgets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO budgets (name, amount) VALUES (?,?)", (request.form['name'], request.form['amount']))
        conn.commit()
    c.execute("SELECT * FROM budgets")
    rows = c.fetchall(); conn.close()
    content = '<h2>📋 الميزانيات</h2><form method="POST"><input name="name" placeholder="اسم" required><input name="amount" placeholder="مبلغ" required><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>المبلغ</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/assets', methods=['GET','POST'])
def assets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO assets (name, value) VALUES (?,?)", (request.form['name'], request.form['value']))
        conn.commit()
    c.execute("SELECT * FROM assets")
    rows = c.fetchall(); conn.close()
    content = '<h2>🏢 الأصول</h2><form method="POST"><input name="name" placeholder="اسم الأصل" required><input name="value" placeholder="القيمة" required><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>القيمة</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/currencies', methods=['GET','POST'])
def currencies():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO currencies (code, rate) VALUES (?,?)", (request.form['code'], request.form['rate']))
        conn.commit()
    c.execute("SELECT * FROM currencies")
    rows = c.fetchall(); conn.close()
    content = '<h2>💱 العملات</h2><form method="POST"><input name="code" placeholder="رمز" required><input name="rate" placeholder="سعر" required><button>إضافة</button></form><table><tr><th>ID</th><th>رمز</th><th>سعر</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content


# ========== 25 عقل ذكاء اصطناعي ==========
@app.route('/ai_center')
def ai_center():
    if 'user' not in session: return redirect('/login')
    ais = [
        ("🧠", "المحلل المالي", "تحليل البيانات المالية", "/accounts"),
        ("🔮", "المتنبئ", "توقع الإيرادات", "/invoices"),
        ("🛡️", "حارس المخاطر", "كشف المخاطر", "/debts"),
        ("🕌", "حاسب الزكاة", "حساب الزكاة", "/zakat"),
        ("👑", "الاستراتيجي", "خطط استراتيجية", "/budgets"),
        ("💵", "مراقب التدفق", "مراقبة التدفقات", "/bank"),
        ("📈", "محلل الربح", "تحليل الربحية", "/accounts"),
        ("💳", "مدير الديون", "إدارة الديون", "/debts"),
        ("💰", "مستشار الضرائب", "نصائح ضريبية", "/budgets"),
        ("📊", "خبير الاستثمار", "توصيات استثمارية", "/assets"),
        ("📋", "مخطط الميزانيات", "تخطيط الميزانيات", "/budgets"),
        ("👥", "محلل العملاء", "تحليل العملاء", "/customers"),
        ("📦", "محلل الموردين", "تحليل الموردين", "/suppliers"),
        ("🏭", "مدير المخزون", "إدارة المخزون", "/products"),
        ("💲", "خبير التسعير", "تسعير المنتجات", "/products"),
        ("🌍", "محلل الأسواق", "تحليل الأسواق", "/currencies"),
        ("💱", "مراقب العملات", "مراقبة العملات", "/currencies"),
        ("🚀", "مخطط النمو", "خطط النمو", "/accounts"),
        ("⚡", "محسن الكفاءة", "تحسين الكفاءة", "/bank"),
        ("📜", "مراقب الامتثال", "الامتثال القانوني", "/budgets"),
        ("🔍", "المدقق", "تدقيق تلقائي", "/accounts"),
        ("📄", "مولد التقارير", "توليد تقارير", "/invoices"),
        ("🔔", "منبه المخاطر", "تنبيهات فورية", "/debts"),
        ("💰", "مستشار الادخار", "نصائح ادخار", "/bank"),
        ("🦅", "العقل الفائق", "ذكاء شامل", "/"),
    ]
    content = '<h2 style="text-align:center;color:#00c8ff;font-size:2rem;">🧠 مركز الذكاء الاصطناعي - 25 عقل</h2>'
    content += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:15px;margin-top:20px;">'
    for icon, name, desc, link in ais:
        content += f'<a href="{link}" style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border-radius:15px;padding:25px;text-align:center;border:1px solid rgba(0,200,255,0.3);transition:all 0.3s;"><div style="font-size:3rem;">{icon}</div><h3 style="color:#00c8ff;margin:10px 0 5px;">{name}</h3><p style="color:#aaa;font-size:0.85rem;">{desc}</p></a>'
    content += '</div><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

# ========== 50 نظام مالي ==========
@app.route('/all_systems')
def all_systems():
    if 'user' not in session: return redirect('/login')
    systems = [
        ("/accounts", "📚", "الحسابات", "إدارة الحسابات العامة"),
        ("/customers", "👥", "العملاء", "إدارة العملاء"),
        ("/suppliers", "📦", "الموردون", "إدارة الموردين"),
        ("/invoices", "🧾", "الفواتير", "إدارة الفواتير"),
        ("/products", "📦", "المنتجات", "إدارة المنتجات"),
        ("/bank", "🏦", "البنك", "الحركات البنكية"),
        ("/zakat", "🕌", "الزكاة", "حساب الزكاة"),
        ("/debts", "💳", "الديون", "إدارة الديون"),
        ("/budgets", "📋", "الميزانيات", "إدارة الميزانيات"),
        ("/assets", "🏢", "الأصول", "إدارة الأصول"),
        ("/currencies", "💱", "العملات", "إدارة العملات"),
        ("/ai_center", "🧠", "الذكاء", "25 عقل ذكي"),
        ("/accounts", "📊", "ميزان المراجعة", "مراجعة الحسابات"),
        ("/invoices", "📈", "قائمة الدخل", "تحليل الدخل"),
        ("/bank", "💵", "التدفقات", "التدفقات النقدية"),
        ("/customers", "🎯", "تحليل العملاء", "تحليل العملاء"),
        ("/suppliers", "📋", "تحليل الموردين", "تحليل الموردين"),
        ("/products", "🏭", "المخزون", "إدارة المخزون"),
        ("/budgets", "📊", "الموازنات", "الموازنات التقديرية"),
        ("/debts", "📉", "تحليل الديون", "تحليل الديون"),
        ("/assets", "💰", "الاستثمارات", "إدارة الاستثمارات"),
        ("/currencies", "🌍", "الأسواق", "تحليل الأسواق"),
        ("/zakat", "🧮", "النصاب", "حساب النصاب"),
        ("/bank", "🔐", "التسويات", "التسويات البنكية"),
        ("/accounts", "📒", "الأستاذ", "دفتر الأستاذ"),
        ("/invoices", "📤", "المدفوعات", "إدارة المدفوعات"),
        ("/customers", "📥", "المقبوضات", "إدارة المقبوضات"),
        ("/suppliers", "📤", "المصروفات", "إدارة المصروفات"),
        ("/products", "📋", "القيود", "قيود اليومية"),
        ("/budgets", "🎯", "الأهداف", "الأهداف المالية"),
        ("/debts", "📊", "التحليلات", "التحليلات المالية"),
        ("/assets", "📈", "النمو", "متابعة النمو"),
        ("/currencies", "💱", "التحويل", "تحويل العملات"),
        ("/zakat", "🕌", "الزكاة الذكية", "زكاة ذكية"),
        ("/bank", "🏦", "البنك الذكي", "بنك ذكي"),
        ("/accounts", "📚", "الحسابات الذكية", "حسابات ذكية"),
        ("/customers", "👥", "العملاء الأذكياء", "عملاء أذكياء"),
        ("/suppliers", "📦", "الموردون الأذكياء", "موردون أذكياء"),
        ("/invoices", "🧾", "فواتير ذكية", "فواتير ذكية"),
        ("/products", "📦", "منتجات ذكية", "منتجات ذكية"),
        ("/all_systems", "📊", "كل الأنظمة", "عرض شامل"),
        ("/ai_center", "🧠", "العقول", "25 عقل"),
        ("/", "🦅", "الرئيسية", "اللوحة السحرية"),
        ("/login", "🔐", "الدخول", "تسجيل الدخول"),
        ("/logout", "🚪", "الخروج", "تسجيل الخروج"),
        ("/bank", "💳", "البطاقات", "إدارة البطاقات"),
        ("/debts", "📋", "القروض", "إدارة القروض"),
        ("/assets", "🏢", "الممتلكات", "إدارة الممتلكات"),
        ("/currencies", "🪙", "العملات الرقمية", "عملات رقمية"),
        ("/budgets", "📊", "التقارير", "التقارير المالية"),
    ]
    content = '<h2 style="text-align:center;color:#FFD700;font-size:2rem;">📊 جميع الأنظمة - 50 نظام</h2>'
    content += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:20px;">'
    for path, icon, name, desc in systems:
        content += f'<a href="{path}" style="background:#1a1a3e;border-radius:12px;padding:20px;text-align:center;border:1px solid rgba(255,215,0,0.2);"><div style="font-size:2rem;">{icon}</div><h3 style="color:#FFD700;font-size:0.9rem;margin:8px 0;">{name}</h3><p style="color:#888;font-size:0.75rem;">{desc}</p></a>'
    content += '</div><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

# ========== 10 أنظمة تطوير ذاتي ==========
@app.route('/self_dev')
def self_dev():
    if 'user' not in session: return redirect('/login')
    devs = [
        ("🧬", "التعلم الذاتي", "يتعلم من البيانات"),
        ("🔧", "الإصلاح الذاتي", "يكتشف الأخطاء"),
        ("📈", "التحسين الذاتي", "يحسن الأداء"),
        ("🔄", "التكيف الذاتي", "يتكيف مع المتغيرات"),
        ("🧠", "التفكير الذاتي", "يحلل القرارات"),
        ("💾", "الحفظ الذاتي", "يحفظ البيانات"),
        ("🔐", "الحماية الذاتية", "يحمي نفسه"),
        ("📊", "التقييم الذاتي", "يقيم أداءه"),
        ("🚀", "التطوير الذاتي", "يضيف ميزات"),
        ("🌟", "التطور الذاتي", "يتطور باستمرار"),
    ]
    content = '<h2 style="text-align:center;color:#4aff4a;font-size:2rem;">🧬 أنظمة التطوير الذاتي - 10 أنظمة</h2>'
    content += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:15px;margin-top:20px;">'
    for icon, name, desc in devs:
        content += f'<div style="background:linear-gradient(145deg,#1a3e1a,#0d2e0d);border-radius:15px;padding:25px;text-align:center;border:1px solid rgba(74,255,74,0.3);"><div style="font-size:2.5rem;">{icon}</div><h3 style="color:#4aff4a;margin:10px 0 5px;">{name}</h3><p style="color:#aaa;font-size:0.85rem;">{desc}</p></div>'
    content += '</div><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
