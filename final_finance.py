from flask import Flask, request, session, redirect, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'final_finance_2026'
DB = 'new_finance.db'

def init_db()

def add_sample_data():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM accounts")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO accounts (name, type, balance) VALUES ('النقدية','أصول',50000)")
        c.execute("INSERT INTO accounts (name, type, balance) VALUES ('البنك','أصول',150000)")
        c.execute("INSERT INTO accounts (name, type, balance) VALUES ('المبيعات','إيرادات',200000)")
        c.execute("INSERT INTO accounts (name, type, balance) VALUES ('المشتريات','مصاريف',80000)")
        c.execute("INSERT INTO customers (name, phone) VALUES ('شركة الأمل','0501234567')")
        c.execute("INSERT INTO customers (name, phone) VALUES ('مؤسسة النور','0507654321')")
        c.execute("INSERT INTO customers (name, phone) VALUES ('شركة المستقبل','0509876543')")
        c.execute("INSERT INTO products (name, price, stock) VALUES ('منتج أ',100,50)")
        c.execute("INSERT INTO products (name, price, stock) VALUES ('منتج ب',200,30)")
        c.execute("INSERT INTO products (name, price, stock) VALUES ('منتج ج',300,20)")
        c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (1,15000,'2026-08-01')")
        c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (2,25000,'2026-08-05')")
        c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (3,10000,'2026-08-10')")
        c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES ('2026-08-01','إيداع',50000)")
        c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES ('2026-08-05','إيداع مبيعات',35000)")
        c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES ('2026-08-10','سحب',-15000)")
        conn.commit()
    conn.close()

