#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, request, render_template_string, session, redirect
import shutil, csv, io

app = Flask(__name__)
app.secret_key = 'noah_secret_key_2024'
DB = 'financial_empire_full.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, balance REAL DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, date TEXT, paid INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS purchase_orders (
        id INTEGER PRIMARY KEY, supplier_id INTEGER, amount REAL, date TEXT, received INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY, name TEXT, salary REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS taxes (
        id INTEGER PRIMARY KEY, invoice_id INTEGER, amount REAL, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bank_moves (
        id INTEGER PRIMARY KEY, date TEXT, desc TEXT, amount REAL, reconciled INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS zakat (
        id INTEGER PRIMARY KEY, amount REAL, date TEXT, paid INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS currencies (
        id INTEGER PRIMARY KEY, code TEXT, rate REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY, name TEXT, amount REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS debts (
        id INTEGER PRIMARY KEY, name TEXT, amount REAL, type TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY, name TEXT, value REAL, depreciation REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")
    c.execute('''CREATE TABLE IF NOT EXISTS warehouses (
        id INTEGER PRIMARY KEY, name TEXT, location TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS stock_moves (
        id INTEGER PRIMARY KEY, product_id INTEGER, warehouse_id INTEGER, qty INTEGER, type TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY, action TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS investments (
        id INTEGER PRIMARY KEY, name TEXT, amount REAL, returns REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS payroll (
        id INTEGER PRIMARY KEY, employee_id INTEGER, salary REAL, deductions REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY, action TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS investments (
        id INTEGER PRIMARY KEY, name TEXT, amount REAL, returns REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS payroll (
        id INTEGER PRIMARY KEY, employee_id INTEGER, salary REAL, deductions REAL)''')
    conn.commit()
    conn.close()

init_db()

PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>نوح - الإمبراطورية المالية الشاملة</title>
<style>
body{font-family:Tahoma;background:#0a0a1a;color:#eee;padding:15px;font-size:14px}
a{color:#4a4aff;text-decoration:none;margin:4px;display:inline-block}
input,select,button{padding:7px;margin:4px;border-radius:5px;border:1px solid #555;background:#222;color:#eee}
table{width:100%;border-collapse:collapse;margin-top:10px}
th,td{border:1px solid #444;padding:6px;text-align:center}
th{background:#333}
.nav{background:#1a1a3e;padding:10px;border-radius:5px;margin-bottom:15px;line-height:2}
.card{background:#151530;padding:20px;border-radius:10px;border:1px solid #4a4aff;flex:1;min-width:150px}
</style>
</head>
<body>
<h1>🏦 نوح - الإمبراطورية المالية الشاملة</h1>
<div class="nav">
<a href="/">🏠</a>
<a href="/accounts">📚 الحسابات</a>
<a href="/customers">👥 العملاء</a>
<a href="/suppliers">📦 الموردون</a>
<a href="/invoices">🧾 الفواتير</a>
<a href="/purchase_orders">📋 أوامر الشراء</a>
<a href="/products">📦 المنتجات</a>
<a href="/employees">👷 الموظفون</a>
<a href="/taxes">💰 الضرائب</a>
<a href="/bank">🏦 البنك</a>
<a href="/zakat">🕌 الزكاة</a>
<a href="/trial_balance">⚖️ ميزان المراجعة</a>
<a href="/ledger">📒 دفتر الأستاذ</a>
<a href="/income_statement">📈 قائمة الدخل</a>
<a href="/balance_sheet">📊 الميزانية</a>
<a href="/currencies">💱 العملات</a>
<a href="/budgets">📋 الميزانيات</a>
<a href="/debts">💳 الديون</a>
<a href="/assets">🏢 الأصول</a>
<a href="/export">📥 تصدير</a>
<a href="/backup">💾 النسخ</a>
<a href="/analytics">📊 التحليلات</a>
<a href="/cashflow">💵 التدفقات</a>
<a href="/kpis">🎯 مؤشرات الأداء</a>
<a href="/investments">📈 الاستثمارات</a>
<a href="/payroll">💼 الرواتب</a>
<a href="/audit">🔍 سجل التدقيق</a>
<a href="/analytics">📊 التحليلات</a>
<a href="/cashflow">💵 التدفقات</a>
<a href="/kpis">🎯 مؤشرات الأداء</a>
<a href="/investments">📈 الاستثمارات</a>
<a href="/payroll">💼 الرواتب</a>
<a href="/audit">🔍 سجل التدقيق</a>
<a href="/warehouses">🏭 المستودعات</a>
<a href="/stock_moves">🔄 حركات المخزون</a>
<a href="/logout">🚪 خروج</a>
</div>
{% block content %}{% endblock %}
</body>
</html>
"""

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB); c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone(); conn.close()
        if user:
            session['user'] = username
            return redirect('/')
        return "❌ خطأ في الدخول"
    return '''
    <!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>تسجيل الدخول</title>
    <style>
    body{font-family:Tahoma;background:#0a0a1a;color:#eee;display:flex;justify-content:center;align-items:center;height:100vh}
    form{background:#1a1a3e;padding:30px;border-radius:10px;border:1px solid #4a4aff}
    input{display:block;width:100%;padding:10px;margin:10px 0;border-radius:5px;border:1px solid #555;background:#222;color:#eee}
    button{width:100%;padding:10px;background:#4a4aff;border:none;border-radius:5px;color:#fff;font-size:16px}
    </style></head><body>
    <form method="POST">
        <h2>🦅 دخول نوح</h2>
        <input type="text" name="username" placeholder="اسم المستخدم" required>
        <input type="password" name="password" placeholder="كلمة المرور" required>
        <button>دخول</button>
    </form></body></html>'''

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM customers"); cust = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); rev = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM purchase_orders"); exp = c.fetchone()[0]
    conn.close()
    net = rev - exp
    # قراءة قالب اللوحة الخرافية
    with open('/data/data/com.termux/files/home/noah_eaglet/dashboard_noah_legendary.html', 'r') as f:
        dashboard = f.read()
    dashboard = dashboard.replace('{{ revenues }}', str(rev))
    dashboard = dashboard.replace('{{ expenses }}', str(exp))
    dashboard = dashboard.replace('{{ net }}', str(net))
    dashboard = dashboard.replace('{{ customers }}', str(cust))
    return dashboard

@app.route('/accounts', methods=['GET','POST'])
def accounts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO accounts (name, type) VALUES (?,?)", (request.form['name'], request.form['type']))
        conn.commit()
    c.execute("SELECT * FROM accounts")
    rows = c.fetchall(); conn.close()
    content = "<h2>📚 الحسابات</h2><form method='POST'><input name='name' placeholder='اسم الحساب'><select name='type'><option>أصول</option><option>خصوم</option><option>حقوق ملكية</option><option>إيرادات</option><option>مصاريف</option></select><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>نوع</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/customers', methods=['GET','POST'])
def customers():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO customers (name, phone) VALUES (?,?)", (request.form['name'], request.form['phone']))
        conn.commit()
    c.execute("SELECT * FROM customers")
    rows = c.fetchall(); conn.close()
    content = "<h2>👥 العملاء</h2><form method='POST'><input name='name' placeholder='اسم'><input name='phone' placeholder='هاتف'><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>هاتف</th><th>رصيد</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/suppliers', methods=['GET','POST'])
def suppliers():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO suppliers (name, phone) VALUES (?,?)", (request.form['name'], request.form['phone']))
        conn.commit()
    c.execute("SELECT * FROM suppliers")
    rows = c.fetchall(); conn.close()
    content = "<h2>📦 الموردون</h2><form method='POST'><input name='name' placeholder='اسم'><input name='phone' placeholder='هاتف'><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>هاتف</th><th>رصيد</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/invoices', methods=['GET','POST'])
def invoices():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (?,?,?)", (request.form['customer_id'], float(request.form['amount']), request.form['date']))
        conn.commit()
    c.execute("SELECT * FROM invoices")
    rows = c.fetchall(); conn.close()
    content = "<h2>🧾 الفواتير</h2><form method='POST'><input name='customer_id' placeholder='عميل ID'><input name='amount' placeholder='مبلغ'><input name='date' type='date'><button>إصدار</button></form><table><tr><th>ID</th><th>عميل</th><th>مبلغ</th><th>تاريخ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/purchase_orders', methods=['GET','POST'])
def purchase_orders():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO purchase_orders (supplier_id, amount, date) VALUES (?,?,?)", (request.form['supplier_id'], float(request.form['amount']), request.form['date']))
        conn.commit()
    c.execute("SELECT * FROM purchase_orders")
    rows = c.fetchall(); conn.close()
    content = "<h2>📋 أوامر الشراء</h2><form method='POST'><input name='supplier_id' placeholder='مورد ID'><input name='amount' placeholder='مبلغ'><input name='date' type='date'><button>إصدار</button></form><table><tr><th>ID</th><th>مورد</th><th>مبلغ</th><th>تاريخ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/products', methods=['GET','POST'])
def products():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO products (name, price, stock) VALUES (?,?,?)", (request.form['name'], float(request.form['price']), int(request.form['stock'])))
        conn.commit()
    c.execute("SELECT * FROM products")
    rows = c.fetchall(); conn.close()
    content = "<h2>📦 المنتجات</h2><form method='POST'><input name='name' placeholder='اسم'><input name='price' placeholder='سعر'><input name='stock' placeholder='مخزون'><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>سعر</th><th>مخزون</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/employees', methods=['GET','POST'])
def employees():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO employees (name, salary) VALUES (?,?)", (request.form['name'], float(request.form['salary'])))
        conn.commit()
    c.execute("SELECT * FROM employees")
    rows = c.fetchall(); conn.close()
    content = "<h2>👷 الموظفون</h2><form method='POST'><input name='name' placeholder='اسم'><input name='salary' placeholder='راتب'><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>راتب</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/taxes', methods=['GET','POST'])
def taxes():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO taxes (invoice_id, amount, date) VALUES (?,?,?)", (request.form['invoice_id'], float(request.form['amount']), request.form['date']))
        conn.commit()
    c.execute("SELECT * FROM taxes")
    rows = c.fetchall(); conn.close()
    content = "<h2>💰 الضرائب</h2><form method='POST'><input name='invoice_id' placeholder='فاتورة ID'><input name='amount' placeholder='مبلغ'><input name='date' type='date'><button>إضافة</button></form><table><tr><th>ID</th><th>فاتورة</th><th>مبلغ</th><th>تاريخ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/bank', methods=['GET','POST'])
def bank():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES (?,?,?)", (request.form['date'], request.form['desc'], float(request.form['amount'])))
        conn.commit()
    c.execute("SELECT * FROM bank_moves")
    rows = c.fetchall(); conn.close()
    content = "<h2>🏦 البنك</h2><form method='POST'><input name='date' type='date'><input name='desc' placeholder='وصف'><input name='amount' placeholder='مبلغ'><button>إضافة</button></form><table><tr><th>ID</th><th>تاريخ</th><th>وصف</th><th>مبلغ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/zakat', methods=['GET','POST'])
def zakat():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO zakat (amount, date) VALUES (?,?)", (float(request.form['amount']), request.form['date']))
        conn.commit()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves")
    total_money = c.fetchone()[0]
    nisab = 85 * 60
    zakat_due = total_money * 0.025 if total_money >= nisab else 0
    c.execute("SELECT * FROM zakat")
    rows = c.fetchall(); conn.close()
    content = f"<h2>🕌 الزكاة</h2><div>💰 إجمالي النقود: {total_money}<br>📏 النصاب: {nisab}<br>🧮 الزكاة المستحقة: {zakat_due:.2f}</div><hr><h3>تسجيل دفعة</h3><form method='POST'><input name='amount' placeholder='مبلغ'><input name='date' type='date'><button>تسجيل</button></form><table><tr><th>ID</th><th>مبلغ</th><th>تاريخ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/trial_balance')
def trial_balance():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, type, balance FROM accounts")
    rows = c.fetchall(); conn.close()
    content = "<h2>⚖️ ميزان المراجعة</h2><table><tr><th>الحساب</th><th>النوع</th><th>الرصيد</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/ledger')
def ledger():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    accounts = c.fetchall(); conn.close()
    content = "<h2>📒 دفتر الأستاذ</h2>"
    for acc in accounts:
        conn = sqlite3.connect(DB); c = conn.cursor()
        c.execute("SELECT * FROM bank_moves WHERE desc LIKE ?", (f"%{acc[1]}%",))
        moves = c.fetchall(); conn.close()
        content += f"<h3>{acc[1]}</h3><table><tr><th>ID</th><th>تاريخ</th><th>وصف</th><th>مبلغ</th></tr>"
        for m in moves: content += f"<tr><td>{m[0]}</td><td>{m[1]}</td><td>{m[2]}</td><td>{m[3]}</td></tr>"
        content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/income_statement')
def income_statement():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    revenues = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM purchase_orders")
    expenses = c.fetchone()[0]
    conn.close()
    net = revenues - expenses
    content = f"<h2>📈 قائمة الدخل</h2><table><tr><th>الإيرادات</th><td>{revenues}</td></tr><tr><th>المصاريف</th><td>{expenses}</td></tr><tr><th>صافي الربح</th><td>{net}</td></tr></table>"
    return render_template_string(PAGE, content=content)

@app.route('/balance_sheet')
def balance_sheet():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(balance),0) FROM accounts WHERE type='أصول'")
    assets = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(balance),0) FROM accounts WHERE type='خصوم'")
    liabilities = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(balance),0) FROM accounts WHERE type='حقوق ملكية'")
    equity = c.fetchone()[0]
    conn.close()
    content = f"<h2>📊 الميزانية العمومية</h2><table><tr><th>الأصول</th><td>{assets}</td></tr><tr><th>الخصوم</th><td>{liabilities}</td></tr><tr><th>حقوق الملكية</th><td>{equity}</td></tr></table>"
    return render_template_string(PAGE, content=content)

@app.route('/currencies', methods=['GET','POST'])
def currencies():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO currencies (code, rate) VALUES (?,?)", (request.form['code'], float(request.form['rate'])))
        conn.commit()
    c.execute("SELECT * FROM currencies")
    rows = c.fetchall(); conn.close()
    content = "<h2>💱 العملات</h2><form method='POST'><input name='code' placeholder='رمز'><input name='rate' placeholder='سعر'><button>إضافة</button></form><table><tr><th>ID</th><th>رمز</th><th>سعر</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/budgets', methods=['GET','POST'])
def budgets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO budgets (name, amount) VALUES (?,?)", (request.form['name'], float(request.form['amount'])))
        conn.commit()
    c.execute("SELECT * FROM budgets")
    rows = c.fetchall(); conn.close()
    content = "<h2>📋 الميزانيات</h2><form method='POST'><input name='name' placeholder='اسم'><input name='amount' placeholder='مبلغ'><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>مبلغ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/debts', methods=['GET','POST'])
def debts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO debts (name, amount, type) VALUES (?,?,?)", (request.form['name'], float(request.form['amount']), request.form['type']))
        conn.commit()
    c.execute("SELECT * FROM debts")
    rows = c.fetchall(); conn.close()
    content = "<h2>💳 الديون</h2><form method='POST'><input name='name' placeholder='اسم'><input name='amount' placeholder='مبلغ'><select name='type'><option>مستحق</option><option>مديونية</option></select><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>مبلغ</th><th>نوع</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/assets', methods=['GET','POST'])
def assets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO assets (name, value, depreciation) VALUES (?,?,?)", (request.form['name'], float(request.form['value']), float(request.form['depreciation'])))
        conn.commit()
    c.execute("SELECT * FROM assets")
    rows = c.fetchall(); conn.close()
    content = "<h2>🏢 الأصول الثابتة</h2><form method='POST'><input name='name' placeholder='اسم'><input name='value' placeholder='القيمة'><input name='depreciation' placeholder='الاستهلاك'><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>قيمة</th><th>استهلاك</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/export')
def export_csv():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM invoices")
    rows = c.fetchall(); conn.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'عميل', 'مبلغ', 'تاريخ'])
    for r in rows: writer.writerow(r)
    return f"<pre>{output.getvalue()}</pre>"

@app.route('/analytics')
def analytics():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    rev = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM purchase_orders")
    exp = c.fetchone()[0]
    conn.close()
    prediction = rev * 1.2  # توقع بسيط: نمو 20%
    content = f"<h2>📊 التحليلات التنبؤية</h2><div class='card'><h3>الإيرادات الحالية: {rev}</h3><h3>التوقع للفترة القادمة: {prediction:.0f} (نمو 20%)</h3></div>"
    return render_template_string(PAGE, content=content)

@app.route('/cashflow')
def cashflow():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0")
    inflow = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0")
    outflow = c.fetchone()[0]
    conn.close()
    net = inflow + outflow
    content = f"<h2>💵 التدفقات النقدية</h2><div class='card'><h3>التدفق الداخل: {inflow}</h3><h3>التدفق الخارج: {outflow}</h3><h3>صافي التدفق: {net}</h3></div>"
    return render_template_string(PAGE, content=content)

@app.route('/kpis')
def kpis():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    rev = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM purchase_orders")
    exp = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers")
    cust = c.fetchone()[0]
    conn.close()
    margin = ((rev - exp) / rev * 100) if rev > 0 else 0
    content = f"<h2>🎯 مؤشرات الأداء</h2><div class='card'><h3>هامش الربح: {margin:.1f}%</h3><h3>عدد العملاء: {cust}</h3><h3>الإيرادات: {rev}</h3><h3>المصاريف: {exp}</h3></div>"
    return render_template_string(PAGE, content=content)

@app.route('/investments', methods=['GET','POST'])
def investments():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO investments (name, amount, returns) VALUES (?,?,?)",
                  (request.form['name'], float(request.form['amount']), float(request.form['returns'])))
        conn.commit()
    c.execute("SELECT * FROM investments")
    rows = c.fetchall(); conn.close()
    content = "<h2>📈 الاستثمارات</h2><form method='POST'><input name='name' placeholder='اسم الاستثمار'><input name='amount' placeholder='المبلغ'><input name='returns' placeholder='العائد %'><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>مبلغ</th><th>عائد</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}%</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/payroll', methods=['GET','POST'])
def payroll():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO payroll (employee_id, salary, deductions) VALUES (?,?,?)",
                  (request.form['employee_id'], float(request.form['salary']), float(request.form['deductions'])))
        conn.commit()
    c.execute("SELECT * FROM payroll")
    rows = c.fetchall(); conn.close()
    content = "<h2>💼 الرواتب</h2><form method='POST'><input name='employee_id' placeholder='رقم الموظف'><input name='salary' placeholder='الراتب'><input name='deductions' placeholder='الخصومات'><button>إضافة</button></form><table><tr><th>ID</th><th>موظف</th><th>راتب</th><th>خصومات</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/audit')
def audit():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM audit_log")
    rows = c.fetchall(); conn.close()
    content = "<h2>🔍 سجل التدقيق</h2><table><tr><th>ID</th><th>العملية</th><th>التاريخ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=False)
