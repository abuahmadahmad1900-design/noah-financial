#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, request, render_template_string, redirect, url_for
import shutil, os, json

app = Flask(__name__)
DB = 'accounting_ultra_full.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # العملاء
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0)''')
    # الموردون
    c.execute('''CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0)''')
    # الفواتير
    c.execute('''CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, date TEXT, paid INTEGER DEFAULT 0)''')
    # البنك
    c.execute('''CREATE TABLE IF NOT EXISTS bank_moves (
        id INTEGER PRIMARY KEY, date TEXT, desc TEXT, amount REAL, reconciled INTEGER DEFAULT 0)''')
    # الموظفون
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY, name TEXT, salary REAL)''')
    # الضرائب
    c.execute('''CREATE TABLE IF NOT EXISTS taxes (
        id INTEGER PRIMARY KEY, invoice_id INTEGER, amount REAL, date TEXT)''')
    # المنتجات
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER DEFAULT 0)''')
    # المشاريع
    c.execute('''CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY, name TEXT, budget REAL)''')
    conn.commit()
    conn.close()

init_db()

PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>نوح - المحاسبة الفائقة</title>
<style>
body{font-family:Tahoma;background:#0a0a1a;color:#eee;padding:15px;font-size:14px}
a{color:#4a4aff;text-decoration:none;margin:4px;display:inline-block}
input,select,button{padding:7px;margin:4px;border-radius:5px;border:1px solid #555;background:#222;color:#eee}
table{width:100%;border-collapse:collapse;margin-top:10px}
th,td{border:1px solid #444;padding:6px;text-align:center}
th{background:#333}
.nav{background:#1a1a3e;padding:10px;border-radius:5px;margin-bottom:15px;line-height:2}
.card{background:#151530;border:1px solid #4a4aff;border-radius:8px;padding:12px;margin:8px 0}
</style>
</head>
<body>
<h1>🦅 نوح - المحاسبة الفائقة</h1>
<div class="nav">
<a href="/">🏠</a><a href="/customers">👥 عملاء</a><a href="/suppliers">📦 موردون</a>
<a href="/invoices">🧾 فواتير</a><a href="/bank">🏦 بنك</a><a href="/employees">👷 موظفون</a>
<a href="/taxes">💰 ضرائب</a><a href="/products">📦 منتجات</a><a href="/projects">📁 مشاريع</a>
<a href="/backup">💾 نسخ</a><a href="/reports">📊 تقارير</a>
</div>
{% block content %}{% endblock %}
</body>
</html>
"""

@app.route('/')
def index():
    content = "<div class='card'><h3>اختر من القائمة</h3></div>"
    return render_template_string(PAGE, content=content)

# ===== العملاء =====
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

# ===== الموردون =====
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

# ===== الفواتير =====
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

# ===== البنك =====
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

# ===== الموظفون =====
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

# ===== الضرائب =====
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

# ===== المنتجات =====
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

# ===== المشاريع =====
@app.route('/projects', methods=['GET','POST'])
def projects():
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO projects (name, budget) VALUES (?,?)",
                  (request.form['name'], float(request.form['budget'])))
        conn.commit()
    c.execute("SELECT * FROM projects")
    rows = c.fetchall(); conn.close()
    content = "<h2>📁 المشاريع</h2><form method='POST'><input name='name' placeholder='اسم'><input name='budget' placeholder='ميزانية'><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>ميزانية</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

# ===== النسخ =====
@app.route('/backup')
def backup():
    shutil.copy(DB, 'backup_ultra.db')
    return "<h3>✅ نسخة احتياطية تمت</h3>"

# ===== التقارير =====
@app.route('/reports')
def reports():
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM customers"); cust = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM invoices"); inv = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products"); prod = c.fetchone()[0]
    conn.close()
    content = f"<h2>📊 تقارير سريعة</h2><div class='card'>👥 العملاء: {cust}<br>🧾 الفواتير: {inv}<br>📦 المنتجات: {prod}</div>"
    return render_template_string(PAGE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=False)
