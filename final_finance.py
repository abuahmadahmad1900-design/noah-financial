from flask import Flask, request, session, redirect, render_template_string
import sqlite3

app = Flask(__name__)
app.secret_key = 'final_2026'
DB = 'finance.db'

def init_db()

conn = sqlite3.connect(DB)
c = conn.cursor()
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
conn.close():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, name TEXT, type TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT);
    CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER);
    CREATE TABLE IF NOT EXISTS bank_moves (id INTEGER PRIMARY KEY, date TEXT, desc TEXT, amount REAL);
    ''')
    conn.commit()
    conn.close()

init_db()

PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>نوح المالي</title></head>
<body style="font-family:Tahoma;background:#0a0a2e;color:#fff;padding:20px;">
{{ content | safe }}
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
    conn.close()
    content = f'''
    <h1 style="text-align:center;color:#FFD700;">🦅 لوحة نوح المالية</h1>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;">
        <div style="background:#1a1a3e;padding:20px;text-align:center;"><h2>{accounts}</h2>حسابات</div>
        <div style="background:#1a1a3e;padding:20px;text-align:center;"><h2>{customers}</h2>عملاء</div>
        <div style="background:#1a1a3e;padding:20px;text-align:center;"><h2>{invoices}</h2>فواتير</div>
        <div style="background:#1a1a3e;padding:20px;text-align:center;"><h2>{products}</h2>منتجات</div>
    </div>
    <div style="margin-top:20px;text-align:center;">
        <a href="/accounts" style="color:#FFD700;">📚 الحسابات</a> |
        <a href="/customers" style="color:#FFD700;">👥 العملاء</a> |
        <a href="/invoices" style="color:#FFD700;">🧾 الفواتير</a> |
        <a href="/products" style="color:#FFD700;">📦 المنتجات</a> |
        <a href="/bank" style="color:#FFD700;">🏦 البنك</a> |
        <a href="/zakat" style="color:#FFD700;">🕌 الزكاة</a> |
        <a href="/debts" style="color:#FFD700;">💳 الديون</a> |
        <a href="/budgets" style="color:#FFD700;">📋 الميزانيات</a> |
        <a href="/assets" style="color:#FFD700;">🏢 الأصول</a> |
        <a href="/currencies" style="color:#FFD700;">💱 العملات</a> |
        <a href="/ledger" style="color:#FFD700;">📒 الأستاذ</a> |
        <a href="/cashflow" style="color:#FFD700;">💵 التدفقات</a> |
        <a href="/ai_forecast" style="color:#FFD700;">🧠 تنبؤ</a> |
        <a href="/logout" style="color:#ff4a4a;">🚪 خروج</a>
    </div>'''
    return render_template_string(PAGE, content=content)

@app.route('/accounts')
def accounts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    rows = c.fetchall(); conn.close()
    content = "<h2>📚 الحسابات</h2><table border='1'><tr><th>ID</th><th>الاسم</th><th>النوع</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/customers')
def customers():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM customers")
    rows = c.fetchall(); conn.close()
    content = "<h2>👥 العملاء</h2><table border='1'><tr><th>ID</th><th>الاسم</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/invoices')
def invoices():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM invoices")
    rows = c.fetchall(); conn.close()
    content = "<h2>🧾 الفواتير</h2><table border='1'><tr><th>ID</th><th>العميل</th><th>المبلغ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/products')
def products():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall(); conn.close()
    content = "<h2>📦 المنتجات</h2><table border='1'><tr><th>ID</th><th>الاسم</th><th>السعر</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/bank')
def bank():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM bank_moves")
    rows = c.fetchall(); conn.close()
    content = "<h2>🏦 البنك</h2><table border='1'><tr><th>ID</th><th>الوصف</th><th>المبلغ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
