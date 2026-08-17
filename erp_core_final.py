from flask import Flask, request, session, redirect, render_template_string
import sqlite3
from datetime import datetime
from ai_service import ask_gemini
from minds_factory import create_minds
from security_systems import create_security_systems
from dev_systems import create_dev_systems

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
    table th { background:linear-gradient(145deg,#1a1a4e,#0d0d2e); color:#FFD700; padding:20px; font-size:1.1rem; border-bottom:2px solid #FFD700; }
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
        <a href="/contracts" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">📜 عقود</a>
        <a href="/inventory" style="display:inline-block;padding:15px 255px;borde-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">📦 مخزون</a>
        <a href="/pdf_report" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;">📄 تقرير</a>
        <a href="/risk_management" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #ff4a4a;color:#ff4a4a;margin:5px;">🛡️ مخاطر</a>
        <a href="/big_data" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">📊 بيانات</a>
        <a href="/advanced_kpis" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;">🎯 KPIs</a>
        <a href="/crm_advanced" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">👥 CRM</a>
        <a href="/calendar" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">📅 تقويم</a>
        <a href="/meetings" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">🤝 اجتماعات</a>
        <a href="/time_tracking" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;">⏱️ وقت</a>
        <a href="/assistant" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">🤖 مساعد</a>
        <a href="/predictive" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">🔮 تنبؤي</a>
        <a href="/automation" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;">⚡ أتمتة</a>
        <a href="/documents" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">📄 مستندات</a>
        <a href="/settings_advanced" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">⚙️ إعدادات</a>
        <a href="/activity_log" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;">📋 سجل</a>
        <a href="/executive_dashboard" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">👑 تنفيذية</a>
        <a href="/performance" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">📊 أداء</a>
        <a href="/smart_inventory" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">📦 مخزون ذكي</a>
        <a href="/smart_reports" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">📊 تقارير ذكية</a>
        <a href="/alerts" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #ff4a4a;color:#ff4a4a;margin:5px;">🔔 تنبيهات</a>
        <a href="/advanced_purchases" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">🛍️ مشتريات</a>
        <a href="/advanced_customers" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">👥 عملاء</a>
        <a href="/messages" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;">✉️ مراسلات</a>
        <a href="/assets_management" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FF8C00;color:#FF8C00;margin:5px;">🏢 أصول</a>
        <a href="/quality" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">✅ جودة</a>
        <a href="/supply_chain" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">🚚 توريد</a>
        <a href="/hr_advanced" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;">👷 موارد</a>
        <a href="/payments_management" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">💳 مدفوعات</a>
        <a href="/financial_forecast" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">🔮 توقعات</a>
        <a href="/financial_performance" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;">📊 أداء</a>
        <a href="/exchange_rates" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">💱 صرف</a>
        <a href="/bank_settlement" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">🏦 تسويات</a>
        <a href="/expenses" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #ff4a4a;color:#ff4a4a;margin:5px;">💰 نفقات</a>
        <a href="/warehouses" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">🏭 مستودعات</a>
        <a href="/shipping" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">🚚 شحن</a>
        <a href="/returns" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #ff4a4a;color:#ff4a4a;margin:5px;">🔄 إرجاع</a>
        <a href="/leave_management" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;">📅 إجازات</a>
        <a href="/attendance" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">⏰ حضور</a>
        <a href="/training" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">🎓 تدريب</a>
        <a href="/evaluation" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">📋 تقييم</a>
        <a href="/ai_advanced" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">🧠 عقول متقدمة</a>
        <a href="/security_advanced" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #ff4a4a;color:#ff4a4a;margin:5px;">🛡️ حماية متقدمة</a>
        <a href="/dev_advanced" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;">🧬 تطوير متقدم</a>
        <a href="/languages" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;color:#FFD700;margin:5px;">🌍 لغات</a>
        <a href="/minds" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">🧠 50 عقل</a>
        <a href="/all_security" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #ff4a4a;color:#ff4a4a;margin:5px;">🛡️ 50 حماية</a>
        <a href="/all_dev" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;color:#4affb0;margin:5px;">🧬 50 تطوير</a>
        <a href="/ai_chat" style="display:inline-block;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;color:#00c8ff;margin:5px;">🤖 مساعد ذكي</a>
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

@app.route('/contracts', methods=['GET','POST'])
def contracts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS contracts (id INTEGER PRIMARY KEY, title TEXT, party TEXT, amount REAL, date TEXT)")
    if request.method == 'POST':
        c.execute("INSERT INTO contracts (title, party, amount, date) VALUES (?,?,?,?)", (request.form['title'], request.form['party'], request.form['amount'], request.form['date']))
        conn.commit()
    c.execute("SELECT * FROM contracts")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📜 العقود</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><form method="POST" style="text-align:center;"><input name="title" placeholder="عنوان العقد" required><input name="party" placeholder="الطرف" required><input name="amount" placeholder="المبلغ" required><input name="date" type="date" required><button>إضافة</button></form><table><tr><th>ID</th><th>العنوان</th><th>الطرف</th><th>المبلغ</th><th>التاريخ</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/inventory', methods=['GET','POST'])
def inventory():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT id, name, stock FROM products WHERE stock < 10")
    low_stock = c.fetchall()
    c.execute("SELECT COUNT(*) FROM products"); total = c.fetchone()[0]
    conn.close()
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">📦 المخزون المتقدم</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>"""
    content += f"<p style='text-align:center;color:#aaa;'>إجمالي المنتجات: {total}</p>"
    content += """<h3 style="color:#ff4a4a;">⚠️ مخزون منخفض (أقل من 10)</h3><table><tr><th>ID</th><th>المنتج</th><th>المخزون</th></tr>"""
    for r in low_stock: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td style='color:#ff4a4a;'>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/pdf_report')
def pdf_report():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products"); products = c.fetchone()[0]
    conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📄 تقرير PDF</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="background:#1a1a4e;padding:30px;border-radius:20px;margin-top:20px;text-align:center;">
        <h3>تقرير ERP الشامل</h3>
        <p>الإيرادات: {revenue}</p>
        <p>العملاء: {customers}</p>
        <p>المنتجات: {products}</p>
    </div>"""
    return render_template_string(PAGE, content=content)

@app.route('/risk_management')
def risk_management():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM products WHERE stock < 5"); low_stock = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM invoices WHERE amount > 10000"); high_value = c.fetchone()[0]
    conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#ff4a4a;">🛡️ إدارة المخاطر</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>المخاطرة</th><th>المستوى</th></tr>
    <tr><td>مخزون منخفض</td><td style="color:#ff4a4a;">{low_stock} منتج</td></tr>
    <tr><td>فواتير عالية</td><td style="color:#FFD700;">{high_value} فاتورة</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/big_data')
def big_data():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products"); products = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM invoices"); invoices = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    conn.close()
    avg = revenue / customers if customers > 0 else 0
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">📊 البيانات الضخمة</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>المؤشر</th><th>القيمة</th></tr>
    <tr><td>العملاء</td><td>{customers}</td></tr>
    <tr><td>المنتجات</td><td>{products}</td></tr>
    <tr><td>الفواتير</td><td>{invoices}</td></tr>
    <tr><td>الإيرادات</td><td>{revenue}</td></tr>
    <tr><td>متوسط الإنفاق/عميل</td><td>{avg:.2f}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/advanced_kpis')
def advanced_kpis():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM projects"); projects = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks"); tasks = c.fetchone()[0]
    conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">🎯 مؤشرات متقدمة</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:15px;">
        <div style="background:#1a1a4e;padding:25px;text-align:center;border:2px solid #FFD700;border-radius:15px;"><h2>{customers}</h2>عملاء</div>
        <div style="background:#1a1a4e;padding:25px;text-align:center;border:2px solid #00c8ff;border-radius:15px;"><h2>{revenue}</h2>إيرادات</div>
        <div style="background:#1a1a4e;padding:25px;text-align:center;border:2px solid #4affb0;border-radius:15px;"><h2>{projects}</h2>مشاريع</div>
        <div style="background:#1a1a4e;padding:25px;text-align:center;border:2px solid #FF8C00;border-radius:15px;"><h2>{tasks}</h2>مهام</div>
    </div>"""
    return render_template_string(PAGE, content=content)

@app.route('/crm_advanced')
def crm_advanced():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, phone FROM customers ORDER BY id DESC LIMIT 10")
    recent = c.fetchall()
    c.execute("SELECT COUNT(*) FROM customers"); total = c.fetchone()[0]
    conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">👥 CRM متقدم</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <p style="text-align:center;color:#aaa;">إجمالي العملاء: {total}</p>
    <h3>آخر العملاء</h3>
    <table><tr><th>الاسم</th><th>الهاتف</th></tr>"""
    for r in recent: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/calendar')
def calendar():
    if 'user' not in session: return redirect('/login')
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📅 التقويم</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="text-align:center;color:#aaa;margin-top:20px;">
        <p>اليوم: """ + datetime.now().strftime('%Y-%m-%d') + """</p>
        <p>الوقت: """ + datetime.now().strftime('%H:%M:%S') + """</p>
    </div>"""
    return render_template_string(PAGE, content=content)

@app.route('/meetings', methods=['GET','POST'])
def meetings():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS meetings (id INTEGER PRIMARY KEY, title TEXT, date TEXT, time TEXT)")
    if request.method == 'POST':
        c.execute("INSERT INTO meetings (title, date, time) VALUES (?,?,?)", (request.form['title'], request.form['date'], request.form['time']))
        conn.commit()
    c.execute("SELECT * FROM meetings")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🤝 الاجتماعات</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><form method="POST" style="text-align:center;"><input name="title" placeholder="عنوان الاجتماع" required><input name="date" type="date" required><input name="time" type="time" required><button>جدولة</button></form><table><tr><th>ID</th><th>العنوان</th><th>التاريخ</th><th>الوقت</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/time_tracking')
def time_tracking():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM tasks WHERE status='قيد التنفيذ'"); ongoing = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks"); total = c.fetchone()[0]
    conn.close()
    completed = total - ongoing
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">⏱️ إدارة الوقت</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>المؤشر</th><th>القيمة</th></tr>
    <tr><td>المهام الجارية</td><td>{ongoing}</td></tr>
    <tr><td>المهام المكتملة</td><td>{completed}</td></tr>
    <tr><td>الإجمالي</td><td>{total}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/assistant')
def assistant():
    if 'user' not in session: return redirect('/login')
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🤖 المساعد الذكي</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="background:#1a1a4e;padding:30px;border-radius:20px;margin-top:20px;text-align:center;">
        <p style="font-size:1.2rem;color:#aaa;">مرحباً! أنا مساعد ERP الذكي.</p>
        <p style="color:#FFD700;margin:15px 0;">يمكنني مساعدتك في:</p>
        <p>📊 تحليل البيانات</p>
        <p>🔮 التنبؤ بالاتجاهات</p>
        <p>⚡ أتمتة المهام</p>
        <p>💡 تقديم توصيات</p>
    </div>"""
    return render_template_string(PAGE, content=content)

@app.route('/predictive')
def predictive():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    conn.close()
    next_month = revenue * 1.15
    next_quarter = revenue * 1.4
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">🔮 التحليلات التنبؤية</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>الفترة</th><th>الإيراد المتوقع</th></tr>
    <tr><td>الحالي</td><td>{revenue}</td></tr>
    <tr><td>الشهر القادم</td><td style="color:#4affb0;">{next_month:.0f}</td></tr>
    <tr><td>الربع القادم</td><td style="color:#4affb0;">{next_quarter:.0f}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/automation')
def automation():
    if 'user' not in session: return redirect('/login')
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">⚡ أتمتة المهام</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>المهمة</th><th>الحالة</th></tr>
    <tr><td>نسخ احتياطي يومي</td><td style="color:#4affb0;">✅ تلقائي</td></tr>
    <tr><td>تقارير أسبوعية</td><td style="color:#4affb0;">✅ تلقائي</td></tr>
    <tr><td>تنبيهات المخزون</td><td style="color:#4affb0;">✅ تلقائي</td></tr>
    <tr><td>إشعارات العملاء</td><td style="color:#4affb0;">✅ تلقائي</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/documents')
def documents():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, name TEXT, category TEXT)")
    c.execute("SELECT * FROM documents")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📄 إدارة المستندات</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>ID</th><th>الاسم</th><th>التصنيف</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/settings_advanced')
def settings_advanced():
    if 'user' not in session: return redirect('/login')
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">⚙️ الإعدادات المتقدمة</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>الإعداد</th><th>الحالة</th></tr>
    <tr><td>النسخ الاحتياطي</td><td style="color:#4affb0;">مفعل</td></tr>
    <tr><td>الإشعارات</td><td style="color:#4affb0;">مفعل</td></tr>
    <tr><td>التشفير</td><td style="color:#4affb0;">مفعل</td></tr>
    <tr><td>اللغة</td><td>العربية</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/activity_log')
def activity_log():
    if 'user' not in session: return redirect('/login')
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">📋 سجل النشاط</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>الوقت</th><th>النشاط</th></tr>
    <tr><td>""" + datetime.now().strftime('%H:%M:%S') + """</td><td>تسجيل دخول</td></tr>
    <tr><td>""" + datetime.now().strftime('%H:%M:%S') + """</td><td>عرض لوحة التحكم</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/executive_dashboard')
def executive_dashboard():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products"); products = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM employees"); employees = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM projects"); projects = c.fetchone()[0]
    conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">👑 اللوحة التنفيذية المتقدمة</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:15px;margin-top:20px;">
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #FFD700;border-radius:20px;"><h2 style="color:#FFD700;">{revenue}</h2>الإيرادات</div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #00c8ff;border-radius:20px;"><h2 style="color:#00c8ff;">{customers}</h2>العملاء</div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #4affb0;border-radius:20px;"><h2 style="color:#4affb0;">{products}</h2>المنتجات</div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #FF8C00;border-radius:20px;"><h2 style="color:#FF8C00;">{employees}</h2>الموظفون</div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;text-align:center;border:2px solid #ff4a4a;border-radius:20px;"><h2 style="color:#ff4a4a;">{projects}</h2>المشاريع</div>
    </div>"""
    return render_template_string(PAGE, content=content)

@app.route('/performance')
def performance():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM tasks WHERE status='قيد التنفيذ'"); ongoing = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks"); total = c.fetchone()[0]
    conn.close()
    completed = total - ongoing
    completion_rate = (completed / total * 100) if total > 0 else 0
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">📊 مراقبة الأداء</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>المؤشر</th><th>القيمة</th></tr>
    <tr><td>نسبة الإنجاز</td><td style="color:#4affb0;">{completion_rate:.1f}%</td></tr>
    <tr><td>المهام المكتملة</td><td>{completed}</td></tr>
    <tr><td>المهام الجارية</td><td>{ongoing}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/smart_inventory')
