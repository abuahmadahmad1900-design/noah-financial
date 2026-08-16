#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, request, render_template_string, redirect, url_for
import json, os, shutil

app = Flask(__name__)

DB = 'accounting_extended.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # العملاء
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0)''')
    # الموردين
    c.execute('''CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0)''')
    # الفواتير
    c.execute('''CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, date TEXT, paid INTEGER DEFAULT 0)''')
    # البنوك
    c.execute('''CREATE TABLE IF NOT EXISTS bank_moves (
        id INTEGER PRIMARY KEY, date TEXT, desc TEXT, amount REAL, reconciled INTEGER DEFAULT 0)''')
    # الموظفين
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY, name TEXT, salary REAL)''')
    # الضرائب
    c.execute('''CREATE TABLE IF NOT EXISTS taxes (
        id INTEGER PRIMARY KEY, invoice_id INTEGER, amount REAL, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>نوح - النظام المحاسبي الموسع</title>
<style>
body{font-family:Tahoma;background:#0a0a1a;color:#eee;padding:20px}
a{color:#4a4aff;text-decoration:none;margin:5px}
input,select,button{padding:8px;margin:5px;border-radius:5px;border:1px solid #555;background:#222;color:#eee}
table{width:100%;border-collapse:collapse;margin-top:15px}
th,td{border:1px solid #444;padding:8px;text-align:center}
th{background:#333}
.nav{background:#1a1a3e;padding:10px;border-radius:5px;margin-bottom:20px}
</style>
</head>
<body>
<h1>🦅 نوح - النظام المحاسبي الموسع</h1>
<div class="nav">
<a href="/">🏠 الرئيسية</a>
<a href="/customers">👥 العملاء</a>
<a href="/suppliers">📦 الموردون</a>
<a href="/invoices">🧾 الفواتير</a>
<a href="/bank">🏦 البنك</a>
<a href="/employees">👷 الموظفون</a>
<a href="/taxes">💰 الضرائب</a>
<a href="/backup">💾 النسخ</a>
</div>
{% block content %}{% endblock %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(PAGE, content="<h2>اختر من القائمة</h2>")

# ===== العملاء =====
@app.route('/customers', methods=['GET','POST'])
def customers():
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO customers (name, phone) VALUES (?,?)", (request.form['name'], request.form['phone']))
        conn.commit()
    c.execute("SELECT * FROM customers")
    rows = c.fetchall()
    conn.close()
    content = "<h2>👥 العملاء</h2><form method='POST'><input name='name' placeholder='اسم العميل'><input name='phone' placeholder='الهاتف'><button>إضافة</button></form><table><tr><th>المعرف</th><th>الاسم</th><th>الهاتف</th><th>الرصيد</th></tr>"
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
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
    rows = c.fetchall()
    conn.close()
    content = "<h2>📦 الموردون</h2><form method='POST'><input name='name' placeholder='اسم المورد'><input name='phone' placeholder='الهاتف'><button>إضافة</button></form><table><tr><th>المعرف</th><th>الاسم</th><th>الهاتف</th><th>الرصيد</th></tr>"
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
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
    rows = c.fetchall()
    conn.close()
    content = "<h2>🧾 الفواتير</h2><form method='POST'><input name='customer_id' placeholder='رقم العميل'><input name='amount' placeholder='المبلغ'><input name='date' type='date'><button>إصدار</button></form><table><tr><th>رقم الفاتورة</th><th>العميل</th><th>المبلغ</th><th>التاريخ</th></tr>"
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
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
    rows = c.fetchall()
    conn.close()
    content = "<h2>🏦 البنك</h2><form method='POST'><input name='date' type='date'><input name='desc' placeholder='الوصف'><input name='amount' placeholder='المبلغ'><button>إضافة</button></form><table><tr><th>المعرف</th><th>التاريخ</th><th>الوصف</th><th>المبلغ</th></tr>"
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
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
    rows = c.fetchall()
    conn.close()
    content = "<h2>👷 الموظفون</h2><form method='POST'><input name='name' placeholder='اسم الموظف'><input name='salary' placeholder='الراتب'><button>إضافة</button></form><table><tr><th>المعرف</th><th>الاسم</th><th>الراتب</th></tr>"
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
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
    rows = c.fetchall()
    conn.close()
    content = "<h2>💰 الضرائب</h2><form method='POST'><input name='invoice_id' placeholder='رقم الفاتورة'><input name='amount' placeholder='مبلغ الضريبة'><input name='date' type='date'><button>إضافة</button></form><table><tr><th>المعرف</th><th>الفاتورة</th><th>المبلغ</th><th>التاريخ</th></tr>"
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

# ===== النسخ الاحتياطي =====
@app.route('/backup')
def backup():
    shutil.copy(DB, 'backup_accounting.db')
    return "<h3>✅ تم إنشاء نسخة احتياطية: backup_accounting.db</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=False)
