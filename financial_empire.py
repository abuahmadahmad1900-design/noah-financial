#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, request, render_template_string
import shutil

app = Flask(__name__)
DB = 'financial_empire.db'

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
    conn.commit()
    conn.close()

init_db()

PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>نوح - النظام المالي الحقيقي</title>
<style>
body{font-family:Tahoma;background:#0a0a1a;color:#eee;padding:15px}
a{color:#4a4aff;text-decoration:none;margin:4px;display:inline-block}
input,select,button{padding:7px;margin:4px;border-radius:5px;border:1px solid #555;background:#222;color:#eee}
table{width:100%;border-collapse:collapse;margin-top:10px}
th,td{border:1px solid #444;padding:6px;text-align:center}
th{background:#333}
.nav{background:#1a1a3e;padding:10px;border-radius:5px;margin-bottom:15px;line-height:2}
</style>
</head>
<body>
<h1>🏦 نوح - النظام المالي الحقيقي</h1>
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
<a href="/reports">📊 التقارير</a>
<a href="/zakat">🕌 الزكاة</a>
<a href="/backup">💾 النسخ</a>
</div>
{% block content %}{% endblock %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(PAGE, content="<h2>أهلاً بك في النظام المالي الحقيقي</h2>")

@app.route('/accounts', methods=['GET','POST'])
def accounts():
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
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (?,?,?)",
                  (request.form['customer_id'], float(request.form['amount']), request.form['date']))
        conn.commit()
    c.execute("SELECT * FROM invoices")
    rows = c.fetchall(); conn.close()
    content = "<h2>🧾 الفواتير</h2><form method='POST'><input name='customer_id' placeholder='عميل ID'><input name='amount' placeholder='مبلغ'><input name='date' type='date'><button>إصدار</button></form><table><tr><th>ID</th><th>عميل</th><th>مبلغ</th><th>تاريخ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/purchase_orders', methods=['GET','POST'])
def purchase_orders():
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO purchase_orders (supplier_id, amount, date) VALUES (?,?,?)",
                  (request.form['supplier_id'], float(request.form['amount']), request.form['date']))
        conn.commit()
    c.execute("SELECT * FROM purchase_orders")
    rows = c.fetchall(); conn.close()
    content = "<h2>📋 أوامر الشراء</h2><form method='POST'><input name='supplier_id' placeholder='مورد ID'><input name='amount' placeholder='مبلغ'><input name='date' type='date'><button>إصدار</button></form><table><tr><th>ID</th><th>مورد</th><th>مبلغ</th><th>تاريخ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/products', methods=['GET','POST'])
def products():
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO products (name, price, stock) VALUES (?,?,?)",
                  (request.form['name'], float(request.form['price']), int(request.form['stock'])))
        conn.commit()
    c.execute("SELECT * FROM products")
    rows = c.fetchall(); conn.close()
    content = "<h2>📦 المنتجات</h2><form method='POST'><input name='name' placeholder='اسم'><input name='price' placeholder='سعر'><input name='stock' placeholder='مخزون'><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>سعر</th><th>مخزون</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/employees', methods=['GET','POST'])
def employees():
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO employees (name, salary) VALUES (?,?)",
                  (request.form['name'], float(request.form['salary'])))
        conn.commit()
    c.execute("SELECT * FROM employees")
    rows = c.fetchall(); conn.close()
    content = "<h2>👷 الموظفون</h2><form method='POST'><input name='name' placeholder='اسم'><input name='salary' placeholder='راتب'><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>راتب</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/taxes', methods=['GET','POST'])
def taxes():
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO taxes (invoice_id, amount, date) VALUES (?,?,?)",
                  (request.form['invoice_id'], float(request.form['amount']), request.form['date']))
        conn.commit()
    c.execute("SELECT * FROM taxes")
    rows = c.fetchall(); conn.close()
    content = "<h2>💰 الضرائب</h2><form method='POST'><input name='invoice_id' placeholder='فاتورة ID'><input name='amount' placeholder='مبلغ'><input name='date' type='date'><button>إضافة</button></form><table><tr><th>ID</th><th>فاتورة</th><th>مبلغ</th><th>تاريخ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/bank', methods=['GET','POST'])
def bank():
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES (?,?,?)",
                  (request.form['date'], request.form['desc'], float(request.form['amount'])))
        conn.commit()
    c.execute("SELECT * FROM bank_moves")
    rows = c.fetchall(); conn.close()
    content = "<h2>🏦 البنك</h2><form method='POST'><input name='date' type='date'><input name='desc' placeholder='وصف'><input name='amount' placeholder='مبلغ'><button>إضافة</button></form><table><tr><th>ID</th><th>تاريخ</th><th>وصف</th><th>مبلغ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/reports')
def reports():
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM customers"); cust = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM invoices"); inv = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products"); prod = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM employees"); emp = c.fetchone()[0]
    conn.close()
    content = f"<h2>📊 التقارير</h2><div>👥 العملاء: {cust}<br>🧾 الفواتير: {inv}<br>📦 المنتجات: {prod}<br>👷 الموظفون: {emp}</div>"
    return render_template_string(PAGE, content=content)

@app.route('/zakat', methods=['GET','POST'])
def zakat():
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        # تسجيل دفعة زكاة
        c.execute("INSERT INTO zakat (amount, date) VALUES (?,?)",
                  (float(request.form['amount']), request.form['date']))
        conn.commit()
    # حساب الزكاة التقريبية: 2.5% من الأصول النقدية
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves")
    total_money = c.fetchone()[0]
    nisab = 85 * 60  # تقريبًا 85 غرام ذهب × 60 دولار للغرام
    zakat_due = total_money * 0.025 if total_money >= nisab else 0
    c.execute("SELECT * FROM zakat")
    rows = c.fetchall()
    conn.close()
    content = f"<h2>🕌 نظام الزكاة</h2><div>💰 إجمالي النقود: {total_money}<br>📏 النصاب التقريبي: {nisab}<br>🧮 الزكاة المستحقة (2.5%): {zakat_due:.2f}</div><hr><h3>تسجيل دفعة زكاة</h3><form method='POST'><input name='amount' placeholder='المبلغ' required><input name='date' type='date' required><button>تسجيل</button></form><h3>سجل الزكاة</h3><table><tr><th>ID</th><th>مبلغ</th><th>تاريخ</th></tr>"
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/backup')
def backup():
    shutil.copy(DB, 'backup_financial_empire.db')
    return "<h3>✅ نسخة احتياطية تمت</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=False)
