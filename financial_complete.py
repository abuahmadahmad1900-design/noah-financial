#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦅 نوح - النظام المالي الإمبراطوري الكامل
لوحة تحكم خيالية + كل الميزات المتقدمة
"""

import sqlite3, shutil, csv, io, os, json, threading, time
from datetime import datetime
from flask import Flask, request, render_template, render_template_string, session, redirect, url_for, Response

app = Flask(__name__)
app.secret_key = 'noah_ultra_secret_2026'
DB = 'financial_complete.db'

# ========== إنشاء قاعدة البيانات ==========
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, name TEXT, type TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS suppliers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, date TEXT, paid INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS purchase_orders (id INTEGER PRIMARY KEY, supplier_id INTEGER, amount REAL, date TEXT, received INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, salary REAL);
    CREATE TABLE IF NOT EXISTS taxes (id INTEGER PRIMARY KEY, invoice_id INTEGER, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS bank_moves (id INTEGER PRIMARY KEY, date TEXT, desc TEXT, amount REAL, reconciled INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS zakat (id INTEGER PRIMARY KEY, amount REAL, date TEXT, paid INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS currencies (id INTEGER PRIMARY KEY, code TEXT, rate REAL);
    CREATE TABLE IF NOT EXISTS budgets (id INTEGER PRIMARY KEY, name TEXT, amount REAL);
    CREATE TABLE IF NOT EXISTS debts (id INTEGER PRIMARY KEY, name TEXT, amount REAL, type TEXT);
    CREATE TABLE IF NOT EXISTS assets (id INTEGER PRIMARY KEY, name TEXT, value REAL, depreciation REAL);
    CREATE TABLE IF NOT EXISTS warehouses (id INTEGER PRIMARY KEY, name TEXT, location TEXT);
    CREATE TABLE IF NOT EXISTS stock_moves (id INTEGER PRIMARY KEY, product_id INTEGER, warehouse_id INTEGER, qty INTEGER, type TEXT, date TEXT);
    CREATE TABLE IF NOT EXISTS investments (id INTEGER PRIMARY KEY, name TEXT, amount REAL, returns REAL);
    CREATE TABLE IF NOT EXISTS payroll (id INTEGER PRIMARY KEY, employee_id INTEGER, salary REAL, deductions REAL);
    CREATE TABLE IF NOT EXISTS audit_log (id INTEGER PRIMARY KEY, action TEXT, date TEXT);
    CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT DEFAULT 'admin');
    CREATE TABLE IF NOT EXISTS roles (id INTEGER PRIMARY KEY, name TEXT UNIQUE);
    CREATE TABLE IF NOT EXISTS alerts (id INTEGER PRIMARY KEY, message TEXT, type TEXT, date TEXT, read INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT, budget REAL, start_date TEXT, end_date TEXT, status TEXT DEFAULT 'نشط');
    CREATE TABLE IF NOT EXISTS contracts (id INTEGER PRIMARY KEY, title TEXT, party TEXT, amount REAL, date TEXT, status TEXT DEFAULT 'ساري');
    CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, sender TEXT, receiver TEXT, subject TEXT, body TEXT, date TEXT, read INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS system_logs (id INTEGER PRIMARY KEY, event TEXT, date TEXT);
    CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
    CREATE TABLE IF NOT EXISTS notifications (id INTEGER PRIMARY KEY, user TEXT, message TEXT, date TEXT, read INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER, qty INTEGER, date TEXT);
    CREATE TABLE IF NOT EXISTS purchases (id INTEGER PRIMARY KEY, supplier_id INTEGER, product_id INTEGER, qty INTEGER, date TEXT);
    ''')
    c.execute("INSERT OR IGNORE INTO roles (name) VALUES ('admin')")
    c.execute("INSERT OR IGNORE INTO roles (name) VALUES ('accountant')")
    c.execute("INSERT OR IGNORE INTO roles (name) VALUES ('viewer')")
    c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
    conn.commit()
    conn.close()

init_db()

# ========== صفحة عامة ==========
PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>نوح - النظام المالي</title>
    <style>
        body{font-family:Tahoma;background:#0a0a1a;color:#eee;padding:15px}
        a{color:#4a4aff;text-decoration:none;margin:4px;display:inline-block}
        input,select,button,textarea{padding:7px;margin:4px;border-radius:5px;border:1px solid #555;background:#222;color:#eee}
        table{width:100%;border-collapse:collapse;margin-top:10px}
        th,td{border:1px solid #444;padding:6px;text-align:center}
        th{background:#333}
        .container{background:#111;padding:20px;border-radius:10px;margin-top:15px}
    </style>
</head>
<body>
    <h1>🏦 نوح</h1>
    <div style="background:#1a1a3e;padding:10px;border-radius:5px;margin-bottom:15px">
        <a href="/">🏠</a>
        <a href="/accounts">📚 الحسابات</a>
        <a href="/customers">👥 العملاء</a>
        <a href="/suppliers">📦 الموردون</a>
        <a href="/invoices">🧾 الفواتير</a>
        <a href="/purchase_orders">📋 أوامر الشراء</a>
        <a href="/products">📦 المنتجات</a>
        <a href="/warehouses">🏭 المستودعات</a>
        <a href="/stock_moves">🔄 المخزون</a>
        <a href="/employees">👷 الموظفون</a>
        <a href="/payroll">💼 الرواتب</a>
        <a href="/taxes">💰 الضرائب</a>
        <a href="/bank">🏦 البنك</a>
        <a href="/zakat">🕌 الزكاة</a>
        <a href="/investments">📈 الاستثمارات</a>
        <a href="/trial_balance">⚖️ ميزان المراجعة</a>
        <a href="/ledger">📒 دفتر الأستاذ</a>
        <a href="/income_statement">📈 قائمة الدخل</a>
        <a href="/balance_sheet">📊 الميزانية</a>
        <a href="/cashflow">💵 التدفقات</a>
        <a href="/kpis">🎯 مؤشرات الأداء</a>
        <a href="/analytics">📊 التحليلات</a>
        <a href="/currencies">💱 العملات</a>
        <a href="/budgets">📋 الميزانيات</a>
        <a href="/debts">💳 الديون</a>
        <a href="/assets">🏢 الأصول</a>
        <a href="/audit">🔍 التدقيق</a>
        <a href="/export">📥 تصدير</a>
        <a href="/backup">💾 النسخ</a>
        <a href="/powers">⚡ القدرات</a>
        <a href="/projects">📁 المشاريع</a>
        <a href="/contracts">📜 العقود</a>
        <a href="/messages">✉️ الرسائل</a>
        <a href="/alerts">🔔 التنبيهات</a>
        <a href="/settings">⚙️ الإعدادات</a>
        <a href="/users">👤 المستخدمون</a>
        <a href="/advanced_analytics">🔮 تحليلات متقدمة</a>
        <a href="/logout">🚪 خروج</a>
    </div>
    <div class="container">
        {{ content | safe }}
    </div>
</body>
</html>
'''

# ========== تسجيل الدخول ==========
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
    <!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>دخول نوح</title>
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

# ========== قائمة الدخل ==========
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

# ========== الميزانية العمومية ==========
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

# ========== التدفقات النقدية ==========
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
    content = f"<h2>💵 التدفقات النقدية</h2><table><tr><th>التدفق الداخل</th><td>{inflow}</td></tr><tr><th>التدفق الخارج</th><td>{outflow}</td></tr><tr><th>صافي التدفق</th><td>{net}</td></tr></table>"
    return render_template_string(PAGE, content=content)

# ========== مؤشرات الأداء ==========
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
    content = f"<h2>🎯 مؤشرات الأداء</h2><table><tr><th>هامش الربح</th><td>{margin:.1f}%</td></tr><tr><th>العملاء</th><td>{cust}</td></tr><tr><th>الإيرادات</th><td>{rev}</td></tr><tr><th>المصاريف</th><td>{exp}</td></tr></table>"
    return render_template_string(PAGE, content=content)

# ========== التحليلات التنبؤية ==========
@app.route('/analytics')
def analytics():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    rev = c.fetchone()[0]
    conn.close()
    prediction = rev * 1.2
    content = f"<h2>📊 التحليلات التنبؤية</h2><table><tr><th>الإيرادات الحالية</th><td>{rev}</td></tr><tr><th>التوقع القادم</th><td>{prediction:.0f}</td></tr></table>"
    return render_template_string(PAGE, content=content)

# ========== العملات ==========
@app.route('/currencies', methods=['GET','POST'])
def currencies():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO currencies (code, rate) VALUES (?,?)", (request.form['code'], float(request.form['rate'])))
        conn.commit()
        log_action(f"إضافة عملة: {request.form['code']}")
    c.execute("SELECT * FROM currencies")
    rows = c.fetchall(); conn.close()
    content = "<h2>💱 العملات</h2><form method='POST'><input name='code' placeholder='رمز العملة' required><input name='rate' placeholder='السعر' required><button>إضافة</button></form><table><tr><th>ID</th><th>رمز</th><th>سعر</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

# ========== الميزانيات ==========
@app.route('/budgets', methods=['GET','POST'])
def budgets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO budgets (name, amount) VALUES (?,?)", (request.form['name'], float(request.form['amount'])))
        conn.commit()
        log_action(f"إضافة ميزانية: {request.form['name']}")
    c.execute("SELECT * FROM budgets")
    rows = c.fetchall(); conn.close()
    content = "<h2>📋 الميزانيات</h2><form method='POST'><input name='name' placeholder='اسم الميزانية' required><input name='amount' placeholder='المبلغ' required><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>مبلغ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

# ========== الديون ==========
@app.route('/debts', methods=['GET','POST'])
def debts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO debts (name, amount, type) VALUES (?,?,?)", (request.form['name'], float(request.form['amount']), request.form['type']))
        conn.commit()
        log_action(f"إضافة دين: {request.form['name']}")
    c.execute("SELECT * FROM debts")
    rows = c.fetchall(); conn.close()
    content = "<h2>💳 الديون</h2><form method='POST'><input name='name' placeholder='اسم الدين' required><input name='amount' placeholder='المبلغ' required><select name='type'><option>علينا</option><option>لنا</option></select><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>مبلغ</th><th>نوع</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

# ========== الأصول ==========
@app.route('/assets', methods=['GET','POST'])
def assets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO assets (name, value, depreciation) VALUES (?,?,?)", (request.form['name'], float(request.form['value']), float(request.form['depreciation'])))
        conn.commit()
        log_action(f"إضافة أصل: {request.form['name']}")
    c.execute("SELECT * FROM assets")
    rows = c.fetchall(); conn.close()
    content = "<h2>🏢 الأصول</h2><form method='POST'><input name='name' placeholder='اسم الأصل' required><input name='value' placeholder='القيمة' required><input name='depreciation' placeholder='الإهلاك' required><button>إضافة</button></form><table><tr><th>ID</th><th>اسم</th><th>قيمة</th><th>إهلاك</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

# ========== المشاريع ==========
@app.route('/projects', methods=['GET','POST'])
def projects():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO projects (name, budget, start_date, end_date, status) VALUES (?,?,?,?,?)",
                  (request.form['name'], float(request.form['budget']), request.form['start_date'],
                   request.form['end_date'], request.form.get('status', 'نشط')))
        conn.commit()
        log_action(f"إضافة مشروع: {request.form['name']}")
    c.execute("SELECT * FROM projects")
    rows = c.fetchall(); conn.close()
    content = "<h2>📁 المشاريع</h2><form method='POST'><input name='name' placeholder='اسم المشروع' required><input name='budget' placeholder='الميزانية' required><input name='start_date' type='date' required><input name='end_date' type='date' required><select name='status'><option>نشط</option><option>مكتمل</option><option>ملغى</option></select><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>الميزانية</th><th>البداية</th><th>النهاية</th><th>الحالة</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

# ========== العقود ==========
@app.route('/contracts', methods=['GET','POST'])
def contracts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO contracts (title, party, amount, date, status) VALUES (?,?,?,?,?)",
                  (request.form['title'], request.form['party'], float(request.form['amount']),
                   request.form['date'], request.form.get('status', 'ساري')))
        conn.commit()
        log_action(f"إضافة عقد: {request.form['title']}")
    c.execute("SELECT * FROM contracts")
    rows = c.fetchall(); conn.close()
    content = "<h2>📜 العقود</h2><form method='POST'><input name='title' placeholder='عنوان العقد' required><input name='party' placeholder='الطرف الآخر' required><input name='amount' placeholder='المبلغ' required><input name='date' type='date' required><select name='status'><option>ساري</option><option>منتهي</option><option>ملغى</option></select><button>إضافة</button></form><table><tr><th>ID</th><th>العنوان</th><th>الطرف</th><th>المبلغ</th><th>التاريخ</th><th>الحالة</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

# ========== الرسائل ==========
@app.route('/messages', methods=['GET','POST'])
def messages():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO messages (sender, receiver, subject, body, date, read) VALUES (?,?,?,?,?,0)",
                  (session['user'], request.form['receiver'], request.form['subject'],
                   request.form['body'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        log_action(f"إرسال رسالة إلى {request.form['receiver']}")
    c.execute("SELECT * FROM messages ORDER BY id DESC")
    rows = c.fetchall(); conn.close()
    content = "<h2>✉️ الرسائل</h2><form method='POST'><input name='receiver' placeholder='إلى' required><input name='subject' placeholder='الموضوع' required><textarea name='body' placeholder='نص الرسالة'></textarea><button>إرسال</button></form><table><tr><th>ID</th><th>من</th><th>إلى</th><th>الموضوع</th><th>التاريخ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[5]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

# ========== التنبيهات ==========
@app.route('/alerts')
def alerts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 50")
    rows = c.fetchall(); conn.close()
    content = "<h2>🔔 التنبيهات</h2><table><tr><th>ID</th><th>الرسالة</th><th>النوع</th><th>التاريخ</th></tr>"
    for r in rows:
        color = "#fff"
        if r[2] == 'warning': color = "#ffd700"
        elif r[2] == 'danger': color = "#ff4a4a"
        content += f"<tr style='color:{color}'><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

# ========== الإعدادات ==========
@app.route('/settings', methods=['GET','POST'])
def settings():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        for key, value in request.form.items():
            c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?,?)", (key, value))
        conn.commit()
        log_action("تحديث الإعدادات")
    c.execute("SELECT * FROM settings")
    rows = c.fetchall(); conn.close()
    content = "<h2>⚙️ الإعدادات</h2><form method='POST'><label>اسم الشركة:</label><input name='company_name' placeholder='اسم الشركة'><br><label>العملة الافتراضية:</label><input name='default_currency' placeholder='مثال: USD'><br><label>حد التنبيه للمخزون:</label><input name='low_stock_threshold' placeholder='مثال: 5'><br><button>حفظ</button></form><table><tr><th>المفتاح</th><th>القيمة</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

# ========== إدارة المستخدمين ==========
@app.route('/users')
def manage_users():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT id, username, role FROM users")
    rows = c.fetchall(); conn.close()
    content = "<h2>👤 إدارة المستخدمين</h2><table><tr><th>ID</th><th>المستخدم</th><th>الدور</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    content += """<form method="POST" action="/add_user">
        <input name="username" placeholder="اسم المستخدم" required>
        <input name="password" placeholder="كلمة المرور" required>
        <select name="role"><option>admin</option><option>accountant</option><option>viewer</option></select>
        <button>إضافة</button></form>"""
    return render_template_string(PAGE, content=content)

@app.route('/add_user', methods=['POST'])
def add_user():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)",
              (request.form['username'], request.form['password'], request.form['role']))
    conn.commit()
    conn.close()
    log_action(f"إضافة مستخدم: {request.form['username']}")
    return redirect('/users')

# ========== سجل النظام ==========
@app.route('/system_logs')
def system_logs():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM system_logs ORDER BY id DESC LIMIT 100")
    rows = c.fetchall(); conn.close()
    content = "<h2>📋 سجل النظام</h2><table><tr><th>ID</th><th>الحدث</th><th>التاريخ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

# ========== تحليلات متقدمة ==========
@app.route('/advanced_analytics')
def advanced_analytics():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT date, SUM(amount) FROM invoices GROUP BY date ORDER BY date")
    data = c.fetchall()
    c.execute("SELECT AVG(amount) FROM invoices")
    avg = c.fetchone()[0] or 0
    c.execute("SELECT MAX(amount) FROM invoices")
    max_amt = c.fetchone()[0] or 0
    conn.close()
    content = "<h2>🔮 تحليلات تنبؤية متقدمة</h2>"
    content += f"<p>متوسط الإيراد: {avg:.2f}</p><p>أعلى إيراد: {max_amt:.2f}</p>"
    content += "<canvas id='forecastChart'></canvas><script src='https://cdn.jsdelivr.net/npm/chart.js'></script><script>const labels=[];const values=[];"
    for row in data:
        content += f"labels.push('{row[0]}');values.push({row[1]});"
    content += "new Chart(document.getElementById('forecastChart'),{type:'line',data:{labels:labels,datasets:[{label:'الإيرادات',data:values,borderColor:'#00c8ff',fill:false}]},options:{responsive:true}});</script>"
    return render_template_string(PAGE, content=content)

# ========== محول العملات ==========
def convert_amount(amount, from_currency, to_currency):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT rate FROM currencies WHERE code=?", (from_currency,))
    row1 = c.fetchone()
    c.execute("SELECT rate FROM currencies WHERE code=?", (to_currency,))
    row2 = c.fetchone()
    conn.close()
    if row1 and row2:
        return amount * (row1[0] / row2[0])
    return amount

@app.route('/currency_converter', methods=['GET','POST'])
def currency_converter():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT code FROM currencies")
    codes = [r[0] for r in c.fetchall()]
    conn.close()
    result = None
    if request.method == 'POST':
        amount = float(request.form['amount'])
        from_cur = request.form['from_currency']
        to_cur = request.form['to_currency']
        result = convert_amount(amount, from_cur, to_cur)
        log_action(f"تحويل عملة {amount} من {from_cur} إلى {to_cur}")
    content = "<h2>💱 محول العملات</h2><form method='POST'>"
    content += "<input name='amount' placeholder='المبلغ' required>"
    content += "<select name='from_currency'>"
    for code in codes:
        content += f"<option value='{code}'>{code}</option>"
    content += "</select> → <select name='to_currency'>"
    for code in codes:
        content += f"<option value='{code}'>{code}</option>"
    content += "</select><button>تحويل</button></form>"
    if result is not None:
        content += f"<div style='background:#222;padding:15px;border-radius:5px;margin-top:15px'>✅ النتيجة: {result:.4f}</div>"
    return render_template_string(PAGE, content=content)

# ========== قائمة القدرات ==========
accounting_100_powers = [
    "إدارة الحسابات", "شجرة الحسابات", "قيود اليومية", "الأستاذ العام",
    "ميزان المراجعة", "قائمة الدخل", "الميزانية العمومية", "التدفقات النقدية",
    "العملاء", "الموردون", "الفواتير", "أوامر الشراء",
    "المنتجات", "المستودعات", "حركات المخزون", "الموظفون",
    "الرواتب", "الضرائب", "البنك", "الزكاة",
    "الاستثمارات", "الميزانيات", "الديون", "الأصول",
    "العملات", "التحليلات المالية", "مؤشرات الأداء", "التدقيق",
    "تصدير CSV", "النسخ الاحتياطي", "لوحة التحكم", "تسجيل الدخول",
    "إدارة المستخدمين", "قيود الإقفال", "الحسابات الختامية", "التسويات البنكية",
    "المخصصات", "الإهلاك", "التقارير الدورية", "الموازنات التقديرية",
    "تحليل الانحرافات", "تحليل النسب", "تحليل السيولة", "تحليل الربحية",
    "تحليل الكفاءة", "تحليل الرفع المالي", "التنبؤ المالي", "إعداد الميزانيات",
    "إدارة التدفق النقدي", "إدارة رأس المال العامل", "إدارة الائتمان", "إدارة المخاطر",
    "الامتثال الضريبي", "الامتثال للزكاة", "التقارير الحكومية", "التقارير الإدارية",
    "البيانات الضخمة", "الذكاء الاصطناعي المالي", "التعلم الآلي للتنبؤ", "أتمتة العمليات",
    "واجهات برمجة التطبيقات", "التكامل مع البنوك", "التكامل مع المتاجر", "التكامل مع العملاء",
    "الدعم متعدد اللغات", "الدعم متعدد العملات", "الدعم متعدد الشركات", "الصلاحيات المتعددة",
    "سجل التدقيق الكامل", "التشفير", "النسخ الاحتياطي التلقائي", "الاستعادة من النسخ",
    "المراقبة في الوقت الحقيقي", "التنبيهات", "الرسوم البيانية", "لوحات مخصصة",
    "تقارير قابلة للتخصيص", "تصدير PDF", "تصدير Excel", "البحث المتقدم",
    "العلامات المرجعية", "الملاحظات", "المرفقات", "سجل النشاط",
    "الاستيراد من ملفات", "التصدير إلى ملفات", "إدارة المشاريع", "الموارد البشرية",
    "إدارة الرواتب", "إدارة المزايا", "إدارة الحضور", "إدارة الأداء",
    "إدارة الضرائب", "إدارة الزكاة", "إدارة الأصول", "إدارة المخزون",
    "إدارة المشتريات", "إدارة المبيعات", "إدارة العملاء", "إدارة الموردين",
    "إدارة العقود", "إدارة المدفوعات", "إدارة المقبوضات", "إدارة الشيكات",
    "إدارة الحسابات البنكية", "إدارة البطاقات الائتمانية", "إدارة القروض", "إدارة الاستثمارات"
]

def show_powers():
    print("=" * 70)
    print("💰  قدرات المحاسبة الحقيقية (100 قدرة)")
    print("=" * 70)
    for i, power in enumerate(accounting_100_powers, 1):
        print(f"{i:3d}. {power}")
    print("=" * 70)
    print(f"الإجمالي: {len(accounting_100_powers)} قدرة")
    print("=" * 70)

@app.route('/powers')
def powers():
    if 'user' not in session: return redirect('/login')
    content = "<h2>⚡ قدرات المحاسبة الحقيقية (100 قدرة)</h2><ol>"
    for power in accounting_100_powers:
        content += f"<li>{power}</li>"
    content += "</ol>"
    return render_template_string(PAGE, content=content)

# ========== تصدير CSV ==========
@app.route('/export')
def export_csv():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    tables = ['accounts', 'customers', 'suppliers', 'invoices', 'purchase_orders',
              'products', 'warehouses', 'stock_moves', 'employees', 'payroll',
              'taxes', 'bank_moves', 'zakat', 'investments', 'currencies',
              'budgets', 'debts', 'assets', 'projects', 'contracts']
    output = io.StringIO()
    writer = csv.writer(output)
    for table in tables:
        writer.writerow([f"=== {table} ==="])
        c.execute(f"SELECT * FROM {table}")
        rows = c.fetchall()
        col_names = [description[0] for description in c.description]
        writer.writerow(col_names)
        for row in rows:
            writer.writerow(row)
        writer.writerow([])
    conn.close()
    csv_content = output.getvalue()
    log_action("تصدير البيانات CSV")
    return Response(csv_content, mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=noah_finance_export.csv"})

# ========== النسخ الاحتياطي ==========
@app.route('/backup')
def backup():
    if 'user' not in session: return redirect('/login')
    backup_name = f"backup_financial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy(DB, backup_name)
    log_action(f"نسخ احتياطي: {backup_name}")
    content = f"<h2>💾 النسخ الاحتياطي</h2><p>تم إنشاء نسخة احتياطية باسم: <b>{backup_name}</b></p>"
    return render_template_string(PAGE, content=content)

# ========== تشغيل التطبيق ==========
if __name__ == '__main__':
    show_powers()
    app.run(host='0.0.0.0', port=5000, debug=True)
