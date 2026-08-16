from flask import Flask, request, session, redirect, render_template_string
import sqlite3

app = Flask(__name__)
from finance_extra import extra
app.register_blueprint(extra)
app.secret_key = 'core_2026'
DB = 'core_finance.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, name TEXT, type TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT);
    CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER);
    CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS bank_moves (id INTEGER PRIMARY KEY, date TEXT, desc TEXT, amount REAL);
    ''')
    c.execute("SELECT COUNT(*) FROM accounts")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO accounts (name, type, balance) VALUES ('النقدية','أصول',50000)")
        c.execute("INSERT INTO accounts (name, type, balance) VALUES ('البنك','أصول',150000)")
        c.execute("INSERT INTO customers (name, phone) VALUES ('شركة الأمل','0501234567')")
        c.execute("INSERT INTO customers (name, phone) VALUES ('مؤسسة النور','0507654321')")
        c.execute("INSERT INTO products (name, price, stock) VALUES ('منتج أ',100,50)")
        c.execute("INSERT INTO products (name, price, stock) VALUES ('منتج ب',200,30)")
        c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (1,15000,'2026-08-01')")
        c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (2,25000,'2026-08-05')")
        c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES ('2026-08-01','إيداع',50000)")
        conn.commit()
    conn.close()

init_db()

PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>نوح المالي</title>
<style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { font-family:Tahoma; background:linear-gradient(135deg,#0a0a2e,#1a0a3e); color:#fff; padding:20px; }
    .container { max-width:1200px; margin:0 auto; background:rgba(20,20,50,0.85); border-radius:30px; padding:30px; border:2px solid rgba(255,215,0,0.4); box-shadow:0 20px 50px rgba(0,0,0,0.6), 0 0 40px rgba(255,215,0,0.2); }
    h1 { text-align:center; color:#FFD700; font-size:2.5rem; text-shadow:0 0 20px rgba(255,215,0,0.5); }
    h2 { color:#FFD700; margin-bottom:20px; }
    .nav-btn { display:inline-block; margin:6px; padding:10px 20px; border-radius:25px; text-decoration:none; font-weight:bold; transition:all 0.3s; animation: float-icon 2.5s ease-in-out infinite; }
    .nav-btn:hover { transform:scale(1.1); }
    .nav-btn span { display:inline-block; animation: spin-icon 3s linear infinite; }
    .nav-btn.gold { border:2px solid #FFD700; color:#FFD700; animation: glow-gold 1.8s infinite alternate, float-icon 2.5s ease-in-out infinite; }
    .nav-btn.blue { border:2px solid #00c8ff; color:#00c8ff; animation: glow-blue 1.8s infinite alternate, float-icon 2.5s ease-in-out infinite; }
    .nav-btn.green { border:2px solid #4affb0; color:#4affb0; animation: glow-green 1.8s infinite alternate, float-icon 2.5s ease-in-out infinite; }
    .nav-btn.red { border:2px solid #ff4a4a; color:#ff4a4a; animation: glow-red 1.8s infinite alternate, float-icon 2.5s ease-in-out infinite; }
    @keyframes glow-gold { 0% { box-shadow:0 0 5px rgba(255,215,0,0.4); } 100% { box-shadow:0 0 25px rgba(255,215,0,0.9); } }
    @keyframes glow-blue { 0% { box-shadow:0 0 5px rgba(0,200,255,0.4); } 100% { box-shadow:0 0 25px rgba(0,200,255,0.9); } }
    @keyframes glow-green { 0% { box-shadow:0 0 5px rgba(74,255,176,0.4); } 100% { box-shadow:0 0 25px rgba(74,255,176,0.9); } }
    @keyframes glow-red { 0% { box-shadow:0 0 5px rgba(255,74,74,0.4); } 100% { box-shadow:0 0 25px rgba(255,74,74,0.9); } }
    @keyframes float-icon { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-5px); } }
    @keyframes spin-icon { 0% { transform:rotate(0deg); } 100% { transform:rotate(360deg); } }
    input, select, button { padding:10px; margin:5px; background:#1a1a3e; color:#fff; border:1px solid #FFD700; border-radius:8px; }
    button { background:#FFD700; color:#000; font-weight:bold; cursor:pointer; }
    table { width:100%; border-collapse:separate; border-spacing:0; margin-top:20px; box-shadow:0 15px 40px rgba(0,0,0,0.5), 0 0 25px rgba(255,215,0,0.15); border-radius:15px; overflow:hidden; }
    table thead th { background:linear-gradient(145deg,#FFD700,#FF8C00); color:#000; padding:15px; font-size:1.1rem; text-shadow:0 1px 2px rgba(255,255,255,0.3); }
    table tbody td { padding:12px; border-bottom:1px solid rgba(255,215,0,0.15); transition:all 0.3s; }
    table tbody tr:hover { background:rgba(255,215,0,0.08); transform:scale(1.01); }
    table tbody tr:nth-child(even) { background:rgba(255,255,255,0.02); }
    th, td { border:1px solid #444; padding:10px; text-align:center; }
    th { animation: th-glow 2s ease-in-out infinite; }
    @keyframes th-glow { 0%,100% { box-shadow:0 0 5px rgba(255,215,0,0.3); } 50% { box-shadow:0 0 20px rgba(255,215,0,0.6); } }
    tr:hover td { background:rgba(255,215,0,0.05); }
    a { text-decoration:none; }
</style></head>
<body>
<div class="container">
    {{ content | safe }}
</div>
</body></html>'''



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['user'] = 'admin'
        return redirect('/dashboard')
    return '<h2>🦅 دخول</h2><form method="POST"><input name="username" placeholder="المستخدم"><input name="password" type="password" placeholder="كلمة المرور"><button>دخول</button></form>'

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
    conn.close()
    content = f"""
    <h1 style="text-align:center;color:#FFD700;">🦅 لوحة نوح المالية</h1>
    <p style="text-align:center;color:#aaa;">النظام المالي الأسطوري المتكامل</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;margin:30px 0;">
        <div style="background:#1a1a3e;padding:25px;border-radius:20px;border:2px solid #FFD700;text-align:center;"><h2>{accounts}</h2>حسابات</div>
        <div style="background:#1a1a3e;padding:25px;border-radius:20px;border:2px solid #00c8ff;text-align:center;"><h2>{customers}</h2>عملاء</div>
        <div style="background:#1a1a3e;padding:25px;border-radius:20px;border:2px solid #4affb0;text-align:center;"><h2>{invoices}</h2>فواتير</div>
        <div style="background:#1a1a3e;padding:25px;border-radius:20px;border:2px solid #FFD700;text-align:center;"><h2>{products}</h2>منتجات</div>
        <div style="background:#1a1a3e;padding:25px;border-radius:20px;border:2px solid #00c8ff;text-align:center;"><h2>{revenue}</h2>إيرادات</div>
    </div>
    <div style="text-align:center;">
        <a href="/accounts" class="nav-btn gold"><span>📚</span> الحسابات</a>
        <a href="/customers" class="nav-btn blue"><span>👥</span> العملاء</a>
        <a href="/invoices" class="nav-btn green"><span>🧾</span> الفواتير</a>
        <a href="/products" class="nav-btn gold"><span>📦</span> المنتجات</a>
        <a href="/bank" class="nav-btn blue"><span>🏦</span> البنك</a>
        <a href="/zakat" class="nav-btn green"><span>🕌</span> الزكاة</a>
        <a href="/debts" class="nav-btn gold"><span>💳</span> الديون</a>
        <a href="/budgets" class="nav-btn blue"><span>📋</span> الميزانيات</a>
        <a href="/assets" class="nav-btn green"><span>🏢</span> الأصول</a>
        <a href="/currencies" class="nav-btn gold"><span>💱</span> العملات</a>
        <a href="/ledger" class="nav-btn blue"><span>📒</span> الأستاذ</a>
        <a href="/cashflow" class="nav-btn green"><span>💵</span> التدفقات</a>
        <a href="/ai_forecast" class="nav-btn gold"><span>🧠</span> تنبؤ</a>
        <a href="/economic_indicators" class="nav-btn blue"><span>📈</span> مؤشرات</a>
        <a href="/stock_market" class="nav-btn green"><span>💰</span> أسهم</a>
        <a href="/blockchain" class="nav-btn gold"><span>🔗</span> بلوكتشين</a>
        <a href="/extra_home" class="nav-btn gold"><span>🚀</span> الموسع</a>
        <a href="/logout" class="nav-btn red"><span>🚪</span> خروج</a>
    </div>"""
    return render_template_string(PAGE, content=content)

