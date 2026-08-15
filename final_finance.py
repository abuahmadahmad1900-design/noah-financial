from flask import Flask, request, session, redirect, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'final_finance_2026'
DB = 'new_finance.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, name TEXT, type TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS suppliers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, balance REAL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER);
    CREATE TABLE IF NOT EXISTS bank_moves (id INTEGER PRIMARY KEY, date TEXT, desc TEXT, amount REAL);
    CREATE TABLE IF NOT EXISTS zakat (id INTEGER PRIMARY KEY, amount REAL, date TEXT);
    CREATE TABLE IF NOT EXISTS debts (id INTEGER PRIMARY KEY, name TEXT, amount REAL, type TEXT);
    CREATE TABLE IF NOT EXISTS budgets (id INTEGER PRIMARY KEY, name TEXT, amount REAL);
    CREATE TABLE IF NOT EXISTS assets (id INTEGER PRIMARY KEY, name TEXT, value REAL);
    CREATE TABLE IF NOT EXISTS currencies (id INTEGER PRIMARY KEY, code TEXT, rate REAL);
    ''')
    conn.commit()
    conn.close()

init_db()

PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>🦅 نوح المالي</title>
<style>
    body { font-family:Tahoma; background:#0a0a2e; color:#fff; padding:20px; }
    a { color:#FFD700; text-decoration:none; margin:5px; }
    input, select, button { padding:10px; margin:5px; background:#222; color:#fff; border:1px solid #FFD700; border-radius:8px; }
    button { background:#FFD700; color:#000; font-weight:bold; cursor:pointer; }
    table { width:100%; border-collapse:collapse; margin-top:15px; }
    th, td { border:1px solid #444; padding:10px; text-align:center; }
    th { background:#1a1a3e; color:#FFD700; }
</style></head>
<body>
    {{ content | safe }}
</body></html>
'''

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form.get('username', 'admin')
        return redirect('/dashboard')
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>🦅 دخول نوح المالي</title>
    <style>
        body { font-family:Tahoma; background:#0a0a2e; color:#fff; display:flex; justify-content:center; align-items:center; height:100vh; }
        .box { background:#1a1a3e; padding:40px; border-radius:25px; border:2px solid #FFD700; text-align:center; }
        h2 { color:#FFD700; }
        input { display:block; width:100%; padding:12px; margin:10px 0; background:#222; border:1px solid #FFD700; color:#fff; border-radius:10px; }
        button { width:100%; padding:12px; background:#FFD700; border:none; border-radius:10px; font-weight:bold; }
    </style></head>
    <body><div class="box"><h2>🦅 نوح المالي</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="المستخدم">
        <input type="password" name="password" placeholder="كلمة المرور">
        <button>🚀 دخول</button>
    </form></div></body></html>''')

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
    c.execute("SELECT COUNT(*) FROM bank_moves"); bank = c.fetchone()[0]
    conn.close()
    content = f'''
    <h1 style="text-align:center;color:#FFD700;font-size:2.5rem;">🦅 لوحة نوح المالية</h1>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;margin:30px 0;">
        <div style="background:#1a1a3e;padding:25px;border-radius:20px;border:2px solid #FFD700;text-align:center;"><h2 style="font-size:2rem;color:#FFD700;">{accounts}</h2>حسابات</div>
        <div style="background:#1a1a3e;padding:25px;border-radius:20px;border:2px solid #00c8ff;text-align:center;"><h2 style="font-size:2rem;color:#00c8ff;">{customers}</h2>عملاء</div>
        <div style="background:#1a1a3e;padding:25px;border-radius:20px;border:2px solid #4affb0;text-align:center;"><h2 style="font-size:2rem;color:#4affb0;">{invoices}</h2>فواتير</div>
        <div style="background:#1a1a3e;padding:25px;border-radius:20px;border:2px solid #FFD700;text-align:center;"><h2 style="font-size:2rem;color:#FFD700;">{products}</h2>منتجات</div>
        <div style="background:#1a1a3e;padding:25px;border-radius:20px;border:2px solid #00c8ff;text-align:center;"><h2 style="font-size:2rem;color:#00c8ff;">{bank}</h2>بنك</div>
        <div style="background:#1a1a3e;padding:25px;border-radius:20px;border:2px solid #4affb0;text-align:center;"><h2 style="font-size:2rem;color:#4affb0;">{revenue}</h2>إيرادات</div>
    </div>
    <div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center;">
        <a href="/accounts" style="background:#1a1a3e;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;">📚 الحسابات</a>
        <a href="/customers" style="background:#1a1a3e;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;">👥 العملاء</a>
        <a href="/suppliers" style="background:#1a1a3e;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;">📦 الموردون</a>
        <a href="/invoices" style="background:#1a1a3e;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;">🧾 الفواتير</a>
        <a href="/products" style="background:#1a1a3e;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;">📦 المنتجات</a>
        <a href="/bank" style="background:#1a1a3e;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;">🏦 البنك</a>
        <a href="/zakat" style="background:#1a1a3e;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;">🕌 الزكاة</a>
        <a href="/debts" style="background:#1a1a3e;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;">💳 الديون</a>
        <a href="/budgets" style="background:#1a1a3e;padding:15px 25px;border-radius:25px;border:2px solid #4affb0;">📋 الميزانيات</a>
        <a href="/assets" style="background:#1a1a3e;padding:15px 25px;border-radius:25px;border:2px solid #FFD700;">🏢 الأصول</a>
        <a href="/currencies" style="background:#1a1a3e;padding:15px 25px;border-radius:25px;border:2px solid #00c8ff;">💱 العملات</a>
        <a href="/logout" style="background:#1a1a3e;padding:15px 25px;border-radius:25px;border:2px solid #ff4a4a;">🚪 خروج</a>
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
    content = "<h2>📚 الحسابات</h2><form method='POST'><input name='name' placeholder='اسم الحساب' required><select name='type'><option>أصول</option><option>خصوم</option><option>إيرادات</option><option>مصاريف</option></select><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>النوع</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
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
    content = "<h2>👥 العملاء</h2><form method='POST'><input name='name' placeholder='اسم العميل' required><input name='phone' placeholder='الهاتف'><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>الهاتف</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
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
    content = "<h2>📦 الموردون</h2><form method='POST'><input name='name' placeholder='اسم المورد' required><input name='phone' placeholder='الهاتف'><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>الهاتف</th></tr>"
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
    content = "<h2>🧾 الفواتير</h2><form method='POST'><input name='customer_id' placeholder='رقم العميل' required><input name='amount' placeholder='المبلغ' required><input name='date' type='date' required><button>إصدار</button></form><table><tr><th>ID</th><th>العميل</th><th>المبلغ</th><th>التاريخ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
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
    content = "<h2>📦 المنتجات</h2><form method='POST'><input name='name' placeholder='اسم المنتج' required><input name='price' placeholder='السعر' required><input name='stock' placeholder='المخزون' required><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>السعر</th><th>المخزون</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/bank', methods=['GET','POST'])
def bank():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES (?,?,?)", (request.form['date'], request.form['desc'], request.form['amount']))
        conn.commit()
    c.execute("SELECT * FROM bank_moves")
    rows = c.fetchall()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves")
    balance = c.fetchone()[0]
    conn.close()
    content = f"<h2>🏦 البنك</h2><p style='font-size:1.5rem;color:#FFD700;'>الرصيد: {balance}</p><form method='POST'><input name='date' type='date' required><input name='desc' placeholder='الوصف' required><input name='amount' placeholder='المبلغ' required><button>إضافة</button></form><table><tr><th>ID</th><th>التاريخ</th><th>الوصف</th><th>المبلغ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

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
    content = f"<h2>🕌 الزكاة</h2><p>💰 النقود: {total}</p><p>📏 النصاب: {nisab}</p><p style='color:#FFD700;font-size:1.5rem;'>🧮 المستحقة: {due:.2f}</p><form method='POST'><input name='amount' placeholder='مبلغ' required><input name='date' type='date' required><button>تسجيل</button></form><table><tr><th>ID</th><th>مبلغ</th><th>تاريخ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/debts', methods=['GET','POST'])
def debts():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO debts (name, amount, type) VALUES (?,?,?)", (request.form['name'], request.form['amount'], request.form['type']))
        conn.commit()
    c.execute("SELECT * FROM debts")
    rows = c.fetchall(); conn.close()
    content = "<h2>💳 الديون</h2><form method='POST'><input name='name' placeholder='اسم' required><input name='amount' placeholder='مبلغ' required><select name='type'><option>علينا</option><option>لنا</option></select><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>مبلغ</th><th>نوع</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/budgets', methods=['GET','POST'])
def budgets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO budgets (name, amount) VALUES (?,?)", (request.form['name'], request.form['amount']))
        conn.commit()
    c.execute("SELECT * FROM budgets")
    rows = c.fetchall(); conn.close()
    content = "<h2>📋 الميزانيات</h2><form method='POST'><input name='name' placeholder='اسم' required><input name='amount' placeholder='مبلغ' required><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>المبلغ</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/assets', methods=['GET','POST'])
def assets():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO assets (name, value) VALUES (?,?)", (request.form['name'], request.form['value']))
        conn.commit()
    c.execute("SELECT * FROM assets")
    rows = c.fetchall(); conn.close()
    content = "<h2>🏢 الأصول</h2><form method='POST'><input name='name' placeholder='اسم الأصل' required><input name='value' placeholder='القيمة' required><button>إضافة</button></form><table><tr><th>ID</th><th>الاسم</th><th>القيمة</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

@app.route('/currencies', methods=['GET','POST'])
def currencies():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO currencies (code, rate) VALUES (?,?)", (request.form['code'], request.form['rate']))
        conn.commit()
    c.execute("SELECT * FROM currencies")
    rows = c.fetchall(); conn.close()
    content = "<h2>💱 العملات</h2><form method='POST'><input name='code' placeholder='رمز' required><input name='rate' placeholder='سعر' required><button>إضافة</button></form><table><tr><th>ID</th><th>رمز</th><th>سعر</th></tr>"
    for r in rows: content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

@app.route('/advanced_reports')
def advanced_reports():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0"); inflow = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0"); outflow = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(balance),0) FROM accounts WHERE type='أصول'"); assets = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(balance),0) FROM accounts WHERE type='خصوم'"); liabilities = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM debts WHERE type='علينا'"); our_debts = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM debts WHERE type='لنا'"); their_debts = c.fetchone()[0]
    conn.close()
    net_cash = inflow + outflow
    equity = assets - liabilities
    content = f'''
    <h2 style="text-align:center;color:#FFD700;">📊 التقارير المتقدمة</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;margin-top:20px;">
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:15px;text-align:center;border:2px solid #FFD700;"><h3>💰 الإيرادات</h3><p style="font-size:2rem;color:#FFD700;">{revenue}</p></div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:15px;text-align:center;border:2px solid #00c8ff;"><h3>💵 صافي التدفق</h3><p style="font-size:2rem;color:#00c8ff;">{net_cash}</p></div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:15px;text-align:center;border:2px solid #4affb0;"><h3>🏢 الأصول</h3><p style="font-size:2rem;color:#4affb0;">{assets}</p></div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:15px;text-align:center;border:2px solid #ff4a4a;"><h3>📉 الخصوم</h3><p style="font-size:2rem;color:#ff4a4a;">{liabilities}</p></div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:15px;text-align:center;border:2px solid #FFD700;"><h3>📊 حقوق الملكية</h3><p style="font-size:2rem;color:#FFD700;">{equity}</p></div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:15px;text-align:center;border:2px solid #00c8ff;"><h3>💳 ديون علينا</h3><p style="font-size:2rem;color:#00c8ff;">{our_debts}</p></div>
        <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:25px;border-radius:15px;text-align:center;border:2px solid #4affb0;"><h3>💳 ديون لنا</h3><p style="font-size:2rem;color:#4affb0;">{their_debts}</p></div>
    </div>'''
    return render_template_string(PAGE, content=content)

@app.route('/smart_analysis')
def smart_analysis():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices"); revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0"); expenses = abs(c.fetchone()[0])
    c.execute("SELECT COUNT(*) FROM customers"); customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products"); products = c.fetchone()[0]
    conn.close()
    profit = revenue - expenses
    margin = (profit / revenue * 100) if revenue > 0 else 0
    insights = []
    if margin > 30: insights.append("✅ ربحية ممتازة!")
    elif margin > 10: insights.append("📊 ربحية جيدة، يمكن تحسينها")
    else: insights.append("⚠️ ربحية منخفضة")
    if customers >= 5: insights.append("👥 قاعدة عملاء قوية")
    else: insights.append("📈 تحتاج المزيد من العملاء")
    if products >= 5: insights.append("📦 تنوع منتجات جيد")
    else: insights.append("📦 أضف منتجات جديدة")
    content = f'''
    <h2 style="text-align:center;color:#00c8ff;">🧠 التحليل الذكي</h2>
    <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:30px;border-radius:20px;margin-top:20px;text-align:center;border:2px solid #00c8ff;">
        <h3 style="color:#00c8ff;">هامش الربح</h3>
        <p style="font-size:3rem;color:#FFD700;">{margin:.1f}%</p>
    </div>
    <div style="margin-top:20px;">'''
    for i in insights:
        content += f'<div style="background:#1a1a4e;padding:15px;border-radius:10px;margin:10px 0;border-right:4px solid #FFD700;">{i}</div>'
    content += "</div>"
    return render_template_string(PAGE, content=content)
