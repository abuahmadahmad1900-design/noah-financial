from flask import Flask, request, session, redirect, render_template_string
import sqlite3
import random

app = Flask(__name__)
from finance_extra import extra
app.register_blueprint(extra)
app.secret_key = 'finance_final_core_2026'
DB = 'final_core.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, name TEXT, type TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT);
    CREATE TABLE IF NOT EXISTS suppliers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT);
    CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER);
    CREATE TABLE IF NOT EXISTS bank_moves (id INTEGER PRIMARY KEY, date TEXT, desc TEXT, amount REAL);
    CREATE TABLE IF NOT EXISTS zakat (id INTEGER PRIMARY KEY, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS debts (id INTEGER PRIMARY KEY, name TEXT, amount REAL, type TEXT);
    CREATE TABLE IF NOT EXISTS budgets (id INTEGER PRIMARY KEY, name TEXT, amount REAL);
    ''')
    conn.commit()
    conn.close()

init_db()

PAGE = '''
<style>
    .inner-box { background:linear-gradient(145deg,rgba(20,20,60,0.95),rgba(10,10,30,0.95)); border-radius:25px; padding:30px; border:2px solid rgba(255,215,0,0.5); box-shadow:0 20px 50px rgba(0,0,0,0.6), 0 0 35px rgba(255,215,0,0.15); }
</style>
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>نوح المالي</title>
<style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { font-family:Tahoma; font-size:16px; font-size:16px; background:linear-gradient(135deg,#0a0a2e,#1a0a3e,#0a1a2e); background-size:400% 400%; animation:bg-shift 8s ease infinite; color:#fff; padding:20px; }
    @keyframes bg-shift { 0% { background-position:0% 50%; } 50% { background-position:100% 50%; } 100% { background-position:0% 50%; } }
    ..nav-btn { display:inline-flex; align-items:center; gap:8px; margin:8px; padding:14px 24px; border-radius:50px; text-decoration:none; font-weight:bold; font-size:0.95rem; transition:all 0.3s; animation: float-btn 3s ease-in-out infinite; background:rgba(10,10,40,0.8); }
    .nav-btn:hover { transform:scale(1.1); }
    .nav-btn span { display:inline-block; animation: spin-icon 3s linear infinite; }
    .nav-btn.gold { border:2px solid #FFD700; color:#FFD700; animation: glow-gold 1.8s infinite alternate, float-btn 3s ease-in-out infinite; }
    .nav-btn.blue { border:2px solid #00c8ff; color:#00c8ff; animation: glow-blue 1.8s infinite alternate, float-btn 3s ease-in-out infinite; }
    .nav-btn.green { border:2px solid #4affb0; color:#4affb0; animation: glow-green 1.8s infinite alternate, float-btn 3s ease-in-out infinite; }
    .nav-btn.red { border:2px solid #ff4a4a; color:#ff4a4a; animation: glow-red 1.8s infinite alternate, float-btn 3s ease-in-out infinite; }
    @keyframes glow-gold { 0% { box-shadow:0 0 5px rgba(255,215,0,0.4); } 100% { box-shadow:0 0 30px rgba(255,215,0,0.9); } }
    @keyframes glow-blue { 0% { box-shadow:0 0 5px rgba(0,200,255,0.4); } 100% { box-shadow:0 0 30px rgba(0,200,255,0.9); } }
    @keyframes glow-green { 0% { box-shadow:0 0 5px rgba(74,255,176,0.4); } 100% { box-shadow:0 0 30px rgba(74,255,176,0.9); } }
    @keyframes glow-red { 0% { box-shadow:0 0 5px rgba(255,74,74,0.4); } 100% { box-shadow:0 0 30px rgba(255,74,74,0.9); } }
    @keyframes float-btn { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-8px); } }
    @keyframes spin-icon { 0% { transform:rotate(0deg); } 100% { transform:rotate(360deg); } }
    table { width:100%; border-collapse:separate; border-spacing:0; margin-top:25px; border-radius:25px; overflow:hidden; box-shadow:0 25px 60px rgba(0,0,0,0.7), 0 0 40px rgba(255,215,0,0.15); background:linear-gradient(180deg,rgba(20,20,60,0.9),rgba(10,10,30,0.9)); }
    table thead th { background:linear-gradient(145deg,#FFD700,#FF8C00); color:#000; padding:20px; font-size:1.2rem; font-weight:bold; letter-spacing:1px; text-shadow:0 1px 2px rgba(255,255,255,0.3); }
    table tbody td { padding:18px 15px; text-align:center; color:#f0f0f0; font-size:1.05rem; border-bottom:1px solid rgba(255,215,0,0.1); transition:all 0.3s; }
    table tbody tr:nth-child(odd) td { background:rgba(255,255,255,0.02); }
    table tbody tr:nth-child(even) td { background:rgba(0,200,255,0.02); }
    table tbody tr:hover td { background:rgba(255,215,0,0.1); color:#FFD700; } border:2px solid rgba(255,215,0,0.4); animation: table-glow 3s ease-in-out infinite alternate; }
    @keyframes table-glow { 0% { box-shadow:0 0 15px rgba(255,215,0,0.2); } 100% { box-shadow:0 0 40px rgba(255,215,0,0.5); } } border-radius:25px; overflow:hidden; box-shadow:0 25px 60px rgba(0,0,0,0.7), 0 0 40px rgba(255,215,0,0.15); background:linear-gradient(180deg,rgba(20,20,60,0.9),rgba(10,10,30,0.9)); }
    table thead th { background:linear-gradient(145deg,#FFD700,#FF8C00); color:#000; padding:20px; font-size:1.2rem; font-weight:bold; letter-spacing:1px; text-shadow:0 1px 2px rgba(255,255,255,0.3); }
    table tbody td { padding:18px 15px; text-align:center; color:#f0f0f0; font-size:1.05rem; border-bottom:1px solid rgba(255,215,0,0.1); transition:all 0.3s; }
    table tbody tr:nth-child(odd) td { background:rgba(255,255,255,0.02); }
    table tbody tr:nth-child(even) td { background:rgba(0,200,255,0.02); }
    table tbody tr:hover td { background:rgba(255,215,0,0.1); color:#FFD700; transform:scale(1.01); }
    table tbody tr:hover td:first-child { border-radius:0 10px 10px 0; }
    table tbody tr:hover td:last-child { border-radius:10px 0 0 10px; } border-radius:20px; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,0.6), 0 0 30px rgba(255,215,0,0.1); }
    table thead th { background:linear-gradient(145deg,#2a2a5e,#1a1a3e); color:#FFD700; padding:18px; font-size:1.1rem; letter-spacing:1px; border-bottom:2px solid #FFD700; }
    table tbody td { padding:15px; text-align:center; color:#e0e0e0; font-size:1rem; border-bottom:1px solid rgba(255,255,255,0.05); transition:all 0.3s; }
    table tbody tr:nth-child(odd) { background:rgba(255,255,255,0.03); }
    table tbody tr:nth-child(even) { background:rgba(0,200,255,0.03); }
    table tbody tr:hover { background:rgba(255,215,0,0.08); transform:scale(1.005); }
    table tbody tr:hover td { color:#fff; }
    
    td { padding:12px; border-bottom:1px solid rgba(255,215,0,0.15); transition:all 0.3s; }
    tr:hover td { background:rgba(255,215,0,0.08); }
    h1 { text-align:center; background:linear-gradient(45deg,#FFD700,#FF8C00,#FFD700); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:1.5rem; animation:gradient-shift 3s ease infinite; }
    @keyframes title-shine { 0% { background-position:0% 50%; } 50% { background-position:100% 50%; } 100% { background-position:0% 50%; } }
        @keyframes gradient-shift { 0% { background-position:0% 50%; } 50% { background-position:100% 50%; } 100% { background-position:0% 50%; } }
    input, select, button { padding:10px; margin:5px; background:#1a1a3e; color:#fff; border:1px solid #FFD700; border-radius:8px; }
    button { background:#FFD700; color:#000; font-weight:bold; cursor:pointer; }
</style></head>
<body>
{{ content | safe }}
</body></html>'''


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['user'] = 'admin'
        return redirect('/dashboard')
    return '<h2>🦅 دخول</h2><form method="POST"><input name="username" placeholder="المستخدم"><input name="password" type="password" placeholder="كلمة المرور"><button>دخول</button></form>'

@app.route('/subledger')
def subledger():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, type, balance FROM accounts ORDER BY type")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">📒 الأستاذ المساعد</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع للوحة التحكم</a></p><form method="GET" action="/subledger" style="text-align:center;margin:10px 0;"><input type="text" name="q" placeholder="ابحث..." style="padding:10px;border-radius:20px;border:2px solid #00c8ff;background:#1a1a3e;color:#fff;width:300px;"><button style="padding:10px 20px;border-radius:20px;border:none;background:#00c8ff;color:#000;font-weight:bold;cursor:pointer;">بحث</button></form><table><tr><th>الحساب</th><th>النوع</th><th>الرصيد</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/subledger_assets')
def subledger_assets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, balance FROM accounts WHERE type='أصول'")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;color:#FFD700;">📒 أستاذ الأصول</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الحساب</th><th>الرصيد</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/subledger_liabilities')
def subledger_liabilities():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, balance FROM accounts WHERE type='خصوم'")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;color:#ff4a4a;">📒 أستاذ الخصوم</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الحساب</th><th>الرصيد</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/subledger_revenue')
def subledger_revenue():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, balance FROM accounts WHERE type='إيرادات'")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;color:#4affb0;">📒 أستاذ الإيرادات</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الحساب</th><th>الرصيد</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/subledger_expenses')
def subledger_expenses():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, balance FROM accounts WHERE type='مصاريف'")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;color:#ff8c00;">📒 أستاذ المصاريف</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الحساب</th><th>الرصيد</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/subledger_equity')
def subledger_equity():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, balance FROM accounts WHERE type='حقوق ملكية'")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;color:#FFD700;">📒 أستاذ الملكية</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الحساب</th><th>الرصيد</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/subledger_customers')
def subledger_customers():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, phone FROM customers")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;color:#00c8ff;">📒 أستاذ العملاء</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الاسم</th><th>الهاتف</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/subledger_suppliers')
def subledger_suppliers():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, phone FROM suppliers")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;color:#4affb0;">📒 أستاذ الموردين</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الاسم</th><th>الهاتف</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/subledger_inventory')
def subledger_inventory():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, price, stock FROM products")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;color:#FFD700;">📒 أستاذ المخزون</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>المنتج</th><th>السعر</th><th>المخزون</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/subledger_invoices')
def subledger_invoices():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT id, amount, date FROM invoices")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;color:#00c8ff;">📒 أستاذ الفواتير</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>رقم</th><th>المبلغ</th><th>التاريخ</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/subledger_bank')
def subledger_bank():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT date, desc, amount FROM bank_moves")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;color:#4affb0;">📒 أستاذ البنك</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>التاريخ</th><th>الوصف</th><th>المبلغ</th></tr>"""
    for r in rows:
        color = "#4affb0" if r[2] > 0 else "#ff4a4a"
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td style='color:{color}'>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/subledger_zakat')
def subledger_zakat():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0")
    total = c.fetchone()[0]
    conn.close()
    nisab = 85 * 60
    due = total * 0.025 if total >= nisab else 0
    content = f"""<h2 style="text-align:center;color:#FFD700;">📒 أستاذ الزكاة</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>النقود</th><th>النصاب</th><th>المستحقة</th></tr><tr><td>{total}</td><td>{nisab}</td><td>{due:.2f}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/subledger_debts')
def subledger_debts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, amount, type FROM debts")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;color:#ff4a4a;">📒 أستاذ الديون</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الاسم</th><th>المبلغ</th><th>النوع</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/subledger_budgets')
def subledger_budgets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, amount FROM budgets")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;color:#FFD700;">📒 أستاذ الميزانيات</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الاسم</th><th>المبلغ</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/subledger_assets_fixed')
def subledger_assets_fixed():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, value FROM assets")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;color:#00c8ff;">📒 أستاذ الأصول الثابتة</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الاسم</th><th>القيمة</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/subledger_currencies')
def subledger_currencies():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT code, rate FROM currencies")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;color:#4affb0;">📒 أستاذ العملات</h2><p style="text-align:center;"><a href="/subledger" style="color:#00c8ff;">رجوع</a></p><table><tr><th>العملة</th><th>السعر</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/advanced_reports')
def advanced_reports():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    conn.close()
    content = f"""<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📊 التقارير المتقدمة</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الإيرادات</th></tr><tr><td>{revenue}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/smart_analysis')
def smart_analysis():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0"); expenses = abs(c.fetchone()[0])
    conn.close()
    margin = (revenue - expenses) / revenue * 100 if revenue > 0 else 0
    content = f"""<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🧠 التحليل الذكي</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>هامش الربح</th></tr><tr><td>{margin:.1f}%</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/currency_converter')
def currency_converter():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">💱 محول العملات</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><form method="POST" action="/currency_converter" style="text-align:center;margin:10px 0;"><input type="number" name="amount" placeholder="المبلغ" step="0.01" style="padding:10px;border-radius:20px;border:2px solid #00c8ff;background:#1a1a3e;color:#fff;width:200px;"><input type="number" name="from_rate" placeholder="من" step="0.01" value="1" style="padding:10px;border-radius:20px;border:2px solid #00c8ff;background:#1a1a3e;color:#fff;width:150px;"><input type="number" name="to_rate" placeholder="إلى" step="0.01" value="1" style="padding:10px;border-radius:20px;border:2px solid #00c8ff;background:#1a1a3e;color:#fff;width:150px;"><button style="padding:10px 20px;border-radius:20px;border:none;background:#00c8ff;color:#000;font-weight:bold;cursor:pointer;">تحويل</button></form>"""
    if request.method == 'POST':
        amount = float(request.form.get('amount', 0))
        from_rate = float(request.form.get('from_rate', 1))
        to_rate = float(request.form.get('to_rate', 1))
        result = amount * (to_rate / from_rate)
        content += f"<p style='text-align:center;font-size:2rem;color:#FFD700;'>✅ {result:.2f}</p>"
    return render_template_string(PAGE, content=content)

@app.route('/kpis')
def kpis():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    conn.close()
    content = f"""<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">🎯 مؤشرات الأداء</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الإيرادات</th><th>العملاء</th></tr><tr><td>{revenue}</td><td>{customers}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

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
    conn.close()
    content = f"""
    <style>
        @keyframes float-card {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-10px); }} }}
        @keyframes glow-gold {{ 0%,100% {{ box-shadow:0 0 15px rgba(255,215,0,0.4); }} 50% {{ box-shadow:0 0 40px rgba(255,215,0,0.9); }} }}
        @keyframes glow-blue {{ 0%,100% {{ box-shadow:0 0 15px rgba(0,200,255,0.4); }} 50% {{ box-shadow:0 0 40px rgba(0,200,255,0.9); }} }}
        @keyframes glow-green {{ 0%,100% {{ box-shadow:0 0 15px rgba(74,255,176,0.4); }} 50% {{ box-shadow:0 0 40px rgba(74,255,176,0.9); }} }}
        @keyframes glow-red {{ 0%,100% {{ box-shadow:0 0 15px rgba(255,74,74,0.4); }} 50% {{ box-shadow:0 0 40px rgba(255,74,74,0.9); }} }}
        .stat-card {{ background:linear-gradient(145deg,#1a1a4e,#0d0d2e); border-radius:25px; padding:30px; text-align:center; border:2px solid; animation:float-card 3s ease-in-out infinite; }}
        .stat-card h2 {{ font-size:1.5rem; margin:10px 0; }}
        .stat-card p {{ color:#aaa; font-size:1rem; }}
        .btn {{ display:inline-block; padding:18px 28px; border-radius:50px; text-decoration:none; font-weight:bold; font-size:1rem; margin:10px; transition:all 0.3s; animation:float-card 3s ease-in-out infinite; }}
        .btn:hover {{ transform:scale(1.1); }}
        .btn span {{ display:inline-block; animation:spin 3s linear infinite; }}
        @keyframes spin {{ 0% {{ transform:rotate(0); }} 100% {{ transform:rotate(360deg); }} }}
    </style>
    <h1 style="text-align:center;font-size:3.5rem;margin-top:40px;font-weight:900;background:linear-gradient(45deg,#FFD700,#FF8C00,#FF4500,#FFD700);background-size:400% 400%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:3px;text-shadow:0 0 50px rgba(255,215,0,0.7), 0 0 100px rgba(255,140,0,0.4);">👑 🦅 لوحة نوح المالية 👑</h1>
    <p style="text-align:center;font-size:1.5rem;font-weight:bold;background:linear-gradient(45deg,#FFD700,#FF8C00,#FFD700);background-size:300% 300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:gradient-shift 3s ease infinite;letter-spacing:2px;text-shadow:0 0 30px rgba(255,215,0,0.5);">✦ النظام المالي الأسطوري المتكامل ✦</p>
    <div style="position:fixed;left:15px;top:150px;z-index:1000;">
        <div style="display:inline-block;background:linear-gradient(145deg,rgba(20,20,60,0.95),rgba(10,10,30,0.95));border:2px solid #FFD700;border-radius:25px;padding:10px 20px;box-shadow:0 0 40px rgba(255,215,0,0.3);animation:glow-gold 2s infinite alternate;">
            <div style="font-size:1rem;color:#FFD700;font-weight:bold;" id="date-display"></div>
            <div style="font-size:1.5rem;color:#fff;font-weight:bold;margin-top:10px;" id="clock-display"></div>
            <div style="font-size:0.8rem;color:#aaa;margin-top:5px;" id="weekday-display"></div>
        </div>
    </div>
    <script>
        function updateDateTime() {{
            const now = new Date();
            const days = ['الأحد','الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت'];
            const months = ['يناير','فبراير','مارس','أبريل','مايو','يونيو','يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر'];
            document.getElementById('date-display').textContent = now.getDate() + ' ' + months[now.getMonth()] + ' ' + now.getFullYear();
            document.getElementById('clock-display').textContent = now.toLocaleTimeString('ar');
            document.getElementById('weekday-display').textContent = days[now.getDay()] + ' - الأسبوع ' + Math.ceil(now.getDate() / 7);
        }}
        updateDateTime();
        setInterval(updateDateTime, 1000);
    </script>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:25px;margin:120px 0 40px 0;">
        <div class="stat-card" style="border-color:#FFD700;animation:glow-gold 2s infinite alternate, float-card 3s ease-in-out infinite;"><h2 style="color:#FFD700;">{accounts}</h2><p>الحسابات</p></div>
        <div class="stat-card" style="border-color:#00c8ff;animation:glow-blue 2s infinite alternate, float-card 3s ease-in-out infinite;"><h2 style="color:#00c8ff;">{customers}</h2><p>العملاء</p></div>
        <div class="stat-card" style="border-color:#4affb0;animation:glow-green 2s infinite alternate, float-card 3s ease-in-out infinite;"><h2 style="color:#4affb0;">{invoices}</h2><p>الفواتير</p></div>
        <div class="stat-card" style="border-color:#FFD700;animation:glow-gold 2s infinite alternate, float-card 3s ease-in-out infinite;"><h2 style="color:#FFD700;">{products}</h2><p>المنتجات</p></div>
    </div>
    <div style="text-align:center;">
        <a href="/accounts" class="btn" style="border:2px solid #FFD700;color:#FFD700;animation:glow-gold 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>📚</span> الحسابات</a>
        <a href="/customers" class="btn" style="border:2px solid #00c8ff;color:#00c8ff;animation:glow-blue 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>👥</span> العملاء</a>
        <a href="/suppliers" class="btn" style="border:2px solid #4affb0;color:#4affb0;animation:glow-green 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>📦</span> الموردون</a>
        <a href="/invoices" class="btn" style="border:2px solid #FFD700;color:#FFD700;animation:glow-gold 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>🧾</span> الفواتير</a>
        <a href="/products" class="btn" style="border:2px solid #00c8ff;color:#00c8ff;animation:glow-blue 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>📦</span> المنتجات</a>
        <a href="/payments" class="btn" style="border:2px solid #FFD700;color:#FFD700;animation:glow-gold 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>💳</span> المدفوعات</a>
        <a href="/bank_reconciliation" class="btn" style="border:2px solid #00c8ff;color:#00c8ff;animation:glow-blue 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>🏦</span> التسويات</a>
        <a href="/bank" class="btn" style="border:2px solid #4affb0;color:#4affb0;animation:glow-green 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>🏦</span> البنك</a>
        <a href="/zakat" class="btn" style="border:2px solid #FFD700;color:#FFD700;animation:glow-gold 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>🕌</span> الزكاة</a>
        <a href="/budget_forecast" class="btn" style="border:2px solid #FFD700;color:#FFD700;animation:glow-gold 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>📈</span> موازنات</a>
        <a href="/debts" class="btn" style="border:2px solid #00c8ff;color:#00c8ff;animation:glow-blue 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>💳</span> الديون</a>
        <a href="/budgets" class="btn" style="border:2px solid #4affb0;color:#4affb0;animation:glow-green 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>📋</span> الميزانيات</a>
        <a href="/assets" class="btn" style="border:2px solid #FFD700;color:#FFD700;animation:glow-gold 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>🏢</span> الأصول</a>
        <a href="/global_currencies" class="btn" style="border:2px solid #FFD700;color:#FFD700;animation:glow-gold 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>🌍</span> العملات العالمية</a>
        <a href="/currencies" class="btn" style="border:2px solid #00c8ff;color:#00c8ff;animation:glow-blue 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>💱</span> العملات</a>
        <a href="/trial_balance_detail" class="btn" style="border:2px solid #FFD700;color:#FFD700;animation:glow-gold 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>⚖️</span> ميزان المراجعة</a>
        <a href="/ledger" class="btn" style="border:2px solid #4affb0;color:#4affb0;animation:glow-green 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>📒</span> الأستاذ</a>
        <a href="/journal" class="btn" style="border:2px solid #00c8ff;color:#00c8ff;animation:glow-blue 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>📒</span> دفتر اليومية</a>
        <a href="/cashflow" class="btn" style="border:2px solid #FFD700;color:#FFD700;animation:glow-gold 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>💵</span> التدفقات</a>
        <a href="/ai_forecast" class="btn" style="border:2px solid #00c8ff;color:#00c8ff;animation:glow-blue 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>🧠</span> تنبؤ</a>
        <a href="/extra_home" class="btn" style="border:2px solid #FFD700;color:#FFD700;animation:glow-gold 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>🚀</span> الموسع</a>
        <a href="/financial_ratios" class="btn" style="border:2px solid #00c8ff;color:#00c8ff;animation:glow-blue 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>📊</span> نسب مالية</a>
        <a href="/sensitivity" class="btn" style="border:2px solid #4affb0;color:#4affb0;animation:glow-green 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>🔮</span> حساسية</a>
        <a href="/executive_dashboard" class="btn" style="border:2px solid #FFD700;color:#FFD700;animation:glow-gold 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>📊</span> تنفيذية</a>
        <a href="/logout" class="btn" style="border:2px solid #ff4a4a;color:#ff4a4a;animation:glow-red 2s infinite alternate, float-card 3s ease-in-out infinite;"><span>🚪</span> خروج</a>
    </div>"""
    return render_template_string(PAGE, content=content)

@app.route('/accounts')
def accounts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    rows = c.fetchall(); conn.close()
    content = """
    <h2 style="text-align:center;font-size:1.5rem;color:#FFD700;">📚 الحسابات</h2>
    <p style="text-align:center;color:#aaa;">إدارة الحسابات العامة</p>
    <table><tr><th>ID</th><th>الاسم</th><th>النوع</th><th>الرصيد</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/customers')
def customers():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM customers")
    rows = c.fetchall(); conn.close()
    content = """
    <h2 style="text-align:center;font-size:1.5rem;color:#00c8ff;">👥 العملاء</h2>
    <p style="text-align:center;color:#aaa;">إدارة علاقات العملاء</p>
    <table><tr><th>ID</th><th>الاسم</th><th>الهاتف</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/suppliers')
def suppliers():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM suppliers")
    rows = c.fetchall(); conn.close()
    content = """
    <h2 style="text-align:center;font-size:1.5rem;color:#4affb0;">📦 الموردون</h2>
    <p style="text-align:center;color:#aaa;">إدارة الموردين</p>
    <table><tr><th>ID</th><th>الاسم</th><th>الهاتف</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/invoices')
def invoices():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM invoices ORDER BY id DESC LIMIT 5")
    rows = c.fetchall(); conn.close()
    content = """
    <h2 style="text-align:center;font-size:1.5rem;color:#FFD700;">🧾 الفواتير</h2>
    <p style="text-align:center;color:#aaa;">إدارة الفواتير</p>
    <table><tr><th>ID</th><th>العميل</th><th>المبلغ</th><th>التاريخ</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/products')
def products():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall(); conn.close()
    content = """
    <h2 style="text-align:center;font-size:1.5rem;color:#00c8ff;">📦 المنتجات</h2>
    <p style="text-align:center;color:#aaa;">إدارة المنتجات</p>
    <table><tr><th>ID</th><th>الاسم</th><th>السعر</th><th>المخزون</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/payments')
def payments():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT date, desc, amount FROM bank_moves WHERE amount > 0 ORDER BY date DESC")
    incoming = c.fetchall()
    c.execute("SELECT date, desc, amount FROM bank_moves WHERE amount < 0 ORDER BY date DESC")
    outgoing = c.fetchall()
    conn.close()
    content = """
    <h2 style="text-align:center;font-size:1.5rem;color:#FFD700;">💳 المدفوعات والمقبوضات</h2>
    <h3 style="color:#4affb0;">📥 المقبوضات</h3>
    <table><tr><th>التاريخ</th><th>الوصف</th><th>المبلغ</th></tr>"""
    for r in incoming:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td style='color:#4affb0;'>{r[2]}</td></tr>"
    content += "</table>"
    content += "<h3 style='color:#ff4a4a;'>📤 المدفوعات</h3>"
    content += "<table><tr><th>التاريخ</th><th>الوصف</th><th>المبلغ</th></tr>"
    for r in outgoing:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td style='color:#ff4a4a;'>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/bank')
def bank():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM bank_moves ORDER BY id DESC LIMIT 5")
    rows = c.fetchall(); conn.close()
    content = """
    <h2 style="text-align:center;font-size:1.5rem;color:#4affb0;">🏦 البنك</h2>
    <p style="text-align:center;color:#aaa;">الحركات البنكية</p>
    <table><tr><th>ID</th><th>التاريخ</th><th>الوصف</th><th>المبلغ</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/bank_reconciliation')
def bank_reconciliation():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0")
    incoming = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0")
    outgoing = c.fetchone()[0]
    conn.close()
    balance = incoming + outgoing
    content = f"""
    <h2 style="text-align:center;font-size:1.5rem;color:#00c8ff;">🏦 التسويات البنكية</h2>
    <table>
        <tr><th>البند</th><th>القيمة</th></tr>
        <tr><td>إجمالي المقبوضات</td><td style="color:#4affb0;">{incoming}</td></tr>
        <tr><td>إجمالي المدفوعات</td><td style="color:#ff4a4a;">{outgoing}</td></tr>
        <tr><td>الرصيد الصافي</td><td style="color:#FFD700;font-size:1rem;">{balance}</td></tr>
    </table>"""
    return render_template_string(PAGE, content=content)

@app.route('/zakat')
def zakat():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0")
    total = c.fetchone()[0]
    conn.close()
    nisab = 85 * 60
    due = total * 0.025 if total >= nisab else 0
    content = f"""
    <h2 style="text-align:center;font-size:1.5rem;color:#FFD700;">🕌 الزكاة</h2>
    <p style="text-align:center;color:#aaa;">حساب زكاة المال</p>
    <table>
        <tr><th>💰 النقود</th><th>📏 النصاب</th><th>🧮 المستحقة</th></tr>
        <tr><td style="font-size:1rem;color:#FFD700;">{total}</td><td style="font-size:1rem;">{nisab}</td><td style="font-size:2rem;color:#FFD700;">{due:.2f}</td></tr>
    </table>"""
    return render_template_string(PAGE, content=content)

@app.route('/budget_forecast')
def budget_forecast():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:1.5rem;color:#FFD700;">📈 الموازنات التقديرية</h2>
    <table>
        <tr><th>البند</th><th>الفعلي</th><th>التقديري</th></tr>
        <tr><td>الإيرادات</td><td>{revenue}</td><td style="color:#4affb0;">{revenue * 1.2:.0f}</td></tr>
        <tr><td>المصاريف</td><td>{revenue * 0.4:.0f}</td><td style="color:#ff4a4a;">{revenue * 0.45:.0f}</td></tr>
    </table>"""
    return render_template_string(PAGE, content=content)

@app.route('/debts')
def debts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM debts")
    rows = c.fetchall(); conn.close()
    content = "<h2>💳 الديون</h2><table border='1'><tr><th>ID</th><th>الاسم</th><th>المبلغ</th><th>النوع</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/budgets')
def budgets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM budgets")
    rows = c.fetchall(); conn.close()
    content = "<h2>📋 الميزانيات</h2><table border='1'><tr><th>ID</th><th>الاسم</th><th>المبلغ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

@app.route('/assets')
def assets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS assets (id INTEGER PRIMARY KEY, name TEXT, value REAL)''')
    c.execute("SELECT * FROM assets")
    rows = c.fetchall(); conn.close()
    content = "<h2>🏢 الأصول</h2><table border='1'><tr><th>ID</th><th>الاسم</th><th>القيمة</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/financial_ratios')
def financial_ratios():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0"); expenses = abs(c.fetchone()[0])
    conn.close()
    profit = revenue - expenses
    margin = (profit / revenue * 100) if revenue > 0 else 0
    content = f"""
    <h2 style="text-align:center;font-size:1.5rem;color:#00c8ff;">📊 النسب المالية</h2>
    <table>
        <tr><th>النسبة</th><th>القيمة</th></tr>
        <tr><td>هامش الربح</td><td style="color:#FFD700;">{margin:.1f}%</td></tr>
    </table>"""
    return render_template_string(PAGE, content=content)

@app.route('/sensitivity')
def sensitivity():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:1.5rem;color:#4affb0;">🔮 تحليل الحساسية</h2>
    <table>
        <tr><th>السيناريو</th><th>الإيراد</th></tr>
        <tr><td>متفائل (+20%)</td><td style="color:#4affb0;">{revenue * 1.2:.0f}</td></tr>
        <tr><td>محايد</td><td>{revenue}</td></tr>
        <tr><td>متشائم (-20%)</td><td style="color:#ff4a4a;">{revenue * 0.8:.0f}</td></tr>
    </table>"""
    return render_template_string(PAGE, content=content)

@app.route('/executive_dashboard')
def executive_dashboard():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products"); products = c.fetchone()[0]
    conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:1.5rem;color:#FFD700;">📊 لوحة المؤشرات التنفيذية</h2>
    <table>
        <tr><th>المؤشر</th><th>القيمة</th></tr>
        <tr><td>الإيرادات</td><td>{revenue}</td></tr>
        <tr><td>العملاء</td><td>{customers}</td></tr>
        <tr><td>المنتجات</td><td>{products}</td></tr>
    </table>"""
    return render_template_string(PAGE, content=content)

@app.route('/global_currencies')
def global_currencies():
    if 'user' not in session: return redirect('/login')
    currencies_data = [
        ("🇺🇸", "دولار أمريكي", "USD", 1.0),
        ("🇪🇺", "يورو", "EUR", 0.92),
        ("🇸🇦", "ريال سعودي", "SAR", 3.75),
        ("🇦🇪", "درهم إماراتي", "AED", 3.67),
        ("🇪🇬", "جنيه مصري", "EGP", 48.5),
        ("🇰🇼", "دينار كويتي", "KWD", 0.31),
        ("🇶🇦", "ريال قطري", "QAR", 3.64),
        ("🇴🇲", "ريال عماني", "OMR", 0.38),
        ("🇧🇭", "دينار بحريني", "BHD", 0.38),
        ("🇯🇴", "دينار أردني", "JOD", 0.71),
        ("🇮🇶", "دينار عراقي", "IQD", 1310),
        ("🇱🇧", "ليرة لبنانية", "LBP", 89500),
        ("🟢⬛", "ليرة سورية (علم جديد)", "SYP", 13000),
        ("🇹🇷", "ليرة تركية", "TRY", 32.8),
        ("🇬🇧", "جنيه إسترليني", "GBP", 0.79),
        ("🇯🇵", "ين ياباني", "JPY", 149.5),
        ("🇨🇳", "يوان صيني", "CNY", 7.2),
        ("🇷🇺", "روبل روسي", "RUB", 92.3),
        ("🇮🇳", "روبية هندية", "INR", 83.5),
        ("🇵🇰", "روبية باكستانية", "PKR", 278.5),
    ]
    rows = ""
    for flag, name, code, rate in currencies_data:
        change = random.uniform(-0.005, 0.005)
        new_rate = rate * (1 + change)
        buy = new_rate * 1.02
        sell = new_rate * 0.98
        rows += f"<tr><td>{flag} {code}</td><td>{name}</td><td style='color:#4affb0;'>{buy:.4f}</td><td style='color:#ff4a4a;'>{sell:.4f}</td></tr>"
    content = f"""
    <h2 style="text-align:center;font-size:1.5rem;color:#FFD700;">🌍 العملات العالمية</h2>
    <p style="text-align:center;color:#aaa;">أسعار الصرف مقابل الدولار</p>
    <table>
        <tr><th>العملة</th><th>الاسم</th><th>شراء</th><th>بيع</th></tr>
        {rows}
    </table>"""
    return render_template_string(PAGE, content=content)

@app.route('/currencies')
def currencies():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS currencies (id INTEGER PRIMARY KEY, code TEXT, rate REAL)''')
    c.execute("SELECT * FROM currencies")
    rows = c.fetchall(); conn.close()
    content = "<h2>💱 العملات</h2><table border='1'><tr><th>ID</th><th>رمز</th><th>سعر</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/trial_balance_detail')
def trial_balance_detail():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT type, SUM(balance) FROM accounts GROUP BY type")
    rows = c.fetchall()
    conn.close()
    content = """
    <h2 style="text-align:center;font-size:1.5rem;color:#FFD700;">⚖️ ميزان المراجعة</h2>
    <p style="text-align:center;color:#aaa;">أرصدة الحسابات حسب النوع</p>
    <table>
        <tr><th>النوع</th><th>الرصيد</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td style='color:#FFD700;'>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/ledger')
def ledger():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    rows = c.fetchall(); conn.close()
    content = "<h2>📒 دفتر الأستاذ</h2><table border='1'><tr><th>ID</th><th>الحساب</th><th>النوع</th><th>الرصيد</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/journal')
def journal():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT date, desc, amount FROM bank_moves ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    content = """
    <h2 style="text-align:center;font-size:1.5rem;color:#00c8ff;">📒 دفتر اليومية</h2>
    <p style="text-align:center;color:#aaa;">القيود اليومية</p>
    <table>
        <tr><th>التاريخ</th><th>الوصف</th><th>المبلغ</th></tr>"""
    for r in rows:
        color = "#4affb0" if r[2] > 0 else "#ff4a4a"
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td style='color:{color}'>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/cashflow')
def cashflow():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0"); inflow = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0"); outflow = c.fetchone()[0]
    conn.close()
    net = inflow + outflow
    content = f"""
    <h2 style="text-align:center;font-size:1.5rem;color:#FFD700;">💵 التدفقات النقدية</h2>
    <p style="text-align:center;color:#aaa;">مراقبة السيولة</p>
    <table>
        <tr><th>البند</th><th>القيمة</th></tr>
        <tr><td>التدفق الداخل</td><td style="color:#4affb0;">{inflow}</td></tr>
        <tr><td>التدفق الخارج</td><td style="color:#ff4a4a;">{outflow}</td></tr>
        <tr><td>صافي التدفق</td><td style="color:#FFD700;font-size:1rem;">{net}</td></tr>
    </table>"""
    return render_template_string(PAGE, content=content)

@app.route('/ai_forecast')
def ai_forecast():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    conn.close()
    next_month = revenue * 1.15
    content = f"""
    <h2 style="text-align:center;font-size:1.5rem;color:#00c8ff;">🧠 التنبؤ المالي</h2>
    <p style="text-align:center;color:#aaa;">توقع الإيرادات المستقبلية</p>
    <table>
        <tr><th>الفترة</th><th>الإيراد المتوقع</th></tr>
        <tr><td>الحالي</td><td style="color:#FFD700;">{revenue}</td></tr>
        <tr><td>الشهر القادم (+15%)</td><td style="color:#4affb0;">{next_month:.0f}</td></tr>
        <tr><td>بعد 3 أشهر (+40%)</td><td style="color:#4affb0;">{revenue * 1.4:.0f}</td></tr>
    </table>"""
    return render_template_string(PAGE, content=content)

@app.route('/economic_indicators')
def economic_indicators():
    if 'user' not in session: return redirect('/login')
    content = """
    <h2 style="text-align:center;font-size:1.5rem;color:#4affb0;">📈 المؤشرات الاقتصادية</h2>
    <table>
        <tr><th>المؤشر</th><th>القيمة</th></tr>
        <tr><td>التضخم</td><td>2.5%</td></tr>
        <tr><td>البطالة</td><td>5.0%</td></tr>
        <tr><td>نمو الناتج المحلي</td><td>3.2%</td></tr>
    </table>"""
    return render_template_string(PAGE, content=content)

@app.route('/stock_market')
def stock_market():
    if 'user' not in session: return redirect('/login')
    content = """
    <h2 style="text-align:center;font-size:1.5rem;color:#FFD700;">💰 سوق الأسهم</h2>
    <table>
        <tr><th>المؤشر</th><th>القيمة</th><th>التغير</th></tr>
        <tr><td>S&P 500</td><td>5,200</td><td style="color:#4affb0;">+1.2%</td></tr>
        <tr><td>ناسداك</td><td>16,500</td><td style="color:#4affb0;">+1.5%</td></tr>
    </table>"""
    return render_template_string(PAGE, content=content)

@app.route('/blockchain')
def blockchain():
    if 'user' not in session: return redirect('/login')
    content = """
    <h2 style="text-align:center;font-size:1.5rem;color:#00c8ff;">🔗 بلوكتشين</h2>
    <table>
        <tr><th>العملة</th><th>السعر</th></tr>
        <tr><td>بيتكوين</td><td>67,250</td></tr>
        <tr><td>إيثريوم</td><td>3,450</td></tr>
    </table>"""
    return render_template_string(PAGE, content=content)

@app.route('/income_detail')
def income_detail():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0"); expenses = abs(c.fetchone()[0])
    conn.close()
    profit = revenue - expenses
    content = f"""
    <h2 style="text-align:center;font-size:1.5rem;color:#4affb0;">📊 قائمة الدخل</h2>
    <table>
        <tr><th>البند</th><th>القيمة</th></tr>
        <tr><td>💰 الإيرادات</td><td style="color:#4affb0;">{revenue}</td></tr>
        <tr><td>📉 المصاريف</td><td style="color:#ff4a4a;">{expenses}</td></tr>
        <tr><td>📈 صافي الربح</td><td style="color:#FFD700;font-size:1rem;">{profit}</td></tr>
    </table>"""
    return render_template_string(PAGE, content=content)