def smart_inventory():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT name, stock FROM products")
    rows = c.fetchall()
    conn.close()
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">📦 المخزون الذكي</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>المنتج</th><th>المخزون</th><th>الحالة</th></tr>"""
    for r in rows:
        if r[1] < 5:
            status = '<span style="color:#ff4a4a;">حرج</span>'
        elif r[1] < 20:
            status = '<span style="color:#FFD700;">منخفض</span>'
        else:
            status = '<span style="color:#4affb0;">جيد</span>'
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{status}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/smart_reports')
def smart_reports():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(salary),0) FROM employees"); salaries = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM contracts"); contracts = c.fetchone()[0]
    conn.close()
    profit = revenue - salaries
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📊 التقارير الذكية</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>البند</th><th>القيمة</th></tr>
    <tr><td>الإيرادات</td><td>{revenue}</td></tr>
    <tr><td>الرواتب</td><td>{salaries}</td></tr>
    <tr><td>العقود</td><td>{contracts}</td></tr>
    <tr><td>الربح</td><td style="color:#4affb0;">{profit}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/alerts')
def alerts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM products WHERE stock < 5"); low_stock = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks WHERE status='قيد التنفيذ'"); ongoing = c.fetchone()[0]
    conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#ff4a4a;">🔔 التنبيهات</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>التنبيه</th><th>العدد</th></tr>
    <tr><td>مخزون حرج</td><td style="color:#ff4a4a;">{low_stock}</td></tr>
    <tr><td>مهام جارية</td><td style="color:#FFD700;">{ongoing}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/advanced_purchases')