@app.route('/accounts')
def accounts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    rows = c.fetchall(); conn.close()
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#FFD700;">📚 الحسابات</h2>
        <p style="color:#aaa;">إدارة الحسابات العامة</p>
    </div>
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
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#00c8ff;">👥 العملاء</h2>
        <p style="color:#aaa;">إدارة علاقات العملاء</p>
    </div>
    <table><tr><th>ID</th><th>الاسم</th><th>الهاتف</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/invoices')
def invoices():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM invoices")
    rows = c.fetchall(); conn.close()
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#4affb0;">🧾 الفواتير</h2>
        <p style="color:#aaa;">إدارة الفواتير والمبيعات</p>
    </div>
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
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#FFD700;">📦 المنتجات</h2>
        <p style="color:#aaa;">إدارة المخزون والمنتجات</p>
    </div>
    <table><tr><th>ID</th><th>الاسم</th><th>السعر</th><th>المخزون</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/bank')
def bank():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM bank_moves")
    rows = c.fetchall(); conn.close()
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#00c8ff;">🏦 البنك</h2>
        <p style="color:#aaa;">الحركات البنكية</p>
    </div>
    <table><tr><th>ID</th><th>التاريخ</th><th>الوصف</th><th>المبلغ</th></tr>"""
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)



@app.route('/assets')
def assets():
    if 'user' not in session: return redirect('/login')
    content = "<h2>🏢 الأصول</h2><p>لا توجد أصول مسجلة</p>"
    return render_template_string(PAGE, content=content)

@app.route('/currencies')
def currencies():
    if 'user' not in session: return redirect('/login')
    content = "<h2>💱 العملات</h2><p>لا توجد عملات</p>"
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

@app.route('/cashflow')
def cashflow():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0"); inflow = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0"); outflow = c.fetchone()[0]
    conn.close()
    net = inflow + outflow
    content = f"<h2>💵 التدفقات النقدية</h2><p>داخل: {inflow}</p><p>خارج: {outflow}</p><p>صافي: {net}</p>"
    return render_template_string(PAGE, content=content)

@app.route('/ai_forecast')
def ai_forecast():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    conn.close()
    next_month = revenue * 1.15
    content = f"<h2>🧠 التنبؤ المالي</h2><p>الحالي: {revenue}</p><p>الشهر القادم: {next_month:.0f}</p>"
    return render_template_string(PAGE, content=content)

@app.route('/economic_indicators')
def economic_indicators():
    if 'user' not in session: return redirect('/login')
    content = "<h2>📈 المؤشرات الاقتصادية</h2><p>التضخم: 2.5%</p><p>البطالة: 5%</p>"
    return render_template_string(PAGE, content=content)

@app.route('/stock_market')
def stock_market():
    if 'user' not in session: return redirect('/login')
    content = "<h2>💰 سوق الأسهم</h2><p>المؤشر: +1.5%</p>"
    return render_template_string(PAGE, content=content)

@app.route('/blockchain')
def blockchain():
    if 'user' not in session: return redirect('/login')
    content = "<h2>🔗 بلوكتشين</h2><p>شبكة آمنة</p>"
    return render_template_string(PAGE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

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
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#FFD700;">🕌 الزكاة</h2>
        <p style="color:#aaa;">حساب زكاة المال</p>
    </div>
    <table><tr><th>💰 النقود</th><th>📏 النصاب</th><th>🧮 المستحقة</th></tr>
    <tr><td>{total}</td><td>{nisab}</td><td style="color:#FFD700;font-size:1.5rem;">{due:.2f}</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/debts')
def debts():
    if 'user' not in session: return redirect('/login')
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#00c8ff;">💳 الديون</h2>
        <p style="color:#aaa;">إدارة الديون المستحقة</p>
    </div>
    <table><tr><th>ID</th><th>الاسم</th><th>المبلغ</th><th>النوع</th></tr>
    <tr><td colspan="4" style="text-align:center;color:#888;">لا توجد ديون مسجلة</td></tr></table>"""
    return render_template_string(PAGE, content=content)

@app.route('/budgets')
def budgets():
    if 'user' not in session: return redirect('/login')
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#4affb0;">📋 الميزانيات</h2>
        <p style="color:#aaa;">تخطيط الميزانيات المالية</p>
    </div>
    <table><tr><th>ID</th><th>الاسم</th><th>المبلغ</th></tr>
    <tr><td colspan="3" style="text-align:center;color:#888;">لا توجد ميزانيات</td></tr></table>"""
    return render_template_string(PAGE, content=content)
