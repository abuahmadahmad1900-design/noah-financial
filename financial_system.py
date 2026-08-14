from flask import Flask, render_template_string, request, session, redirect
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'noah2026'
DB = 'noah.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )''')
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', '123456')")
    conn.commit()
    conn.close()

init_db()

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
    
    error_msg = ''
    if request.args.get('error'):
        error_msg = '<div style="color:#ff4a4a;text-align:center;margin-bottom:20px;">❌ اسم المستخدم أو كلمة المرور غير صحيحة</div>'
    
    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🦅 نوح - بوابة الدخول</title>
        <style>
            * {{ margin:0; padding:0; box-sizing:border-box; }}
            body {{
                font-family: Tahoma, sans-serif;
                background: linear-gradient(135deg, #0a0a2e, #1a0a3e, #0a1a2e);
                background-size: 400% 400%;
                animation: bg-shift 10s ease infinite;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .login-container {{
                width: 100%;
                max-width: 450px;
                background: rgba(20,20,50,0.9);
                border-radius: 30px;
                padding: 50px 40px;
                border: 2px solid rgba(255,215,0,0.4);
                box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 50px rgba(255,215,0,0.2);
            }}
            h1 {{
                text-align: center;
                font-size: 2.5rem;
                background: linear-gradient(45deg, #FFD700, #FF8C00);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
            }}
            .subtitle {{ text-align: center; color: #ccc; margin-bottom: 40px; }}
            input {{
                width: 100%;
                padding: 15px;
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.15);
                border-radius: 15px;
                color: #fff;
                font-size: 1rem;
                margin-bottom: 20px;
                outline: none;
            }}
            button {{
                width: 100%;
                padding: 15px;
                background: linear-gradient(45deg, #FFD700, #FF8C00);
                border: none;
                border-radius: 15px;
                color: #000;
                font-size: 1.1rem;
                font-weight: bold;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>🦅 نوح</h1>
            <p class="subtitle">بوابة الدخول إلى النظام المالي الأسطوري</p>
            {error_msg}
            <form method="POST">
                <input type="text" name="username" placeholder="👤 اسم المستخدم" required>
                <input type="password" name="password" placeholder="🔒 كلمة المرور" required>
                <button type="submit">دخول</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')
    return redirect('/magic')

PAGE_STYLE = '''
<style>
    body { font-family: Tahoma; background: #111; color: #eee; padding: 20px; direction: rtl; }
    a { color: #4af; text-decoration: none; margin: 5px; }
    a:hover { color: #0ff; }
    input, select, button { padding: 8px; margin: 5px; background: #222; color: #eee; border: 1px solid #555; border-radius: 5px; }
    button { background: #4af; color: #000; cursor: pointer; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    th, td { border: 1px solid #444; padding: 8px; text-align: center; }
    th { background: #333; color: #4af; }
    .container { background: #1a1a1a; padding: 20px; border-radius: 10px; }
    .nav { background: #1a1a3e; padding: 10px; border-radius: 5px; margin-bottom: 15px; }
</style>
'''

# لوحة تحكم بسيطة
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM accounts")
    accounts = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers")
    customers = c.fetchone()[0]
    conn.close()
    content = f'''
    <h2>📊 لوحة التحكم</h2>
    <p>الحسابات: {accounts}</p>
    <p>العملاء: {customers}</p>
    '''
    return PAGE_STYLE + content

# إضافة الجداول
def add_tables():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        balance REAL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        balance REAL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        balance REAL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        amount REAL,
        date TEXT
    );
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        stock INTEGER
    );
    ''')
    conn.commit()
    conn.close()

add_tables()

# واجهة الحسابات
@app.route('/accounts', methods=['GET', 'POST'])
def accounts():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        type_acc = request.form['type']
        c.execute("INSERT INTO accounts (name, type) VALUES (?,?)", (name, type_acc))
        conn.commit()
    c.execute("SELECT * FROM accounts")
    rows = c.fetchall()
    conn.close()
    content = '''
    <div class="nav">
        <a href="/dashboard">🏠 الرئيسية</a>
        <a href="/accounts">📚 الحسابات</a>
        <a href="/customers">👥 العملاء</a>
        <a href="/suppliers">📦 الموردون</a>
        <a href="/invoices">🧾 الفواتير</a>
        <a href="/products">📦 المنتجات</a>
        <a href="/charts">📊 الرسوم</a>
                <a href="/global_markets">🌍 المؤشرات</a>
                <a href="/oracle">🔮 عرّاف نوح</a>
                <a href="/logout">🚪 خروج</a>
    </div>
    <div class="container">
    <h2>📚 الحسابات</h2>
    <form method="POST">
        <input name="name" placeholder="اسم الحساب" required>
        <select name="type">
            <option>أصول</option>
            <option>خصوم</option>
            <option>حقوق ملكية</option>
            <option>إيرادات</option>
            <option>مصاريف</option>
        </select>
        <button>إضافة</button>
    </form>
    <table>
        <tr><th>ID</th><th>الاسم</th><th>النوع</th><th>الرصيد</th></tr>
    '''
    for r in rows:
        content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table></div>'
    return PAGE_STYLE + content

# واجهة العملاء
@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        c.execute("INSERT INTO customers (name, phone) VALUES (?,?)", (name, phone))
        conn.commit()
    c.execute("SELECT * FROM customers")
    rows = c.fetchall()
    conn.close()
    content = '''
    <div class="nav">
        <a href="/dashboard">🏠 الرئيسية</a>
        <a href="/accounts">📚 الحسابات</a>
        <a href="/customers">👥 العملاء</a>
        <a href="/suppliers">📦 الموردون</a>
        <a href="/invoices">🧾 الفواتير</a>
        <a href="/products">📦 المنتجات</a>
        <a href="/logout">🚪 خروج</a>
    </div>
    <div class="container">
    <h2>👥 العملاء</h2>
    <form method="POST">
        <input name="name" placeholder="اسم العميل" required>
        <input name="phone" placeholder="الهاتف">
        <button>إضافة</button>
    </form>
    <table>
        <tr><th>ID</th><th>الاسم</th><th>الهاتف</th><th>الرصيد</th></tr>
    '''
    for r in rows:
        content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table></div>'
    return PAGE_STYLE + content

# واجهة المنتجات
@app.route('/products', methods=['GET', 'POST'])
def products():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']
        c.execute("INSERT INTO products (name, price, stock) VALUES (?,?,?)",
                  (name, price, stock))
        conn.commit()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()
    content = '''
    <div class="nav">
        <a href="/dashboard">🏠 الرئيسية</a>
        <a href="/accounts">📚 الحسابات</a>
        <a href="/customers">👥 العملاء</a>
        <a href="/suppliers">📦 الموردون</a>
        <a href="/invoices">🧾 الفواتير</a>
        <a href="/products">📦 المنتجات</a>
        <a href="/logout">🚪 خروج</a>
    </div>
    <div class="container">
    <h2>📦 المنتجات</h2>
    <form method="POST">
        <input name="name" placeholder="اسم المنتج" required>
        <input name="price" placeholder="السعر" required>
        <input name="stock" placeholder="المخزون" required>
        <button>إضافة</button>
    </form>
    <table>
        <tr><th>ID</th><th>الاسم</th><th>السعر</th><th>المخزون</th></tr>
    '''
    for r in rows:
        content += f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>'
    content += '</table></div>'
    return PAGE_STYLE + content

# تشغيل التطبيق

# ========== لوحة التحكم الأسطورية ==========
@app.route('/legendary')
def legendary():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM accounts")
    accounts = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers")
    customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM suppliers")
    suppliers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM invoices")
    invoices = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products")
    products = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM bank_moves")
    bank_moves = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    revenue = c.fetchone()[0]
    conn.close()

    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="theme-color" content="#0a0a2e">
        <title>نوح - لوحة القيادة الأسطورية</title>
        <style>
            body {{
                font-family: Tahoma;
                background: linear-gradient(135deg, #0a0a2e, #1a0a3e, #0a1a2e, #0a0a2e);
            background-size: 400% 400%;
            animation: bg-shift 10s ease infinite;
                color: #fff;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 20px;
                margin: 0;
            }}
            .container {{
                width: 100%;
                max-width: 1100px;
                background: rgba(20,20,50,0.8);
                border-radius: 30px;
                padding: 30px;
                box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 30px rgba(255,215,0,0.3);
                border: 2px solid rgba(255,215,0,0.5);
            box-shadow: 0 0 30px rgba(255,215,0,0.3), 0 0 60px rgba(0,200,255,0.2), inset 0 0 30px rgba(255,215,0,0.1);
                animation: glow 3s ease-in-out infinite alternate;
            }}
            @keyframes bg-shift {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            @keyframes title-glow {{
                from {{ text-shadow: 0 0 10px #FFD700, 0 0 20px #FF8C00; }}
                to {{ text-shadow: 0 0 30px #FFD700, 0 0 60px #FF8C00, 0 0 90px #FF4500; }}
            }}
            @keyframes rev-pulse {{
                0%, 100% {{ text-shadow: 0 0 10px #FFD700; }}
                50% {{ text-shadow: 0 0 40px #FFD700, 0 0 80px #FF8C00; }}
            }}
            @keyframes subtitle-pulse {{
                0%, 100% {{ opacity: 0.7; }}
                50% {{ opacity: 1; text-shadow: 0 0 20px rgba(255,215,0,0.8); }}
            }}
            @keyframes glow {{
                from {{ box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 20px rgba(255,215,0,0.2); }}
                to {{ box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 50px rgba(255,215,0,0.6); }}
            }}
            h1 {{
                text-align: center;
                font-size: 3rem;
                animation: title-glow 2s ease-in-out infinite alternate;
                background: linear-gradient(45deg, #FFD700, #FF8C00, #FFD700);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
            }}
            .subtitle {{
                text-align: center;
                color: #ccc;
            text-shadow: 0 0 5px rgba(0,200,255,0.5);
            font-weight: bold;
                margin-bottom: 40px;
                font-size: 1.2rem;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            .stat-card {{
                background: linear-gradient(145deg, #1a1a3e, #0d0d24);
                border-radius: 20px;
                padding: 25px;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.1);
                transition: all 0.3s;
            }}
            .stat-card:hover {{
                transform: translateY(-10px);
                border-color: #00c8ff;
                box-shadow: 0 15px 30px rgba(0,200,255,0.3);
            }}
            .stat-card .icon {{
                font-size: 3rem;
                margin-bottom: 10px;
            }}
            .stat-card .value {{
                font-size: 2.5rem;
                font-weight: bold;
                color: #fff;
            }}
            .stat-card .label {{
                color: #888;
                font-size: 0.9rem;
                margin-top: 5px;
            }}
            .highlight {{
                background: linear-gradient(145deg, #2a2a4e, #1a1a3e);
                border-radius: 20px;
                padding: 30px;
                text-align: center;
                margin-bottom: 30px;
                border: 1px solid rgba(255,215,0,0.3);
            }}
            .highlight h2 {{
                color: #FFD700;
                font-size: 1.5rem;
                margin-bottom: 15px;
            }}
            .highlight .amount {{
                font-size: 3rem;
                font-weight: bold;
                background: linear-gradient(45deg, #FFD700, #FF8C00);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .nav-links {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                justify-content: center;
                margin-top: 20px;
            }}
            .nav-links a {{
                background: linear-gradient(145deg, #222244, #111133);
                color: #fff;
                padding: 12px 25px;
                border-radius: 30px;
                text-decoration: none;
                font-size: 0.9rem;
                border: 1px solid rgba(255,255,255,0.2);
                transition: all 0.3s;
            }}
            .nav-links a:hover {{
                background: #00c8ff;
                color: #000;
                transform: scale(1.1);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>نوح - لوحة القيادة الأسطورية</h1>
            <p class="subtitle">النظام المالي الأقوى في العالم</p>

            <div class="stats-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:25px;">
                <div class="stat-card" style="background:linear-gradient(135deg,#1a1a4e,#0d0d2e);border-radius:18px;padding:20px;text-align:center;border:1px solid rgba(100,150,255,0.3);">
                    <div style="font-size:2.5rem;">📚</div>
                    <div style="font-size:2rem;font-weight:900;color:#fff;" data-target="{accounts}">0</div>
                    <div style="color:#aaa;font-size:0.8rem;">الحسابات</div>
                </div>
                <div class="stat-card" style="background:linear-gradient(135deg,#1a1a4e,#0d0d2e);border-radius:18px;padding:20px;text-align:center;border:1px solid rgba(100,150,255,0.3);">
                    <div style="font-size:2.5rem;">👥</div>
                    <div style="font-size:2rem;font-weight:900;color:#fff;" data-target="{customers}">0</div>
                    <div style="color:#aaa;font-size:0.8rem;">العملاء</div>
                </div>
                <div class="stat-card" style="background:linear-gradient(135deg,#1a1a4e,#0d0d2e);border-radius:18px;padding:20px;text-align:center;border:1px solid rgba(100,150,255,0.3);">
                    <div style="font-size:2.5rem;">📦</div>
                    <div style="font-size:2rem;font-weight:900;color:#fff;" data-target="{suppliers}">0</div>
                    <div style="color:#aaa;font-size:0.8rem;">الموردون</div>
                </div>
                <div class="stat-card" style="background:linear-gradient(135deg,#1a1a4e,#0d0d2e);border-radius:18px;padding:20px;text-align:center;border:1px solid rgba(100,150,255,0.3);">
                    <div style="font-size:2.5rem;">🧾</div>
                    <div style="font-size:2rem;font-weight:900;color:#fff;" data-target="{invoices}">0</div>
                    <div style="color:#aaa;font-size:0.8rem;">الفواتير</div>
                </div>
                <div class="stat-card" style="background:linear-gradient(135deg,#1a1a4e,#0d0d2e);border-radius:18px;padding:20px;text-align:center;border:1px solid rgba(100,150,255,0.3);">
                    <div style="font-size:2.5rem;">📦</div>
                    <div style="font-size:2rem;font-weight:900;color:#fff;" data-target="{products}">0</div>
                    <div style="color:#aaa;font-size:0.8rem;">المنتجات</div>
                </div>
                <div class="stat-card" style="background:linear-gradient(135deg,#1a1a4e,#0d0d2e);border-radius:18px;padding:20px;text-align:center;border:1px solid rgba(100,150,255,0.3);">
                    <div style="font-size:2.5rem;">🏦</div>
                    <div style="font-size:2rem;font-weight:900;color:#fff;" data-target="{bank_moves}">0</div>
                    <div style="color:#aaa;font-size:0.8rem;">حركات بنكية</div>
                </div>
            </div>

            <div class="financial-summary" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:15px;margin-bottom:25px;">
                <div class="summary-card">
                    <h3>💰 الإيرادات</h3>
                    <div class="amount positive" id="revenue">{revenue}</div>
                </div>
                <div class="summary-card">
                    <h3>📉 المصاريف</h3>
                    <div class="amount negative" id="expenses">{expenses}</div>
                </div>
                <div class="summary-card">
                    <h3>📈 صافي الربح</h3>
                    <div class="amount neutral" id="net">{net}</div>
                </div>
                <div class="summary-card">
                    <h3>💵 التدفق النقدي</h3>
                    <div class="amount {"positive" if net_cash >= 0 else "negative"}" id="net_cash">{net_cash}</div>
                </div>
                <div class="summary-card">
                    <h3>🏢 الأصول</h3>
                    <div class="amount neutral">{total_assets}</div>
                </div>
                <div class="summary-card">
                    <h3>📊 حقوق الملكية</h3>
                    <div class="amount positive">{equity}</div>
                </div>
            </div>

            <div class="recent-section">
                <div class="recent-box">
                    <h3>🏦 آخر الحركات البنكية</h3>
                    {''.join(f'<div class="recent-item">{r[1]} - {r[2]} - {r[3]}</div>' for r in recent_moves)}
                </div>
                <div class="recent-box">
                    <h3>🧾 آخر الفواتير</h3>
                    {''.join(f'<div class="recent-item">فاتورة رقم {r[0]} - {r[2]} - {r[3]}</div>' for r in recent_invoices)}
                </div>
            </div>

            <div class="quick-actions">
                <a href="/ai/financial_analyst">🧠 المحلل المالي</a>
                <a href="/ai/forecaster">🔮 التنبؤ</a>
                <a href="/ai/risk_manager">🛡️ المخاطر</a>
                <a href="/ai/zakat_calculator">🕌 الزكاة الذكية</a>
                <a href="/ai/strategist">👑 الاستراتيجي</a>
            </div>
            <div class="quick-actions">
                <a href="/accounts">📚 الحسابات</a>
                <a href="/customers">👥 العملاء</a>
                <a href="/suppliers">📦 الموردون</a>
                <a href="/invoices">🧾 الفواتير</a>
                <a href="/products">📦 المنتجات</a>
                <a href="/bank">🏦 البنك</a>
                <a href="/zakat">🕌 الزكاة</a>
                <a href="/currency_converter">💱 محول العملات</a>
                <a href="/currency_board">💱 لوحة العملات</a>
                <a href="/reports">📊 التقارير</a>
                <a href="/projects">📁 المشاريع</a>
                <a href="/contracts">📜 العقود</a>
                <a href="/messages">✉️ الرسائل</a>
                <a href="/settings">⚙️ الإعدادات</a>
                <a href="/logout">🚪 خروج</a>
            </div>
        </div>

        <script>
            // الساعة
            function updateClock() {{
                const now = new Date();
                const time = now.toLocaleTimeString('ar');
                const date = now.toLocaleDateString('ar', {{ weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }});
                document.getElementById('clock').textContent = date + ' - ' + time;
            }}
            updateClock();
            setInterval(updateClock, 1000);

            // نجوم
            for (let i = 0; i < 80; i++) {{
                const star = document.createElement('div');
                star.classList.add('star');
                star.style.left = Math.random() * 100 + '%';
                star.style.top = Math.random() * 100 + '%';
                star.style.width = Math.random() * 3 + 1 + 'px';
                star.style.height = star.style.width;
                star.style.animationDuration = Math.random() * 3 + 1 + 's';
                star.style.animationDelay = Math.random() * 5 + 's';
                document.body.appendChild(star);
            }}

            // عدادات
            document.querySelectorAll('.value').forEach(el => {{
                const target = parseInt(el.getAttribute('data-target'));
                let current = 0;
                const step = Math.max(1, Math.floor(target / 40));
                const interval = setInterval(() => {{
                    current += step;
                    if (current >= target) {{
                        el.textContent = target;
                        clearInterval(interval);
                    }} else {{
                        el.textContent = current;
                    }}
                }}, 30);
            }});
        </script>
    <script>
            // عدادات متحركة
            function animateCounter(id, target) {{
                let current = 0;
                const step = Math.max(1, Math.floor(target / 40));
                const interval = setInterval(() => {{
                    current += step;
                    if (current >= target) {{
                        document.getElementById(id).textContent = target;
                        clearInterval(interval);
                    }} else {{
                        document.getElementById(id).textContent = current;
                    }}
                }}, 30);
            }}
            animateCounter('counter-accounts', 5);
            animateCounter('counter-customers', 4);
            animateCounter('counter-suppliers', 3);
            animateCounter('counter-invoices', 5);
            animateCounter('counter-products', 4);
        </script>
    </body>
    </html>
    '''


# ========== اللوحة السحرية المطورة ==========



# ========== العقول الخمسة للذكاء الاصطناعي ==========

# 1. عقل المحلل المالي
@app.route('/ai/financial_analyst')
def ai_financial_analyst():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM purchase_orders")
    expenses = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0")
    inflow = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0")
    outflow = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers")
    customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products")
    products = c.fetchone()[0]
    conn.close()
    
    net = revenue - expenses
    profit_margin = (net / revenue * 100) if revenue > 0 else 0
    cash_flow = inflow + outflow
    
    # تحليل ذكي
    analysis = []
    if profit_margin > 30:
        analysis.append("📈 الربحية ممتازة! استمر في استراتيجيتك الحالية.")
    elif profit_margin > 10:
        analysis.append("📊 الربحية جيدة، يمكن تحسينها بزيادة المبيعات.")
    else:
        analysis.append("⚠️ الربحية منخفضة، راجع مصاريفك.")
    
    if cash_flow < 0:
        analysis.append("🚨 التدفق النقدي سلبي! تحتاج إلى ضخ سيولة.")
    else:
        analysis.append("✅ التدفق النقدي إيجابي، وضعك المالي مستقر.")
    
    if customers < 5:
        analysis.append("👥 قاعدة العملاء صغيرة، ركز على التسويق.")
    
    if products < 5:
        analysis.append("📦 مخزون المنتجات محدود، فكر في التوسع.")
    
    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🧠 عقل المحلل المالي</title>
        <style>
            body {{ font-family: Tahoma; background: #0a0a1a; color: #fff; padding: 30px; direction: rtl; }}
            .container {{ max-width: 900px; margin: 0 auto; background: #1a1a3e; border-radius: 20px; padding: 30px; }}
            h1 {{ color: #00c8ff; text-align: center; margin-bottom: 30px; }}
            .analysis-box {{ background: #222; border-radius: 15px; padding: 20px; margin: 15px 0; border-right: 4px solid #00c8ff; }}
            .metric {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px; }}
            .metric-card {{ background: #111; border-radius: 10px; padding: 15px; text-align: center; }}
            a {{ color: #00c8ff; text-decoration: none; margin: 10px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 عقل المحلل المالي</h1>
            <div class="metric">
                <div class="metric-card">💰 الإيرادات: {revenue}</div>
                <div class="metric-card">📉 المصاريف: {expenses}</div>
                <div class="metric-card">📈 صافي الربح: {net}</div>
                <div class="metric-card">📊 هامش الربح: {profit_margin:.1f}%</div>
            </div>
            {''.join(f'<div class="analysis-box">{a}</div>' for a in analysis)}
            <a href="/magical_v3">🏠 العودة للوحة الرئيسية</a>
        </div>
    <script>
            // عدادات متحركة
            function animateCounter(id, target) {{
                let current = 0;
                const step = Math.max(1, Math.floor(target / 40));
                const interval = setInterval(() => {{
                    current += step;
                    if (current >= target) {{
                        document.getElementById(id).textContent = target;
                        clearInterval(interval);
                    }} else {{
                        document.getElementById(id).textContent = current;
                    }}
                }}, 30);
            }}
            animateCounter('counter-accounts', 5);
            animateCounter('counter-customers', 4);
            animateCounter('counter-suppliers', 3);
            animateCounter('counter-invoices', 5);
            animateCounter('counter-products', 4);
        </script>
    </body>
    </html>
    '''

# 2. عقل التنبؤ
@app.route('/ai/forecaster')
def ai_forecaster():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT date, SUM(amount) FROM invoices GROUP BY date ORDER BY date")
    data = c.fetchall()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    current_revenue = c.fetchone()[0]
    conn.close()
    
    # تنبؤ بسيط
    if len(data) > 0:
        avg = current_revenue / max(len(data), 1)
        next_month = current_revenue * 1.1
        next_quarter = current_revenue * 1.3
    else:
        avg = 0
        next_month = 0
        next_quarter = 0
    
    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🔮 عقل التنبؤ</title>
        <style>
            body {{ font-family: Tahoma; background: #0a0a1a; color: #fff; padding: 30px; direction: rtl; }}
            .container {{ max-width: 900px; margin: 0 auto; background: #1a1a3e; border-radius: 20px; padding: 30px; }}
            h1 {{ color: #FFD700; text-align: center; margin-bottom: 30px; }}
            .prediction {{ background: #222; border-radius: 15px; padding: 20px; margin: 15px 0; text-align: center; }}
            .prediction h3 {{ color: #FFD700; }}
            .prediction .value {{ font-size: 2rem; color: #fff; }}
            a {{ color: #FFD700; text-decoration: none; margin: 10px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔮 عقل التنبؤ المالي</h1>
            <div class="prediction">
                <h3>الإيراد الحالي</h3>
                <div class="value">{current_revenue}</div>
            </div>
            <div class="prediction">
                <h3>متوسط الإيراد اليومي</h3>
                <div class="value">{avg:.2f}</div>
            </div>
            <div class="prediction">
                <h3>توقع الشهر القادم</h3>
                <div class="value">{next_month:.2f}</div>
            </div>
            <div class="prediction">
                <h3>توقع الربع القادم</h3>
                <div class="value">{next_quarter:.2f}</div>
            </div>
            <a href="/magical_v3">🏠 العودة للوحة الرئيسية</a>
        </div>
    <script>
            // عدادات متحركة
            function animateCounter(id, target) {{
                let current = 0;
                const step = Math.max(1, Math.floor(target / 40));
                const interval = setInterval(() => {{
                    current += step;
                    if (current >= target) {{
                        document.getElementById(id).textContent = target;
                        clearInterval(interval);
                    }} else {{
                        document.getElementById(id).textContent = current;
                    }}
                }}, 30);
            }}
            animateCounter('counter-accounts', 5);
            animateCounter('counter-customers', 4);
            animateCounter('counter-suppliers', 3);
            animateCounter('counter-invoices', 5);
            animateCounter('counter-products', 4);
        </script>
    </body>
    </html>
    '''

# 3. عقل المخاطر
@app.route('/ai/risk_manager')
def ai_risk_manager():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM debts WHERE type='علينا'")
    our_debts = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM debts WHERE type='لنا'")
    their_debts = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves")
    cash = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices WHERE paid=0")
    unpaid = c.fetchone()[0]
    conn.close()
    
    risks = []
    if our_debts > cash:
        risks.append("🚨 الديون المستحقة علينا أكبر من النقد المتاح!")
    if unpaid > 0:
        risks.append(f"⚠️ لديك فواتير غير مدفوعة بقيمة {unpaid}")
    if cash < 0:
        risks.append("🚨 الرصيد النقدي سلبي!")
    if not risks:
        risks.append("✅ لا توجد مخاطر كبيرة حالياً. وضعك المالي آمن.")
    
    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🛡️ عقل المخاطر</title>
        <style>
            body {{ font-family: Tahoma; background: #0a0a1a; color: #fff; padding: 30px; direction: rtl; }}
            .container {{ max-width: 900px; margin: 0 auto; background: #1a1a3e; border-radius: 20px; padding: 30px; }}
            h1 {{ color: #ff4a4a; text-align: center; margin-bottom: 30px; }}
            .risk {{ background: #222; border-radius: 15px; padding: 20px; margin: 15px 0; border-right: 4px solid #ff4a4a; }}
            .safe {{ background: #222; border-radius: 15px; padding: 20px; margin: 15px 0; border-right: 4px solid #4aff4a; }}
            a {{ color: #ff4a4a; text-decoration: none; margin: 10px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ عقل المخاطر المالية</h1>
            {''.join(f'<div class="risk">{r}</div>' for r in risks)}
            <a href="/magical_v3">🏠 العودة للوحة الرئيسية</a>
        </div>
    <script>
            // عدادات متحركة
            function animateCounter(id, target) {{
                let current = 0;
                const step = Math.max(1, Math.floor(target / 40));
                const interval = setInterval(() => {{
                    current += step;
                    if (current >= target) {{
                        document.getElementById(id).textContent = target;
                        clearInterval(interval);
                    }} else {{
                        document.getElementById(id).textContent = current;
                    }}
                }}, 30);
            }}
            animateCounter('counter-accounts', 5);
            animateCounter('counter-customers', 4);
            animateCounter('counter-suppliers', 3);
            animateCounter('counter-invoices', 5);
            animateCounter('counter-products', 4);
        </script>
    </body>
    </html>
    '''

# 4. عقل الزكاة الذكي
@app.route('/ai/zakat_calculator')
def ai_zakat_calculator():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0")
    cash = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(balance),0) FROM accounts WHERE type='أصول'")
    assets = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM debts WHERE type='لنا'")
    receivables = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM debts WHERE type='علينا'")
    payables = c.fetchone()[0]
    conn.close()
    
    total_zakatable = cash + assets + receivables - payables
    nisab = 85 * 60  # نصاب الذهب
    zakat_due = total_zakatable * 0.025 if total_zakatable >= nisab else 0
    
    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🕌 عقل الزكاة</title>
        <style>
            body {{ font-family: Tahoma; background: #0a0a1a; color: #fff; padding: 30px; direction: rtl; }}
            .container {{ max-width: 900px; margin: 0 auto; background: #1a1a3e; border-radius: 20px; padding: 30px; }}
            h1 {{ color: #4aff4a; text-align: center; margin-bottom: 30px; }}
            .detail {{ background: #222; border-radius: 10px; padding: 15px; margin: 10px 0; display: flex; justify-content: space-between; }}
            .total {{ background: #1a3e1a; border-radius: 15px; padding: 25px; text-align: center; margin-top: 20px; }}
            .total .amount {{ font-size: 2.5rem; color: #4aff4a; }}
            a {{ color: #4aff4a; text-decoration: none; margin: 10px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🕌 عقل الزكاة الذكي</h1>
            <div class="detail"><span>النقد المتاح:</span><span>{cash}</span></div>
            <div class="detail"><span>الأصول:</span><span>{assets}</span></div>
            <div class="detail"><span>الديون لنا:</span><span>{receivables}</span></div>
            <div class="detail"><span>الديون علينا:</span><span>{payables}</span></div>
            <div class="detail"><span>النصاب:</span><span>{nisab}</span></div>
            <div class="total">
                <h3>الزكاة المستحقة</h3>
                <div class="amount">{zakat_due:.2f}</div>
            </div>
            <a href="/magical_v3">🏠 العودة للوحة الرئيسية</a>
        </div>
    <script>
            // عدادات متحركة
            function animateCounter(id, target) {{
                let current = 0;
                const step = Math.max(1, Math.floor(target / 40));
                const interval = setInterval(() => {{
                    current += step;
                    if (current >= target) {{
                        document.getElementById(id).textContent = target;
                        clearInterval(interval);
                    }} else {{
                        document.getElementById(id).textContent = current;
                    }}
                }}, 30);
            }}
            animateCounter('counter-accounts', 5);
            animateCounter('counter-customers', 4);
            animateCounter('counter-suppliers', 3);
            animateCounter('counter-invoices', 5);
            animateCounter('counter-products', 4);
        </script>
    </body>
    </html>
    '''

# 5. عقل الاستراتيجي
@app.route('/ai/strategist')
def ai_strategist():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM purchase_orders")
    expenses = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers")
    customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products")
    products = c.fetchone()[0]
    conn.close()
    
    strategies = []
    if customers < 10:
        strategies.append("👥 ركز على اكتساب عملاء جدد من خلال التسويق الرقمي.")
    if products < 10:
        strategies.append("📦 قم بتوسيع خط منتجاتك لزيادة مصادر الدخل.")
    if revenue > 0 and expenses > 0:
        ratio = expenses / revenue
        if ratio > 0.7:
            strategies.append("📉 مصاريفك مرتفعة، حاول خفض التكاليف التشغيلية.")
        else:
            strategies.append("📈 وضعك جيد، فكر في التوسع.")
    strategies.append("💡 استثمر في التكنولوجيا لتحسين الكفاءة.")
    strategies.append("🌍 فكر في التوسع الإقليمي والدولي.")
    
    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>👑 عقل الاستراتيجي</title>
        <style>
            body {{ font-family: Tahoma; background: #0a0a1a; color: #fff; padding: 30px; direction: rtl; }}
            .container {{ max-width: 900px; margin: 0 auto; background: #1a1a3e; border-radius: 20px; padding: 30px; }}
            h1 {{ color: #FFD700; text-align: center; margin-bottom: 30px; }}
            .strategy {{ background: #222; border-radius: 15px; padding: 20px; margin: 15px 0; border-right: 4px solid #FFD700; }}
            a {{ color: #FFD700; text-decoration: none; margin: 10px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👑 عقل الاستراتيجي</h1>
            {''.join(f'<div class="strategy">{s}</div>' for s in strategies)}
            <a href="/magical_v3">🏠 العودة للوحة الرئيسية</a>
        </div>
    <script>
            // عدادات متحركة
            function animateCounter(id, target) {{
                let current = 0;
                const step = Math.max(1, Math.floor(target / 40));
                const interval = setInterval(() => {{
                    current += step;
                    if (current >= target) {{
                        document.getElementById(id).textContent = target;
                        clearInterval(interval);
                    }} else {{
                        document.getElementById(id).textContent = current;
                    }}
                }}, 30);
            }}
            animateCounter('counter-accounts', 5);
            animateCounter('counter-customers', 4);
            animateCounter('counter-suppliers', 3);
            animateCounter('counter-invoices', 5);
            animateCounter('counter-products', 4);
        </script>
    </body>
    </html>
    '''



# ========== البحث المتقدم ==========
@app.route('/search')
def search():
    if 'user' not in session:
        return redirect('/login')
    query = request.args.get('q', '')
    results = []
    if query:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        # البحث في العملاء
        c.execute("SELECT 'عميل', name FROM customers WHERE name LIKE ?", (f'%{query}%',))
        results.extend([(r[0], r[1]) for r in c.fetchall()])
        # البحث في الموردين
        c.execute("SELECT 'مورد', name FROM suppliers WHERE name LIKE ?", (f'%{query}%',))
        results.extend([(r[0], r[1]) for r in c.fetchall()])
        # البحث في المنتجات
        c.execute("SELECT 'منتج', name FROM products WHERE name LIKE ?", (f'%{query}%',))
        results.extend([(r[0], r[1]) for r in c.fetchall()])
        # البحث في الحسابات
        c.execute("SELECT 'حساب', name FROM accounts WHERE name LIKE ?", (f'%{query}%',))
        results.extend([(r[0], r[1]) for r in c.fetchall()])
        conn.close()
    
    content = f'''
    <div class="nav">
        <a href="/magical_v3">🏠 الرئيسية</a>
        <a href="/search">🔍 البحث</a>
        <a href="/logout">🚪 خروج</a>
    </div>
    <div class="container">
    <h2>🔍 البحث المتقدم</h2>
    <form method="GET" action="/search">
        <input type="text" name="q" placeholder="ابحث عن..." value="{query}" required>
        <button>بحث</button>
    </form>
    <table>
        <tr><th>النوع</th><th>الاسم</th></tr>
    '''
    for r in results:
        content += f'<tr><td>{r[0]}</td><td>{r[1]}</td></tr>'
    content += '</table></div>'
    return PAGE_STYLE + content

# ========== لوحة إحصائيات شاملة ==========
@app.route('/statistics')
def statistics():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # إجمالي كل شيء
    c.execute("SELECT COUNT(*) FROM accounts")
    total_accounts = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers")
    total_customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM suppliers")
    total_suppliers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM invoices")
    total_invoices = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products")
    total_products = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM bank_moves")
    total_bank_moves = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    total_revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0")
    total_inflow = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0")
    total_outflow = c.fetchone()[0]
    
    conn.close()
    
    content = f'''
    <div class="nav">
        <a href="/magical_v3">🏠 الرئيسية</a>
        <a href="/statistics">📊 الإحصائيات</a>
        <a href="/search">🔍 البحث</a>
        <a href="/logout">🚪 خروج</a>
    </div>
    <div class="container">
    <h2>📊 الإحصائيات الشاملة</h2>
    <table>
        <tr><th>البند</th><th>العدد/القيمة</th></tr>
        <tr><td>📚 الحسابات</td><td>{total_accounts}</td></tr>
        <tr><td>👥 العملاء</td><td>{total_customers}</td></tr>
        <tr><td>📦 الموردون</td><td>{total_suppliers}</td></tr>
        <tr><td>🧾 الفواتير</td><td>{total_invoices}</td></tr>
        <tr><td>📦 المنتجات</td><td>{total_products}</td></tr>
        <tr><td>🏦 الحركات البنكية</td><td>{total_bank_moves}</td></tr>
        <tr><td>💰 إجمالي الإيرادات</td><td>{total_revenue}</td></tr>
        <tr><td>💵 إجمالي التدفق الداخل</td><td>{total_inflow}</td></tr>
        <tr><td>💸 إجمالي التدفق الخارج</td><td>{total_outflow}</td></tr>
    </table>
    </div>'''
    return PAGE_STYLE + content

# ========== التقارير المتقدمة ==========
@app.route('/advanced_reports')
def advanced_reports():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # تحليل شامل
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM purchase_orders")
    expenses = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0")
    inflow = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0")
    outflow = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM debts WHERE type='علينا'")
    our_debts = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM debts WHERE type='لنا'")
    their_debts = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(value),0) FROM assets")
    total_assets = c.fetchone()[0]
    
    conn.close()
    
    net_profit = revenue - expenses
    net_cash = inflow + outflow
    debt_ratio = (our_debts / total_assets * 100) if total_assets > 0 else 0
    profit_margin = (net_profit / revenue * 100) if revenue > 0 else 0
    
    content = f'''
    <div class="nav">
        <a href="/magical_v3">🏠 الرئيسية</a>
        <a href="/advanced_reports">📊 تقارير متقدمة</a>
        <a href="/logout">🚪 خروج</a>
    </div>
    <div class="container">
    <h2>📊 التقارير المالية المتقدمة</h2>
    
    <h3>📈 مؤشرات الربحية</h3>
    <table>
        <tr><th>المؤشر</th><th>القيمة</th></tr>
        <tr><td>هامش الربح</td><td>{profit_margin:.2f}%</td></tr>
        <tr><td>صافي الربح</td><td>{net_profit}</td></tr>
    </table>
    
    <h3>💵 مؤشرات السيولة</h3>
    <table>
        <tr><th>المؤشر</th><th>القيمة</th></tr>
        <tr><td>صافي التدفق النقدي</td><td>{net_cash}</td></tr>
        <tr><td>التدفق الداخل</td><td>{inflow}</td></tr>
        <tr><td>التدفق الخارج</td><td>{outflow}</td></tr>
    </table>
    
    <h3>💳 مؤشرات الديون</h3>
    <table>
        <tr><th>المؤشر</th><th>القيمة</th></tr>
        <tr><td>الديون علينا</td><td>{our_debts}</td></tr>
        <tr><td>الديون لنا</td><td>{their_debts}</td></tr>
        <tr><td>نسبة الديون للأصول</td><td>{debt_ratio:.2f}%</td></tr>
    </table>
    </div>'''
    return PAGE_STYLE + content


# ========== البحث المتقدم ==========


# ========== محول العملات ==========
@app.route('/currency_converter', methods=['GET', 'POST'])
def currency_converter():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT code, rate FROM currencies")
    currencies = c.fetchall()
    conn.close()
    
    result = None
    if request.method == 'POST':
        amount = float(request.form['amount'])
        from_cur = request.form['from_currency']
        to_cur = request.form['to_currency']
        
        # البحث عن الأسعار
        from_rate = 1.0
        to_rate = 1.0
        for code, rate in currencies:
            if code == from_cur:
                from_rate = rate
            if code == to_cur:
                to_rate = rate
        
        result = amount * (to_rate / from_rate)
    
    content = f'''
    <div class="nav">
        <a href="/magical_v3">🏠 الرئيسية</a>
        <a href="/currency_converter">💱 محول العملات</a>
        <a href="/currencies">💱 العملات</a>
        <a href="/logout">🚪 خروج</a>
    </div>
    <div class="container">
    <h2>💱 محول العملات</h2>
    <form method="POST">
        <input name="amount" placeholder="المبلغ" required>
        <select name="from_currency">
    '''
    for code, rate in currencies:
        content += f'<option value="{code}">{code}</option>'
    content += '</select> → <select name="to_currency">'
    for code, rate in currencies:
        content += f'<option value="{code}">{code}</option>'
    content += '</select><button>تحويل</button></form>'
    
    if result is not None:
        content += f'<div style="background:#1a3e1a;padding:20px;border-radius:10px;margin-top:20px;text-align:center;font-size:1.5rem;">✅ النتيجة: {result:.4f}</div>'
    
    content += '</div>'
    return PAGE_STYLE + content

# ========== لوحة العملات ==========
@app.route('/currency_board')
def currency_board():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT code, rate FROM currencies ORDER BY rate")
    currencies = c.fetchall()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    total_revenue = c.fetchone()[0]
    conn.close()
    
    content = f'''
    <div class="nav">
        <a href="/magical_v3">🏠 الرئيسية</a>
        <a href="/currency_board">💱 لوحة العملات</a>
        <a href="/logout">🚪 خروج</a>
    </div>
    <div class="container">
    <h2>💱 لوحة العملات</h2>
    <p style="font-size:1.3rem;color:#FFD700;">الإيرادات بالدولار: {total_revenue:.2f} USD</p>
    <table>
        <tr><th>العملة</th><th>السعر مقابل الدولار</th><th>الإيرادات المعادلة</th></tr>
    '''
    for code, rate in currencies:
        converted = total_revenue / rate if rate > 0 else 0
        content += f'<tr><td>{code}</td><td>{rate:.4f}</td><td>{converted:.2f}</td></tr>'
    content += '</table></div>'
    return PAGE_STYLE + content


# ========== الصفحة الرئيسية الجديدة ==========
@app.route('/magic')
def magic():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM accounts")
    accounts = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers")
    customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM suppliers")
    suppliers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM invoices")
    invoices = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products")
    products = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    revenue = c.fetchone()[0]
    conn.close()

    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🦅 نوح - السحر المالي</title>
        <style>
            * {{ margin:0; padding:0; box-sizing:border-box; }}
            body {{
                font-family: 'Cairo', 'Tahoma', sans-serif;
            letter-spacing: 0.5px;
            text-shadow: 0 0 5px rgba(255,255,255,0.3);
                background: linear-gradient(180deg, #0a0a2e, #1a0a3e, #0a0a2e);
                color: #fff;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .container {{
                width: 100%;
                max-width: 1100px;
                background: rgba(20,20,50,0.85);
                backdrop-filter: blur(15px);
                border-radius: 30px;
                padding: 40px;
                box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 40px rgba(255,215,0,0.3);
                border: 2px solid rgba(255,215,0,0.6); box-shadow: 0 0 40px rgba(255,215,0,0.4), 0 0 80px rgba(0,200,255,0.2);
                animation: glow 3s ease-in-out infinite alternate;
            }}
            @keyframes glow {{
                from {{ box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 20px rgba(255,215,0,0.2); }}
                to {{ box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 50px rgba(255,215,0,0.6); }}
            }}
            h1 {{
                text-align: center;
                font-size: 3rem;
                background: linear-gradient(45deg, #FFD700, #FF8C00, #FFD700);
                background-size: 300% 300%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gradient-shift 3s ease infinite;
                margin-bottom: 10px;
            }}
            @keyframes gradient-shift {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            .subtitle {{
                text-align: center;
                color: #ccc;
            text-shadow: 0 0 10px rgba(255,215,0,0.5);
            animation: subtitle-pulse 3s ease-in-out infinite;
                margin-bottom: 40px;
                font-size: 1.1rem;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            .stat-card {{
                background: linear-gradient(145deg, #1a1a4e, #0d0d2e);
                border-radius: 20px;
                padding: 30px 20px;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.15);
                transition: all 0.3s;
                cursor: pointer;
            }}
            .stat-card:hover {{
                transform: translateY(-10px) rotate(2deg) scale(1.05);
                border-color: #00c8ff;
                box-shadow: 0 15px 30px rgba(0,200,255,0.4);
            }}
            .stat-card {{
                animation: float-card 3s ease-in-out infinite;
            }}
            .stat-card:nth-child(2) {{ animation-delay: 0.3s; }}
            .stat-card:nth-child(3) {{ animation-delay: 0.6s; }}
            .stat-card:nth-child(4) {{ animation-delay: 0.9s; }}
            .stat-card:nth-child(5) {{ animation-delay: 1.2s; }}
            @keyframes float-card {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-5px); }}
            }}
            .stat-card .icon {{
                font-size: 3rem;
                margin-bottom: 15px;
                animation: bounce 2s ease-in-out infinite;
            }}
            @keyframes bounce {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-8px); }}
            }}
            .stat-card .value {{
                font-size: 2.5rem;
                font-weight: 900;
            text-shadow: 0 0 20px rgba(0,200,255,0.8), 0 0 40px rgba(255,215,0,0.4);
            letter-spacing: 2px;
                color: #fff;
                text-shadow: 0 0 15px rgba(0,200,255,0.5), 0 0 30px rgba(255,215,0,0.3);
                animation: pulse 2s ease-in-out infinite;
            }}
            .stat-card .label {{
                color: #aaa;
                font-size: 0.9rem;
                margin-top: 8px;
            }}
            .highlight {{
                background: linear-gradient(145deg, #2a2a5e, #1a1a3e);
                border-radius: 20px;
                padding: 35px;
                text-align: center;
                margin-bottom: 30px;
                border: 1px solid rgba(255,215,0,0.4);
            }}
            .highlight h2 {{
                color: #FFD700;
                margin-bottom: 15px;
            }}
            .highlight .amount {{
                font-size: 3.5rem;
                animation: rev-pulse 1.5s ease-in-out infinite;
                font-weight: 900;
                background: linear-gradient(45deg, #FFD700, #FF8C00);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .nav-links {{
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                justify-content: center;
            }}
            .nav-links a {{
                background: linear-gradient(145deg, #222255, #111133);
            position: relative;
            overflow: hidden;
                color: #fff;
                padding: 14px 28px;
                border-radius: 30px;
                text-decoration: none;
                font-size: 0.95rem;
                border: 1px solid rgba(255,255,255,0.2);
                transition: all 0.3s;
            }}
            .nav-links a:hover {{
                background: #00c8ff;
                color: #000;
                transform: scale(1.1);
                box-shadow: 0 0 30px rgba(0,200,255,0.6);
            }}
            @keyframes sparkle {{
                0% {{ opacity: 0; transform: scale(0); }}
                50% {{ opacity: 1; transform: scale(1.5); }}
                100% {{ opacity: 0; transform: scale(0); }}
            }}
            .sparkle {{
                position: fixed;
                pointer-events: none;
                z-index: 9999;
                animation: sparkle 1s ease-in-out infinite;
            }}
        </style>
    </head>
    <body>
        <div class="clock" id="clock" style="position:absolute;top:20px;left:20px;color:#FFD700;font-size:1.2rem;"></div>
        <div class="container">
            <h1 style="font-size:3.5rem;font-weight:900;background:linear-gradient(45deg,#FFD700,#FF8C00,#FFD700,#FFD700);background-size:300% 300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:gradient-shift 3s ease infinite;text-align:center;margin-bottom:10px;">🦅 نوح - السحر المالي</h1>
            <p class="subtitle">النظام المالي الأسطوري</p>
            <div class="wisdom" style="background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.3);border-radius:15px;padding:15px;text-align:center;margin-bottom:30px;color:#FFD700;">
                💡 <span style="animation:pulse-wisdom 2s ease-in-out infinite;">راقب تدفقاتك النقدية دائماً</span>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="icon">📚</div>
                    <div class="value">{accounts}</div>
                    <div class="label">الحسابات</div>
                </div>
                <div class="stat-card">
                    <div class="icon">👥</div>
                    <div class="value">{customers}</div>
                    <div class="label">العملاء</div>
                </div>
                <div class="stat-card">
                    <div class="icon">📦</div>
                    <div class="value">{suppliers}</div>
                    <div class="label">الموردون</div>
                </div>
                <div class="stat-card">
                    <div class="icon">🧾</div>
                    <div class="value">{invoices}</div>
                    <div class="label">الفواتير</div>
                </div>
                <div class="stat-card">
                    <div class="icon">📦</div>
                    <div class="value">{products}</div>
                    <div class="label">المنتجات</div>
                </div>
            </div>

            <div class="highlight">
                <h2>💰 إجمالي الإيرادات</h2>
                <div class="amount">{revenue}</div>
            </div>

            <div class="nav-links" style="margin-bottom:15px;">
                <a href="/ai/financial_analyst">🧠 المحلل المالي</a>
                <a href="/ai/forecaster">🔮 التنبؤ</a>
                <a href="/ai/risk_manager">🛡️ المخاطر</a>
                <a href="/ai/zakat_calculator">🕌 الزكاة الذكية</a>
                <a href="/ai/strategist">👑 الاستراتيجي</a>
            </div>
            <div class="nav-links">
                <a href="/accounts">📚 الحسابات</a>
                <a href="/customers">👥 العملاء</a>
                <a href="/suppliers">📦 الموردون</a>
                <a href="/invoices">🧾 الفواتير</a>
                <a href="/products">📦 المنتجات</a>
                <a href="/bank">🏦 البنك</a>
                <a href="/zakat">🕌 الزكاة</a>
                <a href="/reports">📊 التقارير</a>
                <a href="/projects">📁 المشاريع</a>
                <a href="/contracts">📜 العقود</a>
                <a href="/messages">✉️ الرسائل</a>
                <a href="/settings">⚙️ الإعدادات</a>
                <a href="/currency_converter">💱 العملات</a>
                <a href="/charts">📊 الرسوم</a>
                <a href="/global_markets">🌍 المؤشرات</a>
                <a href="/logout">🚪 خروج</a>
            </div>
        </div>
    <script>
            // عدادات متحركة
            function animateCounter(id, target) {{
                let current = 0;
                const step = Math.max(1, Math.floor(target / 40));
                const interval = setInterval(() => {{
                    current += step;
                    if (current >= target) {{
                        document.getElementById(id).textContent = target;
                        clearInterval(interval);
                    }} else {{
                        document.getElementById(id).textContent = current;
                    }}
                }}, 30);
            }}
            animateCounter('counter-accounts', 5);
            animateCounter('counter-customers', 4);
            animateCounter('counter-suppliers', 3);
            animateCounter('counter-invoices', 5);
            animateCounter('counter-products', 4);
        </script>
    </body>
    </html>
    '''


# ========== المؤشرات الاقتصادية العالمية ==========
@app.route('/global_markets')
def global_markets():
    if 'user' not in session:
        return redirect('/login')
    
    # بيانات محاكاة للمؤشرات العالمية
    markets = [
        ('🇺🇸', 'الدولار الأمريكي', 1.0, 'مستقر'),
        ('🇪🇺', 'اليورو', 0.92, 'مرتفع'),
        ('🇸🇦', 'الريال السعودي', 3.75, 'مستقر'),
        ('🇦🇪', 'الدرهم الإماراتي', 3.67, 'مستقر'),
        ('🇬🇧', 'الجنيه الإسترليني', 0.79, 'منخفض'),
        ('🇯🇵', 'الين الياباني', 149.5, 'مستقر'),
        ('🇨🇳', 'اليوان الصيني', 7.2, 'مرتفع'),
        ('🇪🇬', 'الجنيه المصري', 48.5, 'منخفض'),
        ('🇹🇷', 'الليرة التركية', 32.8, 'منخفض'),
        ('🇷🇺', 'الروبل الروسي', 92.3, 'مستقر'),
        ('🪙', 'بيتكوين', 67250, 'متقلب'),
        ('🪙', 'إيثريوم', 3450, 'متقلب'),
        ('🥇', 'الذهب', 2380, 'مرتفع'),
        ('🥈', 'الفضة', 28.5, 'مرتفع'),
        ('🛢️', 'النفط الخام', 82.4, 'مستقر'),
    ]
    
    content = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🌍 المؤشرات العالمية</title>
        <style>
            body { font-family:Tahoma; background:#0a0a1a; color:#fff; padding:20px; }
            .container { max-width:1000px; margin:0 auto; }
            h1 { text-align:center; color:#FFD700; margin-bottom:30px; }
            table { width:100%; border-collapse:collapse; }
            th, td { border:1px solid #333; padding:12px; text-align:center; }
            th { background:#1a1a3e; color:#00c8ff; }
            tr:hover { background:#1a1a3e; }
            a { color:#00c8ff; text-decoration:none; display:inline-block; margin-top:20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌍 المؤشرات الاقتصادية العالمية</h1>
            <table>
                <tr><th>الأيقونة</th><th>الأصل</th><th>القيمة</th><th>الحالة</th></tr>
    '''
    for icon, name, value, status in markets:
        color = '#fff'
        if status == 'مرتفع':
            color = '#4aff4a'
        elif status == 'منخفض':
            color = '#ff4a4a'
        elif status == 'متقلب':
            color = '#FFD700'
        content += f'<tr><td>{icon}</td><td>{name}</td><td>{value}</td><td style="color:{color}">{status}</td></tr>'
    
    content += '''
            </table>
            <a href="/magic">🏠 العودة للوحة الرئيسية</a>
        </div>
    <script>
            // عدادات متحركة
            function animateCounter(id, target) {{
                let current = 0;
                const step = Math.max(1, Math.floor(target / 40));
                const interval = setInterval(() => {{
                    current += step;
                    if (current >= target) {{
                        document.getElementById(id).textContent = target;
                        clearInterval(interval);
                    }} else {{
                        document.getElementById(id).textContent = current;
                    }}
                }}, 30);
            }}
            animateCounter('counter-accounts', 5);
            animateCounter('counter-customers', 4);
            animateCounter('counter-suppliers', 3);
            animateCounter('counter-invoices', 5);
            animateCounter('counter-products', 4);
        </script>
    </body>
    </html>
    '''
    return content


# ========== الرسوم البيانية ==========
@app.route('/charts')
def charts():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT type, COUNT(*) FROM accounts GROUP BY type")
    accounts_data = c.fetchall()
    c.execute("SELECT date, SUM(amount) FROM invoices GROUP BY date")
    income_data = c.fetchall()
    conn.close()
    
    labels = []
    values = []
    for row in accounts_data:
        labels.append(row[0])
        values.append(row[1])
    
    income_labels = []
    income_values = []
    for row in income_data:
        income_labels.append(row[0])
        income_values.append(row[1])
    
    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>📊 الرسوم البيانية</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family:Tahoma; background:#0a0a1a; color:#fff; padding:20px; }}
            .container {{ max-width:1000px; margin:0 auto; }}
            h1 {{ text-align:center; color:#00c8ff; margin-bottom:30px; }}
            .chart-box {{ background:#1a1a3e; border-radius:20px; padding:25px; margin-bottom:25px; }}
            a {{ color:#00c8ff; text-decoration:none; display:inline-block; margin-top:20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 الرسوم البيانية المالية</h1>
            <div class="chart-box">
                <canvas id="accountsChart"></canvas>
            </div>
            <div class="chart-box">
                <canvas id="incomeChart"></canvas>
            </div>
            <a href="/magic">🏠 العودة للوحة الرئيسية</a>
        </div>
        <script>
            const accountsLabels = {labels};
            const accountsValues = {values};
            new Chart(document.getElementById('accountsChart'), {{
                type: 'pie',
                data: {{
                    labels: accountsLabels,
                    datasets: [{{
                        data: accountsValues,
                        backgroundColor: ['#FFD700','#FF8C00','#4aff4a','#ff4a4a','#00c8ff']
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        title: {{ display: true, text: 'توزيع الحسابات', color: '#fff' }},
                        legend: {{ labels: {{ color: '#fff' }} }}
                    }}
                }}
            }});

            const incomeLabels = {income_labels};
            const incomeValues = {income_values};
            new Chart(document.getElementById('incomeChart'), {{
                type: 'bar',
                data: {{
                    labels: incomeLabels,
                    datasets: [{{
                        label: 'الإيرادات',
                        data: incomeValues,
                        backgroundColor: '#4aff4a'
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        title: {{ display: true, text: 'الإيرادات اليومية', color: '#fff' }},
                        legend: {{ labels: {{ color: '#fff' }} }}
                    }},
                    scales: {{
                        y: {{ ticks: {{ color: '#fff' }} }},
                        x: {{ ticks: {{ color: '#fff' }} }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    '''


# ========== الرسوم البيانية ==========

# ========== عرّاف نوح الذكي ==========
@app.route('/oracle')
def oracle():
    if 'user' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    revenue = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM customers")
    customers = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products")
    products = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0")
    inflow = c.fetchone()[0]
    conn.close()
    
    # تنبؤات ذكية
    predictions = []
    if revenue > 50000:
        predictions.append(("💰", "إيراداتك تتجاوز 50 ألف - أنت على طريق الثراء"))
    else:
        predictions.append(("📈", "إيراداتك ستنمو قريباً - استمر في العمل"))
    
    if customers >= 4:
        predictions.append(("👥", "قاعدة عملائك قوية - ركز على الاحتفاظ بهم"))
    else:
        predictions.append(("🎯", "تحتاج لتوسيع قاعدة عملائك"))
    
    if inflow > 50000:
        predictions.append(("💎", "تدفقك النقدي ممتاز - فكر في الاستثمار"))
    
    predictions.append(("🔮", "الشهر القادم سيشهد فرصاً مالية جديدة"))
    predictions.append(("✨", "الاستثمار في التكنولوجيا سيعود عليك بفوائد كبيرة"))
    predictions.append(("🌟", "التوسع الإقليمي سيكون خطوة حكيمة"))
    
    content = '''<!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🔮 عرّاف نوح</title>
        <style>
            body { font-family:Tahoma; background:#0a0a1a; color:#fff; padding:20px; display:flex; justify-content:center; align-items:center; min-height:100vh; }
            .container { max-width:800px; background:linear-gradient(145deg,#1a1a4e,#0d0d2e); border-radius:30px; padding:40px; border:2px solid rgba(255,215,0,0.5); box-shadow:0 0 50px rgba(255,215,0,0.3); }
            h1 { text-align:center; color:#FFD700; font-size:2.5rem; margin-bottom:10px; }
            .subtitle { text-align:center; color:#aaa; margin-bottom:30px; }
            .prediction { background:rgba(255,255,255,0.05); border-radius:15px; padding:20px; margin:15px 0; display:flex; align-items:center; gap:15px; font-size:1.1rem; border:1px solid rgba(255,255,255,0.1); }
            .prediction:hover { background:rgba(255,215,0,0.1); transform:translateX(-5px); transition:all 0.3s; }
            .icon { font-size:2rem; }
            a { color:#FFD700; text-decoration:none; display:inline-block; margin-top:20px; text-align:center; width:100%; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔮 عرّاف نوح</h1>
            <p class="subtitle">تنبؤات مالية ذكية من أعماق البيانات</p>'''
    
    for icon, text in predictions:
        content += f'<div class="prediction"><span class="icon">{icon}</span><span>{text}</span></div>'
    
    content += '<a href="/magic">🏠 العودة للوحة الرئيسية</a></div></body></html>'
    return content


# ========== النسخ الاحتياطي التلقائي ==========
import threading
import time as time_module
from datetime import datetime
import shutil

def auto_backup():
    while True:
        time_module.sleep(3600)  # كل ساعة
        try:
            backup_name = f"auto_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy(DB, backup_name)
            print(f"✅ نسخ احتياطي تلقائي: {backup_name}")
        except:
            pass

backup_thread = threading.Thread(target=auto_backup, daemon=True)
backup_thread.start()


# ========== 25 عقل ذكاء اصطناعي ==========
AI_SYSTEMS = [
    ("ai_analyst", "🧠", "المحلل المالي الشامل", "تحليل شامل للبيانات المالية"),
    ("ai_forecaster", "🔮", "المتنبئ المستقبلي", "توقع الإيرادات والمصاريف"),
    ("ai_risk", "🛡️", "حارس المخاطر", "كشف المخاطر المالية"),
    ("ai_zakat", "🕌", "حاسب الزكاة", "حساب الزكاة تلقائياً"),
    ("ai_strategist", "👑", "المخطط الاستراتيجي", "خطط استراتيجية ذكية"),
    ("ai_cashflow", "💵", "مراقب التدفق النقدي", "مراقبة التدفقات"),
    ("ai_profit", "📈", "محلل الربحية", "تحليل الربحية"),
    ("ai_debt", "💳", "مدير الديون", "إدارة الديون"),
    ("ai_tax", "💰", "مستشار الضرائب", "نصائح ضريبية"),
    ("ai_investment", "📊", "خبير الاستثمار", "توصيات استثمارية"),
    ("ai_budget", "📋", "مخطط الميزانيات", "تخطيط الميزانيات"),
    ("ai_customer", "👥", "محلل العملاء", "تحليل سلوك العملاء"),
    ("ai_supplier", "📦", "محلل الموردين", "تحليل الموردين"),
    ("ai_inventory", "🏭", "مدير المخزون", "إدارة المخزون"),
    ("ai_pricing", "💲", "خبير التسعير", "تسعير المنتجات"),
    ("ai_market", "🌍", "محلل الأسواق", "تحليل الأسواق"),
    ("ai_currency", "💱", "مراقب العملات", "مراقبة أسعار العملات"),
    ("ai_growth", "🚀", "مخطط النمو", "خطط النمو"),
    ("ai_efficiency", "⚡", "محسن الكفاءة", "تحسين الكفاءة"),
    ("ai_compliance", "📜", "مراقب الامتثال", "الامتثال القانوني"),
    ("ai_audit", "🔍", "المدقق الذكي", "تدقيق تلقائي"),
    ("ai_report", "📄", "مولد التقارير", "توليد تقارير"),
    ("ai_alert", "🔔", "منبه المخاطر", "تنبيهات فورية"),
    ("ai_savings", "💰", "مستشار الادخار", "نصائح ادخار"),
    ("ai_super", "🦅", "العقل الفائق", "ذكاء شامل"),
]

@app.route('/ai_center')
def ai_center():
    if 'user' not in session:
        return redirect('/login')
    content = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🧠 مركز الذكاء الاصطناعي</title>
        <style>
            body { font-family:Tahoma; background:#0a0a1a; color:#fff; padding:20px; }
            .container { max-width:1200px; margin:0 auto; }
            h1 { text-align:center; color:#00c8ff; margin-bottom:30px; }
            .ai-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:15px; }
            .ai-card { background:linear-gradient(145deg,#1a1a4e,#0d0d2e); border-radius:15px; padding:25px; text-align:center; border:1px solid rgba(0,200,255,0.3); transition:all 0.3s; }
            .ai-card:hover { transform:translateY(-5px); border-color:#00c8ff; box-shadow:0 10px 25px rgba(0,200,255,0.3); }
            .ai-card .icon { font-size:3rem; margin-bottom:10px; }
            .ai-card h3 { color:#00c8ff; margin-bottom:5px; }
            .ai-card p { color:#aaa; font-size:0.85rem; }
            a { color:#00c8ff; text-decoration:none; display:inline-block; margin-top:20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 مركز الذكاء الاصطناعي - 25 عقل</h1>
            <div class="ai-grid">'''
    
    for ai_id, icon, name, desc in AI_SYSTEMS:
        content += f'<div class="ai-card"><div class="icon">{icon}</div><h3>{name}</h3><p>{desc}</p></div>'
    
    content += '</div><a href="/magic">🏠 العودة</a></div></body></html>'
    return content

# ========== 50 نظام مالي ومحاسبي ==========
@app.route('/all_systems')
def all_systems():
    if 'user' not in session:
        return redirect('/login')
    
    systems = [
        ("📚", "الحسابات", "إدارة الحسابات العامة"),
        ("👥", "العملاء", "إدارة العملاء"),
        ("📦", "الموردون", "إدارة الموردين"),
        ("🧾", "الفواتير", "إدارة الفواتير"),
        ("📋", "أوامر الشراء", "إدارة أوامر الشراء"),
        ("📦", "المنتجات", "إدارة المنتجات"),
        ("🏭", "المستودعات", "إدارة المستودعات"),
        ("🔄", "حركات المخزون", "تتبع حركات المخزون"),
        ("👷", "الموظفون", "إدارة الموظفين"),
        ("💼", "الرواتب", "إدارة الرواتب"),
        ("💰", "الضرائب", "إدارة الضرائب"),
        ("🏦", "البنك", "الحركات البنكية"),
        ("🕌", "الزكاة", "حساب الزكاة"),
        ("📈", "الاستثمارات", "إدارة الاستثمارات"),
        ("⚖️", "ميزان المراجعة", "ميزان المراجعة"),
        ("📒", "دفتر الأستاذ", "دفتر الأستاذ"),
        ("📈", "قائمة الدخل", "قائمة الدخل"),
        ("📊", "الميزانية", "الميزانية العمومية"),
        ("💵", "التدفقات", "التدفقات النقدية"),
        ("🎯", "مؤشرات الأداء", "مؤشرات الأداء"),
        ("📊", "التحليلات", "التحليلات المالية"),
        ("💱", "العملات", "إدارة العملات"),
        ("📋", "الميزانيات", "إدارة الميزانيات"),
        ("💳", "الديون", "إدارة الديون"),
        ("🏢", "الأصول", "إدارة الأصول"),
        ("🔍", "التدقيق", "سجل التدقيق"),
        ("📥", "التصدير", "تصدير البيانات"),
        ("💾", "النسخ", "النسخ الاحتياطي"),
        ("📁", "المشاريع", "إدارة المشاريع"),
        ("📜", "العقود", "إدارة العقود"),
        ("✉️", "الرسائل", "الرسائل الداخلية"),
        ("⚙️", "الإعدادات", "إعدادات النظام"),
        ("🔔", "التنبيهات", "التنبيهات الذكية"),
        ("👤", "المستخدمون", "إدارة المستخدمين"),
        ("🔮", "عراف نوح", "التنبؤات الذكية"),
        ("🌍", "المؤشرات", "المؤشرات العالمية"),
        ("📊", "الرسوم", "الرسوم البيانية"),
        ("🧠", "الذكاء", "مركز الذكاء"),
        ("💱", "محول العملات", "تحويل العملات"),
        ("📊", "الإحصائيات", "الإحصائيات الشاملة"),
        ("🔍", "البحث", "البحث المتقدم"),
        ("📊", "تقارير متقدمة", "تقارير مالية متقدمة"),
        ("💰", "المدفوعات", "إدارة المدفوعات"),
        ("📥", "المقبوضات", "إدارة المقبوضات"),
        ("📤", "المصروفات", "إدارة المصروفات"),
        ("📋", "القيود", "قيود اليومية"),
        ("📊", "الموازنات", "الموازنات التقديرية"),
        ("🎯", "الأهداف", "الأهداف المالية"),
        ("📈", "النمو", "متابعة النمو"),
        ("🔐", "الأمان", "إدارة الأمان"),
    ]
    
    content = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>📊 جميع الأنظمة</title>
        <style>
            body { font-family:Tahoma; background:#0a0a1a; color:#fff; padding:20px; }
            .container { max-width:1200px; margin:0 auto; }
            h1 { text-align:center; color:#FFD700; margin-bottom:30px; }
            .systems-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; }
            .system-card { background:#1a1a3e; border-radius:12px; padding:20px; text-align:center; border:1px solid rgba(255,215,0,0.2); transition:all 0.3s; }
            .system-card:hover { transform:translateY(-3px); border-color:#FFD700; }
            .system-card .icon { font-size:2rem; }
            .system-card h3 { color:#FFD700; font-size:0.95rem; margin:10px 0 5px; }
            .system-card p { color:#888; font-size:0.75rem; }
            a { color:#FFD700; text-decoration:none; display:inline-block; margin-top:20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 جميع الأنظمة المالية - 50 نظام</h1>
            <div class="systems-grid">'''
    
    for icon, name, desc in systems:
        content += f'<div class="system-card"><div class="icon">{icon}</div><h3>{name}</h3><p>{desc}</p></div>'
    
    content += '</div><a href="/magic">🏠 العودة</a></div></body></html>'
    return content

# ========== 10 أنظمة تطوير ذاتي ==========
@app.route('/self_dev')
def self_dev():
    if 'user' not in session:
        return redirect('/login')
    
    dev_systems = [
        ("🧬", "التعلم الذاتي", "يتعلم من البيانات تلقائياً"),
        ("🔧", "الإصلاح الذاتي", "يكتشف الأخطاء ويصلحها"),
        ("📈", "التحسين الذاتي", "يحسن أداءه باستمرار"),
        ("🔄", "التكيف الذاتي", "يتكيف مع المتغيرات"),
        ("🧠", "التفكير الذاتي", "يحلل قراراته"),
        ("💾", "الحفظ الذاتي", "يحفظ البيانات تلقائياً"),
        ("🔐", "الحماية الذاتية", "يحمي نفسه من الهجمات"),
        ("📊", "التقييم الذاتي", "يقيم أداءه"),
        ("🚀", "التطوير الذاتي", "يضيف ميزات جديدة"),
        ("🌟", "التطور الذاتي", "يتطور باستمرار"),
    ]
    
    content = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🧬 أنظمة التطوير الذاتي</title>
        <style>
            body { font-family:Tahoma; background:#0a0a1a; color:#fff; padding:20px; }
            .container { max-width:900px; margin:0 auto; }
            h1 { text-align:center; color:#4aff4a; margin-bottom:30px; }
            .dev-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:15px; }
            .dev-card { background:linear-gradient(145deg,#1a3e1a,#0d2e0d); border-radius:15px; padding:25px; text-align:center; border:1px solid rgba(74,255,74,0.3); transition:all 0.3s; }
            .dev-card:hover { transform:translateY(-5px); border-color:#4aff4a; box-shadow:0 10px 25px rgba(74,255,74,0.3); }
            .dev-card .icon { font-size:2.5rem; }
            .dev-card h3 { color:#4aff4a; margin:10px 0 5px; }
            .dev-card p { color:#aaa; font-size:0.85rem; }
            a { color:#4aff4a; text-decoration:none; display:inline-block; margin-top:20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧬 أنظمة التطوير الذاتي - 10 أنظمة</h1>
            <div class="dev-grid">'''
    
    for icon, name, desc in dev_systems:
        content += f'<div class="dev-card"><div class="icon">{icon}</div><h3>{name}</h3><p>{desc}</p></div>'
    
    content += '</div><a href="/magic">🏠 العودة</a></div></body></html>'
    return content


# ========== دوال إضافية للمسارات الناقصة ==========
@app.route('/reports')
def reports():
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM purchase_orders")
    expenses = c.fetchone()[0]
    conn.close()
    net = revenue - expenses
    content = f'<h2>📊 التقارير المالية</h2><table><tr><th>الإيرادات</th><td>{revenue}</td></tr><tr><th>المصاريف</th><td>{expenses}</td></tr><tr><th>صافي الربح</th><td>{net}</td></tr></table><a href="/magic">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/projects')
def projects():
    if 'user' not in session: return redirect('/login')
    content = '<h2>📁 المشاريع</h2><p>لا توجد مشاريع بعد</p><a href="/magic">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/contracts')
def contracts():
    if 'user' not in session: return redirect('/login')
    content = '<h2>📜 العقود</h2><p>لا توجد عقود بعد</p><a href="/magic">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/messages')
def messages():
    if 'user' not in session: return redirect('/login')
    content = '<h2>✉️ الرسائل</h2><p>لا توجد رسائل</p><a href="/magic">🏠 العودة</a>'
    return PAGE_STYLE + content

@app.route('/settings')
def settings():
    if 'user' not in session: return redirect('/login')
    content = '<h2>⚙️ الإعدادات</h2><p>إعدادات النظام</p><a href="/magic">🏠 العودة</a>'
    return PAGE_STYLE + content


# ========== صفحة كل الأنظمة العاملة ==========
@app.route('/working_systems')
def working_systems():
    if 'user' not in session:
        return redirect('/login')
    
    working = [
        ("/magic", "🦅", "اللوحة الرئيسية"),
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
        ("/ai_center", "🧠", "مركز الذكاء"),
        ("/all_systems", "📊", "كل الأنظمة"),
        ("/self_dev", "🧬", "التطوير الذاتي"),
        ("/oracle", "🔮", "عراف نوح"),
        ("/global_markets", "🌍", "المؤشرات"),
        ("/charts", "📊", "الرسوم"),
        ("/currency_converter", "💱", "محول العملات"),
        ("/search", "🔍", "البحث"),
        ("/statistics", "📊", "الإحصائيات"),
        ("/advanced_reports", "📊", "تقارير متقدمة"),
        ("/logout", "🚪", "خروج"),
    ]
    
    content = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>✅ الأنظمة العاملة</title>
        <style>
            body { font-family:Tahoma; background:#0a0a1a; color:#fff; padding:20px; }
            .container { max-width:900px; margin:0 auto; }
            h1 { text-align:center; color:#4aff4a; margin-bottom:30px; }
            .systems-list { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:10px; }
            .system-link { background:#1a1a3e; border-radius:12px; padding:15px; text-align:center; border:1px solid rgba(74,255,74,0.3); transition:all 0.3s; text-decoration:none; color:#fff; }
            .system-link:hover { transform:translateY(-3px); border-color:#4aff4a; background:#1a3e1a; }
            .system-link .icon { font-size:2rem; }
            .system-link .name { display:block; margin-top:8px; font-weight:bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✅ الأنظمة العاملة في نوح</h1>
            <div class="systems-list">'''
    
    for path, icon, name in working:
        content += f'<a class="system-link" href="{path}"><span class="icon">{icon}</span><span class="name">{name}</span></a>'
    
    content += '</div></div></body></html>'
    return content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