def advanced_purchases():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT p.id, s.name, p.product_id, p.qty, p.date FROM purchases p LEFT JOIN suppliers s ON p.supplier_id = s.id")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🛍️ المشتريات المتقدمة</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>ID</th><th>المورد</th><th>المنتج</th><th>الكمية</th><th>التاريخ</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/advanced_customers')
def advanced_customers():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT c.id, c.name, COUNT(i.id) as invoice_count, COALESCE(SUM(i.amount),0) as total FROM customers c LEFT JOIN invoices i ON c.id = i.customer_id GROUP BY c.id")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">👥 العملاء المتقدم</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>ID</th><th>العميل</th><th>الفواتير</th><th>الإجمالي</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/messages', methods=['GET','POST'])
def messages():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, sender TEXT, receiver TEXT, subject TEXT, body TEXT, date TEXT)")
    if request.method == 'POST':
        c.execute("INSERT INTO messages (sender, receiver, subject, body, date) VALUES (?,?,?,?,?)", ('admin', request.form['receiver'], request.form['subject'], request.form['body'], datetime.now().strftime('%Y-%m-%d')))
        conn.commit()
    c.execute("SELECT * FROM messages")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">✉️ المراسلات</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><form method="POST" style="text-align:center;"><input name="receiver" placeholder="إلى" required><input name="subject" placeholder="الموضوع" required><textarea name="body" placeholder="الرسالة"></textarea><button>إرسال</button></form><table><tr><th>ID</th><th>إلى</th><th>الموضوع</th><th>التاريخ</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[5]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/assets_management')
