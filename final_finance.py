from flask import Flask, request, session, redirect, render_template_string
import sqlite3, hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'final_finance_2026'
DB = 'new_finance.db'

def init_db():
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
    <div style="background:#1a1a3e;padding:15px;border-radius:15px;margin-bottom:20px;">
        <a href="/">🏠 الرئيسية</a>
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
        <a href="/logout">🚪 خروج</a>
    </div>
    {{ content | safe }}
</body></html>
'''

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form.get('username', 'admin')
        return redirect('/')
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
        @keyframes float-btn {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-8px); }} }}
        @keyframes glow-gold {{ 0%,100% {{ box-shadow: 0 0 15px rgba(255,215,0,0.4); }} 50% {{ box-shadow: 0 0 35px rgba(255,215,0,0.8); }} }}
        @keyframes glow-blue {{ 0%,100% {{ box-shadow: 0 0 15px rgba(0,200,255,0.4); }} 50% {{ box-shadow: 0 0 35px rgba(0,200,255,0.8); }} }}
        @keyframes spin-icon {{ 0%,100% {{ transform: rotate(0deg); }} 50% {{ transform: rotate(10deg); }} }}
        h1 {{ text-align:center; font-size:2.5rem; background:linear-gradient(45deg,#FFD700,#FF8C00,#FFD700); -webkit-background-clip:text; -webkit-text-fill-color:transparent; animation:gradient-shift 3s ease infinite; }}
        @keyframes gradient-shift {{ 0% {{ background-position:0% 50%; }} 50% {{ background-position:100% 50%; }} 100% {{ background-position:0% 50%; }} }}
        .stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:15px; margin:30px 0; }}
        .stat {{ background:linear-gradient(145deg,#1a1a4e,#0d0d2e); border-radius:20px; padding:25px; text-align:center; border:2px solid #FFD700; animation:float-btn 3s ease-in-out infinite; }}
        .stat h2 {{ font-size:2rem; color:#FFD700; }}
        .nav-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:12px; margin-top:30px; }}
        .nav-btn {{ display:flex; flex-direction:column; align-items:center; gap:8px; padding:20px; border-radius:50%; width:100px; height:100px; justify-content:center; background:linear-gradient(145deg,#1a1a4e,#0d0d2e); text-decoration:none; font-size:0.75rem; transition:all 0.3s; animation:float-btn 3s ease-in-out infinite; }}
        .nav-btn:hover {{ transform: scale(1.15); }}
        .nav-btn span {{ font-size:2rem; animation:spin-icon 4s linear infinite; }}
        .btn-gold {{ border:2px solid #FFD700; color:#FFD700; animation:glow-gold 2s infinite; }}
        .btn-blue {{ border:2px solid #00c8ff; color:#00c8ff; animation:glow-blue 2s infinite; }}
        .btn-green {{ border:2px solid #4affb0; color:#4affb0; box-shadow:0 0 25px rgba(74,255,176,0.4); }}
    </style>
    <h1>🦅 لوحة نوح المالية</h1>
    <div class="stats">
        <div class="stat" style="animation-delay:0s;"><h2>{accounts}</h2>حسابات</div>
        <div class="stat" style="animation-delay:0.2s;"><h2>{customers}</h2>عملاء</div>
        <div class="stat" style="animation-delay:0.4s;"><h2>{invoices}</h2>فواتير</div>
        <div class="stat" style="animation-delay:0.6s;"><h2>{products}</h2>منتجات</div>
        <div class="stat" style="animation-delay:0.8s;"><h2>{bank}</h2>بنك</div>
        <div class="stat" style="animation-delay:1s;"><h2>{revenue}</h2>إيرادات</div>
    </div>
    <div class="nav-grid">
        <a href="/accounts" class="nav-btn btn-gold"><span>📚</span>الحسابات</a>
        <a href="/customers" class="nav-btn btn-blue"><span>👥</span>العملاء</a>
        <a href="/suppliers" class="nav-btn btn-green"><span>📦</span>الموردون</a>
        <a href="/invoices" class="nav-btn btn-gold"><span>🧾</span>الفواتير</a>
        <a href="/products" class="nav-btn btn-blue"><span>📦</span>المنتجات</a>
        <a href="/bank" class="nav-btn btn-green"><span>🏦</span>البنك</a>
        <a href="/zakat" class="nav-btn btn-gold"><span>🕌</span>الزكاة</a>
        <a href="/debts" class="nav-btn btn-blue"><span>💳</span>الديون</a>
        <a href="/budgets" class="nav-btn btn-green"><span>📋</span>الميزانيات</a>
        <a href="/assets" class="nav-btn btn-gold"><span>🏢</span>الأصول</a>
        <a href="/currencies" class="nav-btn btn-blue"><span>💱</span>العملات</a>
        <a href="/logout" class="nav-btn btn-green"><span>🚪</span>خروج</a>
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