add_sample_data():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, name TEXT, type TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS suppliers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER);
    CREATE TABLE IF NOT EXISTS bank_moves (id INTEGER PRIMARY KEY, date TEXT, desc TEXT, amount REAL);
    CREATE TABLE IF NOT EXISTS zakat (id INTEGER PRIMARY KEY, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS debts (id INTEGER PRIMARY KEY, name TEXT, amount REAL, type TEXT);
    CREATE TABLE IF NOT EXISTS budgets (id INTEGER PRIMARY KEY, name TEXT, amount REAL);
    CREATE TABLE IF NOT EXISTS assets (id INTEGER PRIMARY KEY, name TEXT, value REAL);
    CREATE TABLE IF NOT EXISTS currencies (id INTEGER PRIMARY KEY, code TEXT, rate REAL);
    ''')
    conn.commit()
    conn.close()

init_db()

PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>🦅 نوح المالي</title>
<style>
    body { font-family:Tahoma; background:#0a0a2e; color:#fff; padding:20px; }
    a { color:#FFD700; text-decoration:none; margin:5px; }
    input, select, button { padding:10px; margin:5px; background:#222; color:#fff; border:1px solid #FFD700; border-radius:8px; }
    button { background:#FFD700; color:#000; font-weight:bold; cursor:pointer; }
    table { width:100%; border-collapse:collapse; margin-top:15px; }
    th, td { border:1px solid #444; padding:10px; text-align:center; }
    th { background:#1a1a3e; color:#FFD700; }
</style></head>
<body>
    {{ content | safe }}
</body></html>
'''

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form.get('username', 'admin')
        return redirect('/dashboard')
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>🦅 دخول نوح المالي</title>
    <style>
        body { font-family:Tahoma; background:#0a0a2e; color:#fff; display:flex; justify-content:center; align-items:center; height:100vh; }
        .box { background:#1a1a3e; padding:40px; border-radius:25px; border:2px solid #FFD700; text-align:center; }
        h2 { color:#FFD700; }
        input { display:block; width:100%; padding:12px; margin:10px 0; background:#222; border:1px solid #FFD700; color:#fff; border-radius:10px; }
        button { width:100%; padding:12px; background:#FFD700; border:none; border-radius:10px; font-weight:bold; }
    </style></head>
    <body><div class="box"><h2>🦅 نوح المالي</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="المستخدم">
        <input type="password" name="password" placeholder="كلمة المرور">
        <button>🚀 دخول</button>
    </form></div></body></html>''')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/')
def home():
    if 'user' not in session: return redirect('/login')
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM accounts"); accounts = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM invoices"); invoices = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products"); products = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM bank_moves"); bank = c.fetchone()[0]
    conn.close()
    content = f"""
    <style>
        @keyframes bg-shift {{ 0% {{ background-position:0% 50%; }} 50% {{ background-position:100% 50%; }} 100% {{ background-position:0% 50%; }} }}
        @keyframes float-card {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-10px); }} }}
        @keyframes glow-gold {{ 0%,100% {{ box-shadow:0 0 15px rgba(255,215,0,0.4); }} 50% {{ box-shadow:0 0 35px rgba(255,215,0,0.9); }} }}
        @keyframes glow-blue {{ 0%,100% {{ box-shadow:0 0 15px rgba(0,200,255,0.4); }} 50% {{ box-shadow:0 0 35px rgba(0,200,255,0.9); }} }}
        @keyframes glow-green {{ 0%,100% {{ box-shadow:0 0 15px rgba(74,255,176,0.4); }} 50% {{ box-shadow:0 0 35px rgba(74,255,176,0.9); }} }}
        @keyframes pulse-bar {{ 0%,100% {{ filter:brightness(1); }} 50% {{ filter:brightness(1.5); }} }}
        @keyframes subtitle-glow {{ 0%,100% {{ text-shadow:0 0 10px rgba(255,215,0,0.5); }} 50% {{ text-shadow:0 0 30px rgba(255,215,0,0.9), 0 0 50px rgba(0,200,255,0.5); }} }}
        @keyframes spin-icon {{ 0%,100% {{ transform:rotate(0deg); }} 50% {{ transform:rotate(12deg); }} }}
        @keyframes gradient-shift {{ 0% {{ background-position:0% 50%; }} 50% {{ background-position:100% 50%; }} 100% {{ background-position:0% 50%; }} }}
        h1 {{
            text-shadow: 0 0 30px rgba(255,215,0,0.6), 0 0 60px rgba(255,140,0,0.4);
            text-align:center; font-size:2.5rem;
            background:linear-gradient(45deg,#FFD700,#FF8C00,#FFD700);
            background-size:300% 300%;
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            animation:gradient-shift 3s ease infinite;
        }}
        .stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:15px; margin:30px 0; }}
        .stat {{
            background:linear-gradient(145deg,#1a1a4e,#0d0d2e); border-radius:20px;
            padding:25px; text-align:center; border:2px solid #FFD700;
            animation:float-card 3s ease-in-out infinite;
        }}
        .stat:nth-child(1) {{ animation-delay:0s; border-color:#FFD700; animation:glow-gold 2s infinite, float-card 3s ease-in-out infinite; }}
        .stat:nth-child(2) {{ animation-delay:0.2s; border-color:#00c8ff; animation:glow-blue 2s infinite, float-card 3s ease-in-out infinite; }}
        .stat:nth-child(3) {{ animation-delay:0.4s; border-color:#4affb0; animation:glow-green 2s infinite, float-card 3s ease-in-out infinite; }}
        .stat:nth-child(4) {{ animation-delay:0.6s; border-color:#FFD700; animation:glow-gold 2s infinite, float-card 3s ease-in-out infinite; }}
        .stat:nth-child(5) {{ animation-delay:0.8s; border-color:#00c8ff; animation:glow-blue 2s infinite, float-card 3s ease-in-out infinite; }}
        .stat:nth-child(6) {{ animation-delay:1s; border-color:#4affb0; animation:glow-green 2s infinite, float-card 3s ease-in-out infinite; }}
        .stat h2 {{ font-size:2rem; }}
        .nav {{ display:flex; flex-wrap:wrap; gap:10px; justify-content:center; margin-top:30px; }}
        .nav a {{
            background:linear-gradient(145deg,#1a1a4e,#0d0d2e); padding:15px 25px;
            border-radius:25px; text-decoration:none; font-weight:bold;
            transition:all 0.3s;
        }}
        .nav a:hover {{ transform:scale(1.1); }}
        .nav a span {{ display:inline-block; animation:spin-icon 4s linear infinite; }}
    </style>
    <div class="magic-particles"></div>
    <div class="stars"></div>
    <h1>🦅 لوحة نوح المالية</h1>
    <p style="text-align:center;color:#aaa;">النظام المالي الأسطوري المتكامل</p>
    <style>
        .magic-particles, .stars {{ position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:0; }}
        .particle {{ position:absolute; border-radius:50%; animation:float-particle linear infinite; }}
        .star {{ position:absolute; border-radius:50%; background:#fff; animation:twinkle ease-in-out infinite; }}
        @keyframes float-particle {{ 0% {{ transform:translateY(100vh) scale(0); opacity:0; }} 10% {{ opacity:1; }} 90% {{ opacity:1; }} 100% {{ transform:translateY(-10vh) scale(1); opacity:0; }} }}
        @keyframes twinkle {{ 0%,100% {{ opacity:0.3; }} 50% {{ opacity:1; transform:scale(1.5); }} }}
        .stats, .nav {{ position:relative; z-index:1; }}
    </style>
    <script>
        for (let i = 0; i < 30; i++) {{
            const p = document.createElement('div');
            p.classList.add('particle');
            p.style.left = Math.random() * 100 + '%';
            p.style.width = Math.random() * 6 + 3 + 'px';
            p.style.height = p.style.width;
            p.style.background = ['#FFD700','#00c8ff','#4affb0','#ff4a4a'][Math.floor(Math.random()*4)];
            p.style.animationDuration = Math.random() * 8 + 4 + 's';
            p.style.animationDelay = Math.random() * 8 + 's';
            document.querySelector('.magic-particles').appendChild(p);
        }}
        for (let i = 0; i < 50; i++) {{
            const s = document.createElement('div');
            s.classList.add('star');
            s.style.left = Math.random() * 100 + '%';
            s.style.top = Math.random() * 100 + '%';
            s.style.width = Math.random() * 3 + 1 + 'px';
            s.style.height = s.style.width;
            s.style.animationDuration = Math.random() * 3 + 1 + 's';
            s.style.animationDelay = Math.random() * 5 + 's';
            document.querySelector('.stars').appendChild(s);
        }}
    </script>
    <p style="text-align:center;color:#aaa;">النظام المالي الأسطوري المتكامل</p>
    <div style="text-align:center;margin:20px 0;color:#FFD700;font-size:1.2rem;" id="clock"></div>
    <script>
        function updateClock() {{
            const now = new Date();
            document.getElementById('clock').textContent = now.toLocaleDateString('ar') + ' - ' + now.toLocaleTimeString('ar');
        }}
        updateClock();
        setInterval(updateClock, 1000);
    </script>
    <div class="stats">
        <div class="stat"><h2 style="color:#FFD700;">{accounts}</h2>حسابات</div>
        <div class="stat"><h2 style="color:#00c8ff;">{customers}</h2>عملاء</div>
        <div class="stat"><h2 style="color:#4affb0;">{invoices}</h2>فواتير</div>
        <div class="stat"><h2 style="color:#FFD700;">{products}</h2>منتجات</div>
        <div class="stat"><h2 style="color:#00c8ff;">{bank}</h2>بنك</div>
        <div class="stat"><h2 style="color:#4affb0;">{revenue}</h2>إيرادات</div>
    </div>
    <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border-radius:20px;padding:25px;margin:20px 0;text-align:center;border:2px solid #FFD700;position:relative;z-index:1;">
        <h3 style="color:#FFD700;">📊 أداء الإيرادات</h3>
        <div style="background:#222;border-radius:15px;height:25px;margin-top:15px;overflow:hidden;">
            <div style="background:linear-gradient(90deg,#FFD700,#FF8C00);height:100%;width:80%;border-radius:15px;animation:pulse-bar 2s ease-in-out infinite;"></div>
        </div>
        <p style="color:#aaa;margin-top:10px;">80% من الهدف</p>
    </div>
    <div class="nav">
        <a href="/accounts" style="border:2px solid #FFD700;color:#FFD700;"><span>📚</span> الحسابات</a>
        <a href="/customers" style="border:2px solid #00c8ff;color:#00c8ff;"><span>👥</span> العملاء</a>
        <a href="/suppliers" style="border:2px solid #4affb0;color:#4affb0;"><span>📦</span> الموردون</a>
        <a href="/invoices" style="border:2px solid #FFD700;color:#FFD700;"><span>🧾</span> الفواتير</a>
        <a href="/products" style="border:2px solid #00c8ff;color:#00c8ff;"><span>📦</span> المنتجات</a>
        <a href="/bank" style="border:2px solid #4affb0;color:#4affb0;"><span>🏦</span> البنك</a>
        <a href="/zakat" style="border:2px solid #FFD700;color:#FFD700;"><span>🕌</span> الزكاة</a>
        <a href="/debts" style="border:2px solid #00c8ff;color:#00c8ff;"><span>💳</span> الديون</a>
        <a href="/budgets" style="border:2px solid #4affb0;color:#4affb0;"><span>📋</span> الميزانيات</a>
        <a href="/assets" style="border:2px solid #FFD700;color:#FFD700;"><span>🏢</span> الأصول</a>
        <a href="/currencies" style="border:2px solid #00c8ff;color:#00c8ff;"><span>💱</span> العملات</a>
        <a href="/advanced_reports" style="border:2px solid #4affb0;color:#4affb0;"><span>📊</span> تقارير</a>
        <a href="/smart_analysis" style="border:2px solid #FFD700;color:#FFD700;"><span>🧠</span> تحليل</a>
        <a href="/currency_converter" style="border:2px solid #00c8ff;color:#00c8ff;"><span>💱</span> محول</a>
        <a href="/kpis" style="border:2px solid #4affb0;color:#4affb0;"><span>🎯</span> مؤشرات</a>
        <a href="/logout" style="border:2px solid #ff4a4a;color:#ff4a4a;"><span>🚪</span> خروج</a>
    </div>"""
    return render_template_string(PAGE, content=content)

@app.route('/accounts', methods=['GET','POST'])
def accounts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO accounts (name, type) VALUES (?,?)", (request.form['name'], request.form['type']))
        conn.commit()
    c.execute("SELECT * FROM accounts")
    rows = c.fetchall(); conn.close()
    content = "<h2>📚 الحسابات</h2><form method='POST'><input name='name' placeholder='اسم الحساب' required><select name='type'><option>أصول</option><option>خصوم</option><option>إيرادات</option><option>مصاريف</option></select><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>النوع</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/customers', methods=['GET','POST'])
def customers():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO customers (name, phone) VALUES (?,?)", (request.form['name'], request.form.get('phone','')))
        conn.commit()
    c.execute("SELECT * FROM customers")
    rows = c.fetchall(); conn.close()
    content = "<h2>👥 العملاء</h2><form method='POST'><input name='name' placeholder='اسم العميل' required><input name='phone' placeholder='الهاتف'><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>الهاتف</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/suppliers', methods=['GET','POST'])
def suppliers():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO suppliers (name, phone) VALUES (?,?)", (request.form['name'], request.form.get('phone','')))
        conn.commit()
    c.execute("SELECT * FROM suppliers")
    rows = c.fetchall(); conn.close()
    content = "<h2>📦 الموردون</h2><form method='POST'><input name='name' placeholder='اسم المورد' required><input name='phone' placeholder='الهاتف'><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>الهاتف</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/invoices', methods=['GET','POST'])
def invoices():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (?,?,?)", (request.form['customer_id'], request.form['amount'], request.form['date']))
        conn.commit()
    c.execute("SELECT * FROM invoices")
    rows = c.fetchall(); conn.close()
    content = "<h2>🧾 الفواتير</h2><form method='POST'><input name='customer_id' placeholder='رقم العميل' required><input name='amount' placeholder='المبلغ' required><input name='date' type='date' required><button>إصدار</button></form><table><tr><th>ID</th><th>العميل</th><th>المبلغ</th><th>التاريخ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/products', methods=['GET','POST'])
def products():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO products (name, price, stock) VALUES (?,?,?)", (request.form['name'], request.form['price'], request.form['stock']))
        conn.commit()
    c.execute("SELECT * FROM products")
    rows = c.fetchall(); conn.close()
    content = "<h2>📦 المنتجات</h2><form method='POST'><input name='name' placeholder='اسم المنتج' required><input name='price' placeholder='السعر' required><input name='stock' placeholder='المخزون' required><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>السعر</th><th>المخزون</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/bank', methods=['GET','POST'])
def bank():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES (?,?,?)", (request.form['date'], request.form['desc'], request.form['amount']))
        conn.commit()
    c.execute("SELECT * FROM bank_moves")
    rows = c.fetchall()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves")
    balance = c.fetchone()[0]
    conn.close()
    content = f"<h2>🏦 البنك</h2><p style='font-size:1.5rem;color:#FFD700;'>الرصيد: {balance}</p><form method='POST'><input name='date' type='date' required><input name='desc' placeholder='الوصف' required><input name='amount' placeholder='المبلغ' required><button>إضافة</button></form><table><tr><th>ID</th><th>التاريخ</th><th>الوصف</th><th>المبلغ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

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
    content = f"<h2>🕌 الزكاة</h2><p>💰 النقود: {total}</p><p>📏 النصاب: {nisab}</p><p style='color:#FFD700;font-size:1.5rem;'>🧮 المستحقة: {due:.2f}</p><form method='POST'><input name='amount' placeholder='مبلغ' required><input name='date' type='date' required><button>تسجيل</button></form><table><tr><th>ID</th><th>مبلغ</th><th>تاريخ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/debts', methods=['GET','POST'])
def debts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO debts (name, amount, type) VALUES (?,?,?)", (request.form['name'], request.form['amount'], request.form['type']))
        conn.commit()
    c.execute("SELECT * FROM debts")
    rows = c.fetchall(); conn.close()
    content = "<h2>💳 الديون</h2><form method='POST'><input name='name' placeholder='اسم' required><input name='amount' placeholder='مبلغ' required><select name='type'><option>علينا</option><option>لنا</option></select><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>مبلغ</th><th>نوع</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/budgets', methods=['GET','POST'])
def budgets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO budgets (name, amount) VALUES (?,?)", (request.form['name'], request.form['amount']))
        conn.commit()
    c.execute("SELECT * FROM budgets")
    rows = c.fetchall(); conn.close()
    content = "<h2>📋 الميزانيات</h2><form method='POST'><input name='name' placeholder='اسم' required><input name='amount' placeholder='مبلغ' required><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>المبلغ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/assets', methods=['GET','POST'])
def assets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO assets (name, value) VALUES (?,?)", (request.form['name'], request.form['value']))
        conn.commit()
    c.execute("SELECT * FROM assets")
    rows = c.fetchall(); conn.close()
    content = "<h2>🏢 الأصول</h2><form method='POST'><input name='name' placeholder='اسم الأصل' required><input name='value' placeholder='القيمة' required><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>القيمة</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/currencies', methods=['GET','POST'])
def currencies():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO currencies (code, rate) VALUES (?,?)", (request.form['code'], request.form['rate']))
        conn.commit()
    c.execute("SELECT * FROM currencies")
    rows = c.fetchall(); conn.close()
    content = "<h2>💱 العملات</h2><form method='POST'><input name='code' placeholder='رمز' required><input name='rate' placeholder='سعر' required><button>إضافة</button></form><table><tr><th>ID</th><th>رمز</th><th>سعر</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

@app.route('/advanced_reports')
def advanced_reports():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0"); inflow = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0"); outflow = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(balance),0) FROM accounts WHERE type='أصول'"); assets = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(balance),0) FROM accounts WHERE type='خصوم'"); liabilities = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM debts WHERE type='علينا'"); our_debts = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM debts WHERE type='لنا'"); their_debts = c.fetchone()[0]
    conn.close()
    net_cash = inflow + outflow
    equity = assets - liabilities
    content = f'''
    <h2 style="text-align:center;color:#FFD700;">📊 التقارير المتقدمة</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;margin-top:20px;">
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:15px;text-align:center;border:2px solid #FFD700;"><h3>💰 الإيرادات</h3><p style="font-size:2rem;color:#FFD700;">{revenue}</p></div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:15px;text-align:center;border:2px solid #00c8ff;"><h3>💵 صافي التدفق</h3><p style="font-size:2rem;color:#00c8ff;">{net_cash}</p></div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:15px;text-align:center;border:2px solid #4affb0;"><h3>🏢 الأصول</h3><p style="font-size:2rem;color:#4affb0;">{assets}</p></div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:15px;text-align:center;border:2px solid #ff4a4a;"><h3>📉 الخصوم</h3><p style="font-size:2rem;color:#ff4a4a;">{liabilities}</p></div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:15px;text-align:center;border:2px solid #FFD700;"><h3>📊 حقوق الملكية</h3><p style="font-size:2rem;color:#FFD700;">{equity}</p></div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:15px;text-align:center;border:2px solid #00c8ff;"><h3>💳 ديون علينا</h3><p style="font-size:2rem;color:#00c8ff;">{our_debts}</p></div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:15px;text-align:center;border:2px solid #4affb0;"><h3>💳 ديون لنا</h3><p style="font-size:2rem;color:#4affb0;">{their_debts}</p></div>
    </div>'''
    return render_template_string(PAGE, content=content)

@app.route('/smart_analysis')
def smart_analysis():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0"); expenses = abs(c.fetchone()[0])
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products"); products = c.fetchone()[0]
    conn.close()
    profit = revenue - expenses
    margin = (profit / revenue * 100) if revenue > 0 else 0
    insights = []
    if margin > 30: insights.append("✅ ربحية ممتازة!")
    elif margin > 10: insights.append("📊 ربحية جيدة، يمكن تحسينها")
    else: insights.append("⚠️ ربحية منخفضة")
    if customers >= 5: insights.append("👥 قاعدة عملاء قوية")
    else: insights.append("📈 تحتاج المزيد من العملاء")
    if products >= 5: insights.append("📦 تنوع منتجات جيد")
    else: insights.append("📦 أضف منتجات جديدة")
    content = f'''
    <h2 style="text-align:center;color:#00c8ff;">🧠 التحليل الذكي</h2>
    <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:30px;border-radius:20px;margin-top:20px;text-align:center;border:2px solid #00c8ff;">
        <h3 style="color:#00c8ff;">هامش الربح</h3>
        <p style="font-size:3rem;color:#FFD700;">{margin:.1f}%</p>
    </div>
    <div style="margin-top:20px;">'''
    for i in insights:
        content += f'<div style="background:#1a1a4e;padding:15px;border-radius:10px;margin:10px 0;border-right:4px solid #FFD700;">{i}</div>'
    content += "</div>"
    return render_template_string(PAGE, content=content)

@app.route('/currency_converter', methods=['GET','POST'])
def currency_converter():
    if 'user' not in session: return redirect('/login')
    result = None
    if request.method == 'POST':
        amount = float(request.form['amount'])
        from_rate = float(request.form.get('from_rate', 1))
        to_rate = float(request.form.get('to_rate', 1))
        result = amount * (to_rate / from_rate)
    content = '''
    <h2 style="text-align:center;color:#00c8ff;">💱 محول العملات</h2>
    <form method="POST" style="text-align:center;margin-top:20px;">
        <input name="amount" placeholder="المبلغ" required>
        <input name="from_rate" placeholder="سعر العملة من" value="1">
        <input name="to_rate" placeholder="سعر العملة إلى" value="1">
        <button>تحويل</button>
    </form>'''
    if result is not None:
        content += f'<p style="text-align:center;font-size:2rem;color:#FFD700;margin-top:20px;">✅ {result:.2f}</p>'
    return render_template_string(PAGE, content=content)

@app.route('/kpis')
def kpis():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0"); expenses = abs(c.fetchone()[0])
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products"); products = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves"); cash = c.fetchone()[0]
    conn.close()
    profit = revenue - expenses
    margin = (profit / revenue * 100) if revenue > 0 else 0
    content = f'''
    <h2 style="text-align:center;color:#4affb0;">🎯 مؤشرات الأداء</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin-top:20px;">
        <div style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #FFD700;"><h3>هامش الربح</h3><p style="font-size:2rem;color:#FFD700;">{margin:.1f}%</p></div>
        <div style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #00c8ff;"><h3>العملاء</h3><p style="font-size:2rem;color:#00c8ff;">{customers}</p></div>
        <div style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #4affb0;"><h3>المنتجات</h3><p style="font-size:2rem;color:#4affb0;">{products}</p></div>
        <div style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #FFD700;"><h3>النقد</h3><p style="font-size:2rem;color:#FFD700;">{cash}</p></div>
    </div>'''
    return render_template_string(PAGE, content=content)