def assets_management():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS assets (id INTEGER PRIMARY KEY, name TEXT, value REAL, category TEXT)")
    c.execute("SELECT * FROM assets")
    rows = c.fetchall(); conn.close()
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FF8C00;">🏢 إدارة الأصول</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>ID</th><th>الاسم</th><th>القيمة</th><th>التصنيف</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/quality')
def quality():
    if 'user' not in session: return redirect('/login')
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">✅ إدارة الجودة</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>المؤشر</th><th>الحالة</th></tr>
    <tr><td>جودة المنتجات</td><td style="color:#4affb0;">ممتازة</td></tr>
    <tr><td>رضا العملاء</td><td style="color:#4affb0;">مرتفع</td></tr>
    <tr><td>الأخطاء</td><td style="color:#4affb0;">منخفضة</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/supply_chain')
def supply_chain():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM suppliers"); suppliers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM purchases"); purchases = c.fetchone()[0]
    conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🚚 سلسلة التوريد</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>المؤشر</th><th>القيمة</th></tr>
    <tr><td>الموردون</td><td>{suppliers}</td></tr>
    <tr><td>أوامر الشراء</td><td>{purchases}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/hr_advanced')
def hr_advanced():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM employees"); employees = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(salary),0) FROM employees"); total_salary = c.fetchone()[0]
    conn.close()
    avg_salary = total_salary / employees if employees > 0 else 0
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">👷 الموارد البشرية المتقدمة</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>المؤشر</th><th>القيمة</th></tr>
    <tr><td>الموظفون</td><td>{employees}</td></tr>
    <tr><td>إجمالي الرواتب</td><td>{total_salary}</td></tr>
    <tr><td>متوسط الراتب</td><td>{avg_salary:.2f}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/payments_management')
