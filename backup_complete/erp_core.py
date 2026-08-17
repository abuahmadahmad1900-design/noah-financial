from flask import Flask, request, session, redirect, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'erp_supreme_2026'
DB = 'erp.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, name TEXT, type TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT);
    CREATE TABLE IF NOT EXISTS suppliers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT);
    CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER);
    CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, salary REAL);
    CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT, budget REAL, status TEXT);
    CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, project_id INTEGER, title TEXT, status TEXT);
    ''')
    conn.commit()
    conn.close()

init_db()

PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>ERP نوح</title>
<style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { font-family:Tahoma; background:linear-gradient(135deg,#0a0a2e,#1a0a3e,#0a1a2e); background-size:400% 400%; animation:bg-shift 8s ease infinite; color:#fff; padding:20px; }
    @keyframes glow-gold { 0% { box-shadow:0 0 10px rgba(255,215,0,0.4); } 100% { box-shadow:0 0 30px rgba(255,215,0,0.9); } }
    @keyframes glow-blue { 0% { box-shadow:0 0 10px rgba(0,200,255,0.4); } 100% { box-shadow:0 0 30px rgba(0,200,255,0.9); } }
    @keyframes glow-green { 0% { box-shadow:0 0 10px rgba(74,255,176,0.4); } 100% { box-shadow:0 0 30px rgba(74,255,176,0.9); } }
    @keyframes glow-gold { 0% { box-shadow:0 0 10px rgba(255,215,0,0.4); } 100% { box-shadow:0 0 30px rgba(255,215,0,0.9); } }
    @keyframes glow-blue { 0% { box-shadow:0 0 10px rgba(0,200,255,0.4); } 100% { box-shadow:0 0 30px rgba(0,200,255,0.9); } }
    @keyframes glow-green { 0% { box-shadow:0 0 10px rgba(74,255,176,0.4); } 100% { box-shadow:0 0 30px rgba(74,255,176,0.9); } }
    @keyframes bg-shift { 0% { background-position:0% 50%; } 50% { background-position:100% 50%; } 100% { background-position:0% 50%; } }
    a { color:#FFD700; text-decoration:none; margin:5px; }
    table { width:100%; border-collapse:separate; border-spacing:0; margin-top:25px; border-radius:25px; overflow:hidden; box-shadow:0 25px 60px rgba(0,0,0,0.7), 0 0 40px rgba(255,215,0,0.15); background:linear-gradient(180deg,rgba(20,20,60,0.9),rgba(10,10,30,0.9)); }
    table th { background:linear-gradient(145deg,#FFD700,#FF8C00); color:#000; padding:20px; font-size:1.1rem; }
    table td { padding:15px; text-align:center; color:#f0f0f0; border-bottom:1px solid rgba(255,215,0,0.1); transition:all 0.3s; }
    table tr:nth-child(odd) td { background:rgba(255,255,255,0.02); }
    table tr:nth-child(even) td { background:rgba(0,200,255,0.02); }
    table tr:hover td { background:rgba(255,215,0,0.1); color:#FFD700; }
    th { background:linear-gradient(145deg,#FFD700,#FF8C00); color:#000; padding:15px; }
    td { padding:12px; border-bottom:1px solid rgba(255,215,0,0.1); text-align:center; }
    tr:hover td { background:rgba(255,215,0,0.08); }
    input, select, button { padding:10px; margin:5px; background:#1a1a3e; color:#fff; border:1px solid #FFD700; border-radius:8px; }
    button { background:#FFD700; color:#000; font-weight:bold; cursor:pointer; }
</style></head>
<body>
{{ content | safe }}
</body></html>'''

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form.get('username', 'admin')
        return redirect('/dashboard')
    return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>دخول ERP نوح</title>
    <style>
        body { font-family:Tahoma; background:linear-gradient(135deg,#0a0a2e,#1a0a3e); color:#fff; display:flex; justify-content:center; align-items:center; height:100vh; }
        .box { background:rgba(20,20,50,0.9); padding:50px; border-radius:30px; border:2px solid #FFD700; text-align:center; box-shadow:0 0 50px rgba(255,215,0,0.4); animation:glow 3s infinite alternate; }
        @keyframes glow { from { box-shadow:0 0 30px rgba(255,215,0,0.3); } to { box-shadow:0 0 70px rgba(255,215,0,0.8); } }
        h2 { color:#FFD700; font-size:2rem; margin-bottom:20px; }
        input { display:block; width:100%; padding:15px; margin:15px 0; background:#1a1a3e; border:2px solid #FFD700; border-radius:15px; color:#fff; font-size:1rem; }
        button { width:100%; padding:15px; background:linear-gradient(45deg,#FFD700,#FF8C00); border:none; border-radius:15px; font-weight:bold; font-size:1.1rem; cursor:pointer; }
    </style></head>
    <body><div class="box">
        <h2>🦅 ERP نوح</h2>
        <p style="color:#aaa;margin-bottom:20px;">نظام إدارة الموارد الأسطوري</p>
        <form method="POST">
            <input type="text" name="username" placeholder="المستخدم">
            <input type="password" name="password" placeholder="كلمة المرور">
            <button>🚀 دخول</button>
        </form>
    </div></body></html>'''

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
    c.execute("SELECT COUNT(*) FROM products"); products = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM employees"); employees = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM projects"); projects = c.fetchone()[0]
    conn.close()
    content = f'''
    <h1 style="text-align:center;font-size:2.5rem;color:#FFD700;text-shadow:0 0 30px rgba(255,215,0,0.6);">🦅 لوحة ERP الشاملة</h1>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:15px;margin:30px 0;">
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #FFD700;border-radius:20px;"><h2 style="font-size:2rem;color:#FFD700;">{accounts}</h2>حسابات</div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #00c8ff;border-radius:20px;"><h2 style="font-size:2rem;color:#00c8ff;">{customers}</h2>عملاء</div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #4affb0;border-radius:20px;"><h2 style="font-size:2rem;color:#4affb0;">{products}</h2>منتجات</div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #FFD700;border-radius:20px;"><h2 style="font-size:2rem;color:#FFD700;">{employees}</h2>موظفون</div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #00c8ff;border-radius:20px;"><h2 style="font-size:2rem;color:#00c8ff;">{projects}</h2>مشاريع</div>
    </div>
    <div style="text-align:center;margin-top:20px;">
        <a href="/accounts" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;animation:glow-gold 2s infinite alternate;">📊 الحسابات</a>
        <a href="/customers" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;animation:glow-blue 2s infinite alternate;">👥 العملاء</a>
        <a href="/products" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;animation:glow-green 2s infinite alternate;">📦 المنتجات</a>
        <a href="/employees" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">👷 الموظفون</a>
        <a href="/projects" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">📁 المشاريع</a>
        <a href="/suppliers" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;animation:glow-green 2s infinite alternate;">📦 الموردون</a>
        <a href="/invoices" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;animation:glow-gold 2s infinite alternate;">🧾 الفواتير</a>
        <a href="/tasks" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;animation:glow-blue 2s infinite alternate;">📝 المهام</a>
        <a href="/reports" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;animation:glow-gold 2s infinite alternate;">📊 تقارير</a>
        <a href="/analytics" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;animation:glow-blue 2s infinite alternate;">📈 تحليلات</a>
        <a href="/executive" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;animation:glow-green 2s infinite alternate;">👑 تنفيذية</a>
        <a href="/ai_center" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;animation:glow-blue 2s infinite alternate;">🧠 الذكاء</a>
        <a href="/security" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #ff4a4a;color:#ff4a4a;margin:5px;">🛡️ الحماية</a>
        <a href="/development" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;animation:glow-green 2s infinite alternate;">🧬 التطوير</a>
        <a href="/charts" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;animation:glow-gold 2s infinite alternate;">📊 رسوم</a>
        <a href="/export" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;animation:glow-blue 2s infinite alternate;">📥 تصدير</a>
        <a href="/search" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;animation:glow-blue 2s infinite alternate;">🔍 بحث</a>
        <a href="/notifications" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;animation:glow-gold 2s infinite alternate;">🔔 إشعارات</a>
        <a href="/backup" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;animation:glow-green 2s infinite alternate;">💾 نسخ</a>
        <a href="/sales" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">🛒 مبيعات</a>
        <a href="/purchases" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">🛍️ مشتريات</a>
        <a href="/payroll" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;">💼 رواتب</a>
        <a href="/logout" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #ff4a4a;color:#ff4a4a;margin:5px;">🚪 خروج</a>
    </div>'''
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
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📊 الحسابات</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <form method="GET" action="/accounts" style="text-align:center;margin:10px 0;"><input type="text" name="q" placeholder="ابحث..." style="padding:10px;border-radius:20px;border:2px solid #00c8ff;background:#1a1a3e;color:#fff;width:300px;"><button style="padding:10px 20px;border-radius:20px;border:none;background:#00c8ff;color:#000;font-weight:bold;">بحث</button></form>
    <form method="POST" style="text-align:center;"><input name="name" placeholder="اسم الحساب" required><select name="type"><option>أصول</option><option>خصوم</option><option>إيرادات</option><option>مصاريف</option></select><button>إضافة</button></form>
    <table><tr><th>ID</th><th>الاسم</th><th>النوع</th><th>الرصيد</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
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
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">👥 العملاء</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <form method="GET" action="/accounts" style="text-align:center;margin:10px 0;"><input type="text" name="q" placeholder="ابحث..." style="padding:10px;border-radius:20px;border:2px solid #00c8ff;background:#1a1a3e;color:#fff;width:300px;"><button style="padding:10px 20px;border-radius:20px;border:none;background:#00c8ff;color:#000;font-weight:bold;">بحث</button></form>
    <form method="POST" style="text-align:center;"><input name="name" placeholder="اسم العميل" required><input name="phone" placeholder="الهاتف"><button>إضافة</button></form>
    <table><tr><th>ID</th><th>الاسم</th><th>الهاتف</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
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
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">📦 المنتجات</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <form method="GET" action="/accounts" style="text-align:center;margin:10px 0;"><input type="text" name="q" placeholder="ابحث..." style="padding:10px;border-radius:20px;border:2px solid #00c8ff;background:#1a1a3e;color:#fff;width:300px;"><button style="padding:10px 20px;border-radius:20px;border:none;background:#00c8ff;color:#000;font-weight:bold;">بحث</button></form>
    <form method="POST" style="text-align:center;"><input name="name" placeholder="اسم المنتج" required><input name="price" placeholder="السعر" required><input name="stock" placeholder="المخزون" required><button>إضافة</button></form>
    <table><tr><th>ID</th><th>الاسم</th><th>السعر</th><th>المخزون</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/employees', methods=['GET','POST'])
def employees():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO employees (name, salary) VALUES (?,?)", (request.form['name'], request.form['salary']))
        conn.commit()
    c.execute("SELECT * FROM employees")
    rows = c.fetchall(); conn.close()
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">👷 الموظفون</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <form method="GET" action="/accounts" style="text-align:center;margin:10px 0;"><input type="text" name="q" placeholder="ابحث..." style="padding:10px;border-radius:20px;border:2px solid #00c8ff;background:#1a1a3e;color:#fff;width:300px;"><button style="padding:10px 20px;border-radius:20px;border:none;background:#00c8ff;color:#000;font-weight:bold;">بحث</button></form>
    <form method="POST" style="text-align:center;"><input name="name" placeholder="اسم الموظف" required><input name="salary" placeholder="الراتب" required><button>إضافة</button></form>
    <table><tr><th>ID</th><th>الاسم</th><th>الراتب</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/projects', methods=['GET','POST'])
def projects():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO projects (name, budget, status) VALUES (?,?,?)", (request.form['name'], request.form['budget'], 'نشط'))
        conn.commit()
    c.execute("SELECT * FROM projects")
    rows = c.fetchall(); conn.close()
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">📁 المشاريع</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <form method="GET" action="/accounts" style="text-align:center;margin:10px 0;"><input type="text" name="q" placeholder="ابحث..." style="padding:10px;border-radius:20px;border:2px solid #00c8ff;background:#1a1a3e;color:#fff;width:300px;"><button style="padding:10px 20px;border-radius:20px;border:none;background:#00c8ff;color:#000;font-weight:bold;">بحث</button></form>
    <form method="POST" style="text-align:center;"><input name="name" placeholder="اسم المشروع" required><input name="budget" placeholder="الميزانية" required><button>إضافة</button></form>
    <table><tr><th>ID</th><th>الاسم</th><th>الميزانية</th><th>الحالة</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
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
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">📦 الموردون</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <form method="POST" style="text-align:center;"><input name="name" placeholder="اسم المورد" required><input name="phone" placeholder="الهاتف"><button>إضافة</button></form>
    <table><tr><th>ID</th><th>الاسم</th><th>الهاتف</th></tr>"""
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
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">🧾 الفواتير</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <form method="POST" style="text-align:center;"><input name="customer_id" placeholder="رقم العميل" required><input name="amount" placeholder="المبلغ" required><input name="date" type="date" required><button>إصدار</button></form>
    <table><tr><th>ID</th><th>العميل</th><th>المبلغ</th><th>التاريخ</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/tasks', methods=['GET','POST'])
def tasks():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO tasks (project_id, title, status) VALUES (?,?,?)", (request.form['project_id'], request.form['title'], 'قيد التنفيذ'))
        conn.commit()
    c.execute("SELECT * FROM tasks")
    rows = c.fetchall(); conn.close()
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">📝 المهام</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <form method="POST" style="text-align:center;"><input name="project_id" placeholder="رقم المشروع" required><input name="title" placeholder="عنوان المهمة" required><button>إضافة</button></form>
    <table><tr><th>ID</th><th>المشروع</th><th>العنوان</th><th>الحالة</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/reports')
def reports():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products"); products = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM employees"); employees = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM projects"); projects = c.fetchone()[0]
    conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📊 التقارير</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>المؤشر</th><th>القيمة</th></tr>
    <tr><td>💰 الإيرادات</td><td>{revenue}</td></tr>
    <tr><td>👥 العملاء</td><td>{customers}</td></tr>
    <tr><td>📦 المنتجات</td><td>{products}</td></tr>
    <tr><td>👷 الموظفون</td><td>{employees}</td></tr>
    <tr><td>📁 المشاريع</td><td>{projects}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/analytics')
def analytics():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(salary),0) FROM employees"); salaries = c.fetchone()[0]
    conn.close()
    profit = revenue - salaries
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">📈 التحليلات</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>الإيرادات</th><th>الرواتب</th><th>الربح</th></tr>
    <tr><td>{revenue}</td><td>{salaries}</td><td style="color:#4affb0;">{profit}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/executive')
def executive():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM projects"); projects = c.fetchone()[0]
    conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">👑 اللوحة التنفيذية</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin-top:20px;">
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #FFD700;border-radius:20px;"><h2 style="color:#FFD700;">{revenue}</h2>الإيرادات</div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #00c8ff;border-radius:20px;"><h2 style="color:#00c8ff;">{customers}</h2>العملاء</div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #4affb0;border-radius:20px;"><h2 style="color:#4affb0;">{projects}</h2>المشاريع</div>
    </div>"""
    return render_template_string(PAGE, content=content)

@app.route('/ai_center')
def ai_center():
    if 'user' not in session: return redirect('/login')
    minds = [
        ("🧠", "المحلل المالي", "تحليل الإيرادات والمصاريف", "/reports"),
        ("🔮", "المتنبئ", "توقع النمو", "/analytics"),
        ("📊", "محلل الأداء", "مؤشرات الأداء", "/executive"),
        ("👥", "محلل العملاء", "تحليل العملاء", "/customers"),
        ("📦", "محلل المخزون", "تحليل المخزون", "/products"),
        ("👷", "محلل الموظفين", "تحليل الرواتب", "/employees"),
        ("📁", "محلل المشاريع", "تحليل المشاريع", "/projects"),
        ("🧾", "محلل الفواتير", "تحليل الفواتير", "/invoices"),
        ("📦", "محلل الموردين", "تحليل الموردين", "/suppliers"),
        ("📝", "محلل المهام", "تحليل المهام", "/tasks"),
    ]
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🧠 مركز الذكاء الاصطناعي</h2>
    <p style="text-align:center;color:#aaa;">10 عقول ذكية متخصصة</p>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;margin-top:20px;">"""
    for icon, name, desc, link in minds:
        content += f'<a href="{link}" style="display:block;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:20px;text-align:center;border:2px solid #00c8ff;text-decoration:none;color:#fff;"><span style="font-size:2.5rem;">{icon}</span><h3 style="color:#00c8ff;margin:10px 0;">{name}</h3><p style="color:#aaa;">{desc}</p></a>'
    content += "</div>"
    return render_template_string(PAGE, content=content)

@app.route('/security')
def security():
    if 'user' not in session: return redirect('/login')
    systems = [
        ("🔐", "تشفير البيانات", "AES-256"),
        ("🛡️", "حماية من الهجمات", "جدار ناري"),
        ("📋", "سجل التدقيق", "كل العمليات"),
        ("💾", "نسخ احتياطي", "تلقائي"),
        ("🔑", "إدارة الصلاحيات", "أدوار المستخدمين"),
        ("🚨", "كشف الاختراق", "تنبيه فوري"),
        ("🧹", "تنظيف البيانات", "حذف آمن"),
        ("🔍", "فحص الثغرات", "دوري"),
        ("📊", "تقارير الأمان", "شاملة"),
        ("👁️", "مراقبة مباشرة", "24/7"),
    ]
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#ff4a4a;">🛡️ مركز الحماية</h2>
    <p style="text-align:center;color:#aaa;">10 أنظمة حماية</p>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;">"""
    for icon, name, desc in systems:
        content += f'<div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:20px;text-align:center;border:2px solid #ff4a4a;"><span style="font-size:2.5rem;">{icon}</span><h3 style="color:#ff4a4a;margin:10px 0;">{name}</h3><p style="color:#aaa;">{desc}</p></div>'
    content += "</div>"
    return render_template_string(PAGE, content=content)

@app.route('/development')
def development():
    if 'user' not in session: return redirect('/login')
    systems = [
        ("🧬", "التعلم الذاتي", "يتعلم من البيانات"),
        ("🔧", "الإصلاح الذاتي", "يصلح الأخطاء"),
        ("📈", "التحسين الذاتي", "يحسن الأداء"),
        ("🔄", "التكيف الذاتي", "يتكيف مع المتغيرات"),
        ("🧠", "التفكير الذاتي", "يحلل القرارات"),
        ("💾", "الحفظ الذاتي", "يحفظ تلقائياً"),
        ("🔐", "الحماية الذاتية", "يحمي نفسه"),
        ("📊", "التقييم الذاتي", "يقيم أداءه"),
        ("🚀", "التطوير الذاتي", "يضيف ميزات"),
        ("🌟", "التطور الذاتي", "يتطور باستمرار"),
    ]
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">🧬 مركز التطوير الذاتي</h2>
    <p style="text-align:center;color:#aaa;">10 أنظمة تطوير</p>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;">"""
    for icon, name, desc in systems:
        content += f'<div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:20px;text-align:center;border:2px solid #4affb0;"><span style="font-size:2.5rem;">{icon}</span><h3 style="color:#4affb0;margin:10px 0;">{name}</h3><p style="color:#aaa;">{desc}</p></div>'
    content += "</div>"
    return render_template_string(PAGE, content=content)

@app.route('/charts')
def charts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT type, COUNT(*) FROM accounts GROUP BY type")
    accounts_data = c.fetchall()
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products"); products = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM employees"); employees = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM projects"); projects = c.fetchone()[0]
    conn.close()
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📊 الرسوم البيانية</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:15px;margin-top:20px;">
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #FFD700;border-radius:20px;"><h2 style="color:#FFD700;">{customers}</h2>عملاء</div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #00c8ff;border-radius:20px;"><h2 style="color:#00c8ff;">{products}</h2>منتجات</div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #4affb0;border-radius:20px;"><h2 style="color:#4affb0;">{employees}</h2>موظفون</div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #FFD700;border-radius:20px;"><h2 style="color:#FFD700;">{projects}</h2>مشاريع</div>
    </div>
    <canvas id="chart" style="margin-top:20px;"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        new Chart(document.getElementById('chart'), {
            type: 'bar',
            data: {
                labels: ['العملاء','المنتجات','الموظفون','المشاريع'],
                datasets: [{data: [""" + str(customers) + "," + str(products) + "," + str(employees) + "," + str(projects) + """], backgroundColor: ['#FFD700','#00c8ff','#4affb0','#FF8C00']}]
            },
            options: {responsive: true, plugins: {legend: {display: false}}}
        });
    </script>"""
    return render_template_string(PAGE, content=content)

@app.route('/export')
def export():
    if 'user' not in session: return redirect('/login')
    import csv, io
    conn = sqlite3.connect(DB); c = conn.cursor()
    tables = ['accounts','customers','suppliers','products','invoices','employees','projects','tasks']
    output = io.StringIO()
    writer = csv.writer(output)
    for table in tables:
        writer.writerow([f"=== {table} ==="])
        c.execute(f"SELECT * FROM {table}")
        rows = c.fetchall()
        for row in rows:
            writer.writerow(row)
        writer.writerow([])
    conn.close()
    from flask import Response
    csv_content = output.getvalue()
    return Response(csv_content, mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=erp_export.csv"})

@app.route('/search')
def search():
    if 'user' not in session: return redirect('/login')
    query = request.args.get('q', '')
    results = []
    if query:
        conn = sqlite3.connect(DB); c = conn.cursor()
        c.execute("SELECT 'عميل', name FROM customers WHERE name LIKE ?", (f'%{query}%',))
        results.extend(c.fetchall())
        c.execute("SELECT 'منتج', name FROM products WHERE name LIKE ?", (f'%{query}%',))
        results.extend(c.fetchall())
        c.execute("SELECT 'موظف', name FROM employees WHERE name LIKE ?", (f'%{query}%',))
        results.extend(c.fetchall())
        c.execute("SELECT 'مشروع', name FROM projects WHERE name LIKE ?", (f'%{query}%',))
        results.extend(c.fetchall())
        conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🔍 البحث الشامل</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <form method="GET" action="/search" style="text-align:center;"><input name="q" placeholder="ابحث..." value="{query}" style="padding:10px;border-radius:20px;border:2px solid #00c8ff;background:#1a1a3e;color:#fff;width:300px;"><button style="padding:10px 20px;border-radius:20px;border:none;background:#00c8ff;color:#000;">بحث</button></form>
    <table><tr><th>النوع</th><th>الاسم</th></tr>"""
    for r in results:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/notifications')
def notifications():
    if 'user' not in session: return redirect('/login')
    alerts = [
        "📊 تقرير يومي جاهز",
        "👥 عميل جديد مسجل",
        "📦 مخزون منخفض",
        "👷 موظف جديد",
        "📁 مشروع نشط",
    ]
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">🔔 الإشعارات</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>"""
    for a in alerts:
        content += f'<div style="background:#1a1a4e;padding:15px;border-radius:10px;margin:10px 0;border:2px solid #FFD700;">{a}</div>'
    return render_template_string(PAGE, content=content)

@app.route('/backup')
def backup():
    if 'user' not in session: return redirect('/login')
    import shutil
    backup_name = f"erp_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy(DB, backup_name)
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">💾 النسخ الاحتياطي</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <p style="text-align:center;">تم إنشاء: {backup_name}</p>"""
    return render_template_string(PAGE, content=content)

@app.route('/sales', methods=['GET','POST'])
def sales():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER, qty INTEGER, date TEXT)")
    if request.method == 'POST':
        c.execute("INSERT INTO sales (customer_id, product_id, qty, date) VALUES (?,?,?,?)", (request.form['customer_id'], request.form['product_id'], request.form['qty'], request.form['date']))
        conn.commit()
    c.execute("SELECT * FROM sales")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">🛒 المبيعات</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><form method="POST" style="text-align:center;"><input name="customer_id" placeholder="العميل" required><input name="product_id" placeholder="المنتج" required><input name="qty" placeholder="الكمية" required><input name="date" type="date" required><button>تسجيل</button></form><table><tr><th>ID</th><th>العميل</th><th>المنتج</th><th>الكمية</th><th>التاريخ</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/purchases', methods=['GET','POST'])
def purchases():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS purchases (id INTEGER PRIMARY KEY, supplier_id INTEGER, product_id INTEGER, qty INTEGER, date TEXT)")
    if request.method == 'POST':
        c.execute("INSERT INTO purchases (supplier_id, product_id, qty, date) VALUES (?,?,?,?)", (request.form['supplier_id'], request.form['product_id'], request.form['qty'], request.form['date']))
        conn.commit()
    c.execute("SELECT * FROM purchases")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🛍️ المشتريات</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><form method="POST" style="text-align:center;"><input name="supplier_id" placeholder="المورد" required><input name="product_id" placeholder="المنتج" required><input name="qty" placeholder="الكمية" required><input name="date" type="date" required><button>تسجيل</button></form><table><tr><th>ID</th><th>المورد</th><th>المنتج</th><th>الكمية</th><th>التاريخ</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/payroll', methods=['GET','POST'])
def payroll():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS payroll (id INTEGER PRIMARY KEY, employee_id INTEGER, salary REAL, deductions REAL)")
    if request.method == 'POST':
        c.execute("INSERT INTO payroll (employee_id, salary, deductions) VALUES (?,?,?)", (request.form['employee_id'], request.form['salary'], request.form.get('deductions',0)))
        conn.commit()
    c.execute("SELECT * FROM payroll")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">💼 الرواتب</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><form method="POST" style="text-align:center;"><input name="employee_id" placeholder="الموظف" required><input name="salary" placeholder="الراتب" required><input name="deductions" placeholder="الخصومات" value="0"><button>تسجيل</button></form><table><tr><th>ID</th><th>الموظف</th><th>الراتب</th><th>الخصومات</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051)
