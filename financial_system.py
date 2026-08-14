import sqlite3, hashlib, shutil, csv, io, os
from flask import Flask, render_template_string, request, session, redirect, Response
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'noah2026'
DB = 'noah.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT);
    CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, name TEXT, type TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS suppliers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS purchase_orders (id INTEGER PRIMARY KEY, supplier_id INTEGER, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER);
    CREATE TABLE IF NOT EXISTS bank_moves (id INTEGER PRIMARY KEY, date TEXT, desc TEXT, amount REAL);
    CREATE TABLE IF NOT EXISTS zakat (id INTEGER PRIMARY KEY, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS debts (id INTEGER PRIMARY KEY, name TEXT, amount REAL, type TEXT);
    CREATE TABLE IF NOT EXISTS budgets (id INTEGER PRIMARY KEY, name TEXT, amount REAL);
    CREATE TABLE IF NOT EXISTS assets (id INTEGER PRIMARY KEY, name TEXT, value REAL);
    CREATE TABLE IF NOT EXISTS currencies (id INTEGER PRIMARY KEY, code TEXT, rate REAL);
    ''')
    hashed = hashlib.sha256('123456'.encode()).hexdigest()
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', ?)", (hashed,))
    conn.commit()
    conn.close()

init_db()

PAGE_STYLE = '''
<style>
    body { 
    font-family:Tahoma; 
    background: linear-gradient(180deg, #0a0a2e, #1a0a3e, #0a0a2e);
    color:#eee; 
    padding:20px; 
    direction:rtl; 
    min-height:100vh;
    animation: bg-shift 10s ease infinite;
}
@keyframes bg-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
a { 
    color:#4af; 
    text-decoration:none; 
    margin:5px;
    transition: all 0.3s;
}
a:hover {
    color:#FFD700;
    text-shadow: 0 0 10px rgba(255,215,0,0.8);
}
input, select, button { 
    padding:8px; 
    margin:5px; 
    background:#222; 
    color:#eee; 
    border:1px solid #555; 
    border-radius:5px;
    transition: all 0.3s;
}
input:focus, select:focus {
    border-color: #FFD700;
    box-shadow: 0 0 15px rgba(255,215,0,0.3);
}
button { 
    background: linear-gradient(45deg, #FFD700, #FF8C00);
    color:#000; 
    cursor:pointer;
    font-weight: bold;
    border: none;
}
button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(255,215,0,0.4);
}
table { 
    width:100%; 
    border-collapse:collapse; 
    margin-top:15px;
}
th, td { 
    border:1px solid #444; 
    padding:8px; 
    text-align:center;
    transition: all 0.3s;
}
tr:hover td {
    background: rgba(255,215,0,0.05);
}
th { 
    background: linear-gradient(145deg, #1a1a4e, #0d0d2e); 
    color:#FFD700;
    text-shadow: 0 0 5px rgba(255,215,0,0.5);
}
.container { 
    background: rgba(20,20,50,0.8);
    padding:20px; 
    border-radius:20px;
    border: 1px solid rgba(255,215,0,0.3);
    box-shadow: 0 0 30px rgba(255,215,0,0.1);
    backdrop-filter: blur(10px);
}
.nav { 
    background: linear-gradient(145deg, #1a1a4e, #0d0d2e);
    padding:15px; 
    border-radius:15px; 
    margin-bottom:15px;
    border: 1px solid rgba(0,200,255,0.3);
    box-shadow: 0 0 20px rgba(0,200,255,0.1);
}
    a { color:#4af; text-decoration:none; margin:5px; }
    input, select, button { padding:8px; margin:5px; background:#222; color:#eee; border:1px solid #555; border-radius:5px; }
    button { background:#4af; color:#000; cursor:pointer; }
    table { width:100%; border-collapse:collapse; margin-top:15px; }
    th, td { border:1px solid #444; padding:8px; text-align:center; }
    th { background:#333; color:#4af; }
    .container { background:#1a1a1a; padding:20px; border-radius:10px; }
    .nav { background:#1a1a3e; padding:10px; border-radius:5px; margin-bottom:15px; }
</style>
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
        user = c.fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect('/')
        return redirect('/login?error=1')
    return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>نوح - الدخول</title></head>
    <body style="font-family:Tahoma;background:#0a0a2e;color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;">
        <div style="background:#1a1a3e;padding:40px;border-radius:20px;border:1px solid #FFD700;">
            <h1 style="text-align:center;color:#FFD700;">🦅 نوح</h1>
            <form method="POST">
                <input type="text" name="username" placeholder="المستخدم" required style="display:block;width:100%;padding:10px;margin:10px 0;border-radius:10px;border:1px solid #555;background:#222;color:#fff;">
                <input type="password" name="password" placeholder="كلمة المرور" required style="display:block;width:100%;padding:10px;margin:10px 0;border-radius:10px;border:1px solid #555;background:#222;color:#fff;">
                <button style="width:100%;padding:12px;background:#FFD700;border:none;border-radius:10px;font-weight:bold;cursor:pointer;">دخول</button>
            </form>
        </div>
    </body></html>'''

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/')
def index():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM accounts"); accounts = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM suppliers"); suppliers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM invoices"); invoices = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products"); products = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    conn.close()
    content = f'''
    <h1 style="text-align:center;color:#FFD700;">🦅 نوح - لوحة التحكم</h1>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;">
        <div style="background:#1a1a3e;padding:25px;border-radius:15px;text-align:center;"><div style="font-size:2rem;">📚</div><div style="font-size:2rem;">{accounts}</div>الحسابات</div>
        <div style="background:#1a1a3e;padding:25px;border-radius:15px;text-align:center;"><div style="font-size:2rem;">👥</div><div style="font-size:2rem;">{customers}</div>العملاء</div>
        <div style="background:#1a1a3e;padding:25px;border-radius:15px;text-align:center;"><div style="font-size:2rem;">📦</div><div style="font-size:2rem;">{suppliers}</div>الموردون</div>
        <div style="background:#1a1a3e;padding:25px;border-radius:15px;text-align:center;"><div style="font-size:2rem;">🧾</div><div style="font-size:2rem;">{invoices}</div>الفواتير</div>
        <div style="background:#1a1a3e;padding:25px;border-radius:15px;text-align:center;"><div style="font-size:2rem;">📦</div><div style="font-size:2rem;">{products}</div>المنتجات</div>
    </div>
    <div style="background:#1a1a3e;padding:25px;border-radius:15px;text-align:center;margin-top:20px;"><h2 style="color:#FFD700;">💰 الإيرادات</h2><div style="font-size:2.5rem;">{revenue}</div></div>
    <div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:20px;">
        <a href="/accounts">📚 الحسابات</a>
        <a href="/customers">👥 العملاء</a>
        <a href="/suppliers">📦 الموردون</a>
        <a href="/invoices">🧾 الفواتير</a>
        <a href="/products">📦 المنتجات</a>
        <a href="/bank">🏦 البنك</a>
        <a href="/zakat">🕌 الزكاة</a>
        <a href="/debts">💳 الديون</a>
        <a href="/all_systems">📊 كل الأنظمة</a>
        <a href="/logout">🚪 خروج</a>
    </div>'''
    return PAGE_STYLE + content

@app.route('/all_systems')
def all_systems():
    if 'user' not in session: return redirect('/login')
    systems = [
        ("/accounts", "📚", "الحسابات"),
        ("/customers", "👥", "العملاء"),
        ("/suppliers", "📦", "الموردون"),
        ("/invoices", "🧾", "الفواتير"),
        ("/products", "📦", "المنتجات"),
        ("/bank", "🏦", "البنك"),
        ("/zakat", "🕌", "الزكاة"),
        ("/debts", "💳", "الديون"),
        ("/budgets", "📋", "الميزانيات"),
        ("/assets", "🏢", "الأصول"),
        ("/currencies", "💱", "العملات"),
    ]
    content = '<h2 style="text-align:center;color:#FFD700;">📊 كل الأنظمة العاملة</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;">'
    for path, icon, name in systems:
        content += f'<a href="{path}" style="background:#1a1a3e;padding:20px;border-radius:10px;text-align:center;"><div style="font-size:2rem;">{icon}</div>{name}</a>'
    content += '</div><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/accounts', methods=['GET','POST'])
def accounts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO accounts (name, type) VALUES (?,?)", (request.form['name'], request.form['type']))
        conn.commit()
    c.execute("SELECT * FROM accounts")
    rows = c.fetchall(); conn.close()
    content = '<h2>📚 الحسابات</h2><form method="POST"><input name="name" placeholder="اسم الحساب" required><select name="type"><option>أصول</option><option>خصوم</option><option>إيرادات</option><option>مصاريف</option></select><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>النوع</th><th>الرصيد</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/customers', methods=['GET','POST'])
def customers():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO customers (name, phone) VALUES (?,?)", (request.form['name'], request.form['phone']))
        conn.commit()
    c.execute("SELECT * FROM customers")
    rows = c.fetchall(); conn.close()
    content = '<h2>👥 العملاء</h2><form method="POST"><input name="name" placeholder="اسم العميل" required><input name="phone" placeholder="الهاتف"><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>الهاتف</th><th>الرصيد</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/suppliers', methods=['GET','POST'])
def suppliers():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO suppliers (name, phone) VALUES (?,?)", (request.form['name'], request.form['phone']))
        conn.commit()
    c.execute("SELECT * FROM suppliers")
    rows = c.fetchall(); conn.close()
    content = '<h2>📦 الموردون</h2><form method="POST"><input name="name" placeholder="اسم المورد" required><input name="phone" placeholder="الهاتف"><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>الهاتف</th><th>الرصيد</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/invoices', methods=['GET','POST'])
def invoices():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (?,?,?)", (request.form['customer_id'], request.form['amount'], request.form['date']))
        conn.commit()
    c.execute("SELECT * FROM invoices")
    rows = c.fetchall(); conn.close()
    content = '<h2>🧾 الفواتير</h2><form method="POST"><input name="customer_id" placeholder="عميل ID" required><input name="amount" placeholder="مبلغ" required><input name="date" type="date" required><button>إصدار</button></form><table><tr><th>ID</th><th>العميل</th><th>المبلغ</th><th>التاريخ</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/products', methods=['GET','POST'])
def products():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO products (name, price, stock) VALUES (?,?,?)", (request.form['name'], request.form['price'], request.form['stock']))
        conn.commit()
    c.execute("SELECT * FROM products")
    rows = c.fetchall(); conn.close()
    content = '<h2>📦 المنتجات</h2><form method="POST"><input name="name" placeholder="اسم المنتج" required><input name="price" placeholder="السعر" required><input name="stock" placeholder="المخزون" required><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>السعر</th><th>المخزون</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/bank', methods=['GET','POST'])
def bank():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES (?,?,?)", (request.form['date'], request.form['desc'], request.form['amount']))
        conn.commit()
    c.execute("SELECT * FROM bank_moves")
    rows = c.fetchall(); conn.close()
    content = '<h2>🏦 البنك</h2><form method="POST"><input name="date" type="date" required><input name="desc" placeholder="الوصف" required><input name="amount" placeholder="المبلغ" required><button>إضافة</button></form><table><tr><th>ID</th><th>التاريخ</th><th>الوصف</th><th>المبلغ</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/zakat', methods=['GET','POST'])
def zakat():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO zakat (amount, date) VALUES (?,?)", (request.form['amount'], request.form['date']))
        conn.commit()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0")
    total = c.fetchone()[0]
    c.execute("SELECT * FROM zakat")
    rows = c.fetchall(); conn.close()
    nisab = 85 * 60
    due = total * 0.025 if total >= nisab else 0
    content = f'<h2>🕌 الزكاة</h2><p>💰 النقود: {total}</p><p>📏 النصاب: {nisab}</p><p style="color:#FFD700;font-size:1.5rem;">🧮 المستحقة: {due:.2f}</p><form method="POST"><input name="amount" placeholder="مبلغ" required><input name="date" type="date" required><button>تسجيل</button></form><table><tr><th>ID</th><th>مبلغ</th><th>تاريخ</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/debts', methods=['GET','POST'])
def debts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO debts (name, amount, type) VALUES (?,?,?)", (request.form['name'], request.form['amount'], request.form['type']))
        conn.commit()
    c.execute("SELECT * FROM debts")
    rows = c.fetchall(); conn.close()
    content = '<h2>💳 الديون</h2><form method="POST"><input name="name" placeholder="اسم" required><input name="amount" placeholder="مبلغ" required><select name="type"><option>علينا</option><option>لنا</option></select><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>مبلغ</th><th>نوع</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/budgets', methods=['GET','POST'])
def budgets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO budgets (name, amount) VALUES (?,?)", (request.form['name'], request.form['amount']))
        conn.commit()
    c.execute("SELECT * FROM budgets")
    rows = c.fetchall(); conn.close()
    content = '<h2>📋 الميزانيات</h2><form method="POST"><input name="name" placeholder="اسم" required><input name="amount" placeholder="مبلغ" required><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>المبلغ</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/assets', methods=['GET','POST'])
def assets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO assets (name, value) VALUES (?,?)", (request.form['name'], request.form['value']))
        conn.commit()
    c.execute("SELECT * FROM assets")
    rows = c.fetchall(); conn.close()
    content = '<h2>🏢 الأصول</h2><form method="POST"><input name="name" placeholder="اسم الأصل" required><input name="value" placeholder="القيمة" required><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>القيمة</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/currencies', methods=['GET','POST'])
def currencies():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO currencies (code, rate) VALUES (?,?)", (request.form['code'], request.form['rate']))
        conn.commit()
    c.execute("SELECT * FROM currencies")
    rows = c.fetchall(); conn.close()
    content = '<h2>💱 العملات</h2><form method="POST"><input name="code" placeholder="رمز" required><input name="rate" placeholder="سعر" required><button>إضافة</button></form><table><tr><th>ID</th><th>رمز</th><th>سعر</th></tr>'
    for r in rows: content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>'
    content += '</table><a href="/">🏠 العودة</a>'
    return PAGE_STYLE + content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