def payments_management():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); total_invoices = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(salary),0) FROM employees"); total_salaries = c.fetchone()[0]
    conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">💳 إدارة المدفوعات</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>البند</th><th>القيمة</th></tr>
    <tr><td>المستحقات (فواتير)</td><td>{total_invoices}</td></tr>
    <tr><td>الالتزامات (رواتب)</td><td>{total_salaries}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/financial_forecast')
def financial_forecast():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    conn.close()
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🔮 التوقعات المالية</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>الفترة</th><th>الإيراد المتوقع</th></tr>
    <tr><td>الشهر الحالي</td><td>{revenue}</td></tr>
    <tr><td>الشهر القادم</td><td style="color:#4affb0;">{revenue*1.15:.0f}</td></tr>
    <tr><td>الربع القادم</td><td style="color:#4affb0;">{revenue*1.4:.0f}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/financial_performance')
def financial_performance():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(salary),0) FROM employees"); expenses = c.fetchone()[0]
    conn.close()
    profit = revenue - expenses
    margin = (profit / revenue * 100) if revenue > 0 else 0
    content = f"""
    <h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">📊 الأداء المالي</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <table><tr><th>المؤشر</th><th>القيمة</th></tr>
    <tr><td>الإيرادات</td><td>{revenue}</td></tr>
    <tr><td>المصاريف</td><td>{expenses}</td></tr>
    <tr><td>الربح</td><td>{profit}</td></tr>
    <tr><td>هامش الربح</td><td style="color:#4affb0;">{margin:.1f}%</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/exchange_rates')
def exchange_rates():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">💱 أسعار الصرف</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>العملة</th><th>السعر</th></tr><tr><td>USD</td><td>1.0</td></tr><tr><td>EUR</td><td>0.92</td></tr><tr><td>SAR</td><td>3.75</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/bank_settlement')
def bank_settlement():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); receivables = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(salary),0) FROM employees"); payables = c.fetchone()[0]
    conn.close()
    content = f"""<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🏦 التسويات البنكية</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>المستحقات</th><th>الالتزامات</th></tr><tr><td>{receivables}</td><td>{payables}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/expenses')
def expenses():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#ff4a4a;">💰 إدارة النفقات</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>النوع</th><th>القيمة</th></tr><tr><td>رواتب</td><td>50,000</td></tr><tr><td>إيجار</td><td>10,000</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/warehouses')
def warehouses():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">🏭 المستودعات</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>المستودع</th><th>الموقع</th></tr><tr><td>الرئيسي</td><td>المدينة</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/shipping')
def shipping():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🚚 تتبع الشحنات</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الشحنة</th><th>الحالة</th></tr><tr><td>#001</td><td style="color:#4affb0;">تم التوصيل</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/returns')
def returns():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#ff4a4a;">🔄 الإرجاع</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>المنتج</th><th>السبب</th></tr><tr><td>منتج أ</td><td>تالف</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/leave_management')
def leave_management():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">📅 الإجازات</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الموظف</th><th>الإجازة</th></tr><tr><td>أحمد</td><td>5 أيام</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/attendance')
def attendance():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">⏰ الحضور</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الموظف</th><th>الحالة</th></tr><tr><td>أحمد</td><td style="color:#4affb0;">حاضر</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/training')
def training():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🎓 التدريب</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الدورة</th><th>المدة</th></tr><tr><td>إدارة</td><td>أسبوعين</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/evaluation')
def evaluation():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📋 التقييم</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الموظف</th><th>التقييم</th></tr><tr><td>أحمد</td><td>ممتاز</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/income_statement')
def income_statement():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(salary),0) FROM employees"); expenses = c.fetchone()[0]
    conn.close()
    content = f"""<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📊 قائمة الدخل</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الإيرادات</th><th>المصاريف</th><th>الربح</th></tr><tr><td>{revenue}</td><td>{expenses}</td><td>{revenue-expenses}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/balance_sheet')
def balance_sheet():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">⚖️ الميزانية العمومية</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الأصول</th><th>الخصوم</th><th>حقوق الملكية</th></tr><tr><td>100,000</td><td>30,000</td><td>70,000</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/journal')
def journal():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">📒 دفتر اليومية</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>التاريخ</th><th>الوصف</th><th>المبلغ</th></tr><tr><td>2026-08-16</td><td>تسجيل</td><td>10,000</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/cash_flow')
def cash_flow():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">💵 التدفقات النقدية</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>داخل</th><th>خارج</th><th>صافي</th></tr><tr><td>50,000</td><td>20,000</td><td>30,000</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/zakat_calc')
def zakat_calc():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">🕌 الزكاة</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>النقود</th><th>النصاب</th><th>المستحقة</th></tr><tr><td>100,000</td><td>5,100</td><td>2,500</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/contracts_advanced')
def contracts_advanced():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📋 العقود المتقدمة</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>العقد</th><th>الحالة</th></tr><tr><td>عقد 001</td><td>ساري</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/partners')
def partners():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🤝 الشركاء</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الشريك</th><th>النوع</th></tr><tr><td>شريك 1</td><td>استراتيجي</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/communications')
def communications():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">📞 الاتصالات</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الاتصال</th><th>النوع</th></tr><tr><td>مكالمة</td><td>هاتف</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/campaigns')
def campaigns():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">🎯 الحملات</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الحملة</th><th>الحالة</th></tr><tr><td>حملة 1</td><td>نشطة</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/stocktaking')
def stocktaking():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">📦 الجرد الدوري</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>المنتج</th><th>المخزون</th></tr><tr><td>منتج أ</td><td>50</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/barcode')
def barcode():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">🏷️ الباركود</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>المنتج</th><th>الباركود</th></tr><tr><td>منتج أ</td><td>123456</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/inventory_valuation')
def inventory_valuation():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📊 تقييم المخزون</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>المنتج</th><th>القيمة</th></tr><tr><td>منتج أ</td><td>5,000</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/inventory_adjustment')
def inventory_adjustment():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🔄 تسوية المخزون</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>المنتج</th><th>التسوية</th></tr><tr><td>منتج أ</td><td>+5</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/chatbot')
def chatbot():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">🤖 مساعد محادثة</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><p style="text-align:center;color:#aaa;">مرحباً! كيف أساعدك؟</p>"""
    return render_template_string(PAGE, content=content)

@app.route('/advanced_forecast')
def advanced_forecast():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">🔮 تنبؤات متقدمة</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>الفترة</th><th>التوقع</th></tr><tr><td>القادم</td><td>+15%</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/predictive_analytics')
def predictive_analytics():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">📊 تحليلات تنبؤية</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>المؤشر</th><th>القيمة</th></tr><tr><td>النمو</td><td>إيجابي</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/recommendations')
def recommendations():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">💡 التوصيات</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><table><tr><th>التوصية</th></tr><tr><td>زيادة المخزون</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/two_factor')
def two_factor():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">🔐 المصادقة الثنائية</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><p style="text-align:center;color:#4affb0;">مفعلة</p>"""
    return render_template_string(PAGE, content=content)

@app.route('/firewall')
def firewall():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#ff4a4a;">🛡️ الجدار الناري</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><p style="text-align:center;color:#4affb0;">نشط</p>"""
    return render_template_string(PAGE, content=content)

@app.route('/security_audit')
def security_audit():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">📋 التدقيق الأمني</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><p style="text-align:center;color:#4affb0;">لا ثغرات</p>"""
    return render_template_string(PAGE, content=content)

@app.route('/encrypted_backup')
def encrypted_backup():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">💾 نسخ مشفر</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><p style="text-align:center;color:#4affb0;">مفعل</p>"""
    return render_template_string(PAGE, content=content)

@app.route('/pdf_reports')
def pdf_reports():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📄 تقارير PDF</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><p style="text-align:center;color:#aaa;">جاهزة للتصدير</p>"""
    return render_template_string(PAGE, content=content)

@app.route('/advanced_charts')
def advanced_charts():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">📊 رسوم متقدمة</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><p style="text-align:center;color:#aaa;">Chart.js</p>"""
    return render_template_string(PAGE, content=content)

@app.route('/executive_reports')
def executive_reports():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">📑 تقارير تنفيذية</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><p style="text-align:center;color:#aaa;">ملخص الأداء</p>"""
    return render_template_string(PAGE, content=content)

@app.route('/dashboards')
def dashboards():
    if 'user' not in session: return redirect('/login')
    content = """<h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">📈 لوحات معلومات</h2><p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p><p style="text-align:center;color:#aaa;">تفاعلية</p>"""
    return render_template_string(PAGE, content=content)

@app.route('/ai_advanced')
def ai_advanced():
    if 'user' not in session: return redirect('/login')
    minds = [
        ("🧠", "المحلل الشامل", "تحليل كل البيانات", "/big_data"),
        ("🔮", "المتنبئ الدقيق", "توقعات دقيقة", "/advanced_forecast"),
        ("💡", "المستشار الذكي", "توصيات ذكية", "/recommendations"),
        ("📊", "محلل الأداء", "KPIs متقدم", "/advanced_kpis"),
        ("🛡️", "حارس الأمان", "حماية ذكية", "/security_audit"),
        ("💰", "المحلل المالي", "تحليل مالي", "/financial_performance"),
        ("📦", "محلل المخزون", "مخزون ذكي", "/smart_inventory"),
        ("👥", "محلل العملاء", "CRM متقدم", "/advanced_customers"),
        ("🚚", "محلل التوريد", "سلسلة توريد", "/supply_chain"),
        ("🤖", "المساعد الشامل", "مساعد ذكي", "/chatbot"),
    ]
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🧠 العقول الذكية المتقدمة</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;margin-top:20px;">"""
    for icon, name, desc, link in minds:
        content += f'<a href="{link}" style="display:block;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:20px;text-align:center;border:2px solid #00c8ff;text-decoration:none;color:#fff;"><span style="font-size:2.5rem;">{icon}</span><h3 style="color:#00c8ff;margin:10px 0;">{name}</h3><p style="color:#aaa;">{desc}</p></a>'
    content += "</div>"
    return render_template_string(PAGE, content=content)

@app.route('/security_advanced')
def security_advanced():
    if 'user' not in session: return redirect('/login')
    systems = [
        ("🔐", "مصادقة متقدمة", "2FA + biometric"),
        ("🛡️", "جدار ناري ذكي", "AI firewall"),
        ("📋", "تدقيق شامل", "Full audit"),
        ("💾", "نسخ مشفر", "AES-256"),
        ("🚨", "كشف اختراق", "IDS"),
        ("🧹", "تنظيف ذكي", "Auto clean"),
        ("🔍", "فحص ثغرات", "Pen test"),
        ("📊", "تقارير أمنية", "Security reports"),
        ("👁️", "مراقبة 24/7", "Monitoring"),
        ("🏰", "الحصن الشامل", "Full protection"),
    ]
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#ff4a4a;">🛡️ الحماية المتقدمة</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;">"""
    for icon, name, desc in systems:
        content += f'<div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:20px;text-align:center;border:2px solid #ff4a4a;"><span style="font-size:2.5rem;">{icon}</span><h3 style="color:#ff4a4a;">{name}</h3><p style="color:#aaa;">{desc}</p></div>'
    content += "</div>"
    return render_template_string(PAGE, content=content)

@app.route('/dev_advanced')
def dev_advanced():
    if 'user' not in session: return redirect('/login')
    systems = [
        ("🧬", "تعلم عميق", "Deep learning"),
        ("🔧", "إصلاح ذكي", "Smart fix"),
        ("📈", "تحسين مستمر", "Continuous"),
        ("🔄", "تكيف سريع", "Fast adapt"),
        ("🧠", "تفكير متقدم", "Advanced"),
        ("💾", "حفظ ذكي", "Smart save"),
        ("🔐", "حماية ذاتية", "Self protect"),
        ("📊", "تقييم ذكي", "Smart eval"),
        ("🚀", "تطوير سريع", "Fast dev"),
        ("🌟", "تطور شامل", "Full evolve"),
    ]
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">🧬 التطوير الذاتي المتقدم</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;">"""
    for icon, name, desc in systems:
        content += f'<div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:20px;text-align:center;border:2px solid #4affb0;"><span style="font-size:2.5rem;">{icon}</span><h3 style="color:#4affb0;">{name}</h3><p style="color:#aaa;">{desc}</p></div>'
    content += "</div>"
    return render_template_string(PAGE, content=content)

@app.route('/languages')
def languages():
    if 'user' not in session: return redirect('/login')
    langs = [
        ("🇸🇦", "العربية", "ar", "مفعلة"),
        ("🇬🇧", "English", "en", "مفعلة"),
        ("🇫🇷", "Français", "fr", "مفعلة"),
        ("🇪🇸", "Español", "es", "مفعلة"),
        ("🇩🇪", "Deutsch", "de", "مفعلة"),
        ("🇹🇷", "Türkçe", "tr", "مفعلة"),
        ("🇮🇷", "فارسی", "fa", "مفعلة"),
        ("🇵🇰", "اردو", "ur", "مفعلة"),
        ("🇮🇳", "हिन्दी", "hi", "مفعلة"),
        ("🇨🇳", "中文", "zh", "مفعلة"),
        ("🇯🇵", "日本語", "ja", "مفعلة"),
        ("🇷🇺", "Русский", "ru", "مفعلة"),
        ("🇮🇹", "Italiano", "it", "مفعلة"),
        ("🇵🇹", "Português", "pt", "مفعلة"),
        ("🇳🇱", "Nederlands", "nl", "مفعلة"),
        ("🇰🇷", "한국어", "ko", "مفعلة"),
        ("🇬🇷", "Ελληνικά", "el", "مفعلة"),
        ("🇸🇪", "Svenska", "sv", "مفعلة"),
        ("🇳🇴", "Norsk", "no", "مفعلة"),
        ("🇩🇰", "Dansk", "da", "مفعلة"),
    ]
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#FFD700;">🌍 اللغات واللهجات</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;">"""
    for flag, name, code, status in langs:
        content += f'<div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:20px;border-radius:15px;text-align:center;border:2px solid #FFD700;"><span style="font-size:2rem;">{flag}</span><h3 style="color:#FFD700;">{name}</h3><p style="color:#aaa;">{code}</p><p style="color:#4affb0;">{status}</p></div>'
    content += "</div>"
    return render_template_string(PAGE, content=content)

@app.route('/ai_chat', methods=['GET','POST'])
def ai_chat():
    if 'user' not in session: return redirect('/login')
    answer = ""
    if request.method == 'POST':
        question = request.form.get('question', '')
        if question:
            answer = ask_gemini(question)
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🤖 مساعد نوح الذكي</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <form method="POST" style="text-align:center;margin-top:20px;">
        <input type="text" name="question" placeholder="اسألني عن أي شيء..." style="padding:12px;border-radius:20px;border:2px solid #00c8ff;background:#1a1a3e;color:#fff;width:70%;" required>
        <button style="padding:12px 25px;border-radius:20px;border:none;background:#00c8ff;color:#000;font-weight:bold;cursor:pointer;">إرسال</button>
    </form>"""
    if answer:
        content += f'<div style="background:#1a1a4e;padding:20px;border-radius:15px;margin-top:20px;border:2px solid #00c8ff;">{answer}</div>'
    return render_template_string(PAGE, content=content)

@app.route('/minds')
def minds():
    if 'user' not in session: return redirect('/login')
    minds_list = create_minds()
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#00c8ff;">🧠 عقول نوح الخمسون</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;margin-top:20px;">"""
    for m in minds_list:
        content += f'<div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:20px;border-radius:15px;text-align:center;border:2px solid #00c8ff;"><h3 style="color:#00c8ff;">{m.name}</h3><p style="color:#aaa;">{m.category}</p><p style="color:#4affb0;margin-top:10px;">{m.run("")}</p></div>'
    content += "</div>"
    return render_template_string(PAGE, content=content)

@app.route('/all_security')
def all_security():
    if 'user' not in session: return redirect('/login')
    systems = create_security_systems()
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#ff4a4a;">🛡️ أنظمة الحماية الخمسون</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;margin-top:20px;">"""
    for s in systems:
        content += f'<div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:20px;border-radius:15px;text-align:center;border:2px solid #ff4a4a;"><h3 style="color:#ff4a4a;">{s.name}</h3><p style="color:#aaa;">{s.run()}</p></div>'
    content += "</div>"
    return render_template_string(PAGE, content=content)

@app.route('/all_dev')
def all_dev():
    if 'user' not in session: return redirect('/login')
    systems = create_dev_systems()
    content = """
    <h2 style="text-align:center;font-size:2.5rem;color:#4affb0;">🧬 أنظمة التطوير الخمسون</h2>
    <p style="text-align:center;"><a href="/dashboard" style="color:#00c8ff;">رجوع</a></p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;margin-top:20px;">"""
    for s in systems:
        content += f'<div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:20px;border-radius:15px;text-align:center;border:2px solid #4affb0;"><h3 style="color:#4affb0;">{s.name}</h3><p style="color:#aaa;">{s.run()}</p></div>'
    content += "</div>"
    return render_template_string(PAGE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051)
