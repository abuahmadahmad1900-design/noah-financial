from flask import Flask, render_template_string, request, session, redirect
import sqlite3

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
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect('/')
        return 'خطأ في الدخول'
    return '''
    <form method="POST">
        <input type="text" name="username" placeholder="المستخدم" required>
        <input type="password" name="password" placeholder="كلمة المرور" required>
        <button>دخول</button>
    </form>'''

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')
    return redirect('/legendary')

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
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    revenue = c.fetchone()[0]
    conn.close()

    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>نوح - لوحة القيادة الأسطورية</title>
        <style>
            body {{
                font-family: Tahoma;
                background: #0a0a2e;
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
                border: 1px solid rgba(255,215,0,0.4);
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
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
            }}
            .subtitle {{
                text-align: center;
                color: #aaa;
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

            <div class="nav-links">
                <a href="/accounts">📚 الحسابات</a>
                <a href="/customers">👥 العملاء</a>
                <a href="/suppliers">📦 الموردون</a>
                <a href="/invoices">🧾 الفواتير</a>
                <a href="/products">📦 المنتجات</a>
                <a href="/logout">🚪 خروج</a>
            </div>
        </div>
    </body>
    </html>
    '''


# ========== لوحة التحكم الخيالية ==========
@app.route('/legendary_v2')
def legendary_v2():
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
        <title>🦅 نوح - لوحة القيادة الخيالية</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: Tahoma, sans-serif;
                background: #0a0a1a;
                color: #fff;
                min-height: 100vh;
                overflow-x: hidden;
                position: relative;
            }}
            /* جزيئات متحركة */
            .particle {{
                position: fixed;
                border-radius: 50%;
                background: rgba(0,200,255,0.6);
                pointer-events: none;
                animation: float-particle linear infinite;
            }}
            @keyframes float-particle {{
                0% {{ transform: translateY(100vh) scale(0); opacity: 0; }}
                10% {{ opacity: 1; }}
                90% {{ opacity: 1; }}
                100% {{ transform: translateY(-10vh) scale(1); opacity: 0; }}
            }}
            .main-container {{
                position: relative;
                z-index: 2;
                max-width: 1200px;
                margin: 0 auto;
                padding: 30px 20px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 50px;
            }}
            .header h1 {{
                font-size: 3.5rem;
                font-weight: 900;
                background: linear-gradient(45deg, #FFD700, #FF8C00, #FFD700, #FF8C00);
                background-size: 300% 300%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gradient-shift 3s ease infinite, pulse-glow 2s ease-in-out infinite alternate;
                margin-bottom: 15px;
            }}
            @keyframes gradient-shift {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            @keyframes pulse-glow {{
                from {{ text-shadow: 0 0 10px #FFD700, 0 0 20px #FFA500; }}
                to {{ text-shadow: 0 0 30px #FFD700, 0 0 60px #FF8C00; }}
            }}
            .header .subtitle {{
                color: #ccc;
                font-size: 1.2rem;
                letter-spacing: 2px;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 25px;
                margin-bottom: 40px;
            }}
            .stat-card {{
                background: linear-gradient(145deg, rgba(30,30,70,0.9), rgba(15,15,40,0.9));
                border-radius: 25px;
                padding: 30px 20px;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.15);
                box-shadow: 0 10px 40px rgba(0,0,0,0.5), 0 0 20px rgba(0,200,255,0.1) inset;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                cursor: pointer;
                position: relative;
                overflow: hidden;
            }}
            .stat-card::before {{
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: conic-gradient(from 0deg, transparent, rgba(0,200,255,0.15), transparent, rgba(255,215,0,0.15), transparent);
                animation: rotate-border 4s linear infinite;
            }}
            @keyframes rotate-border {{
                100% {{ transform: rotate(360deg); }}
            }}
            .stat-card:hover {{
                transform: translateY(-15px) scale(1.05);
                box-shadow: 0 20px 50px rgba(0,200,255,0.3), 0 0 30px rgba(0,200,255,0.4) inset;
                border-color: #00c8ff;
            }}
            .stat-card .icon {{
                font-size: 3.5rem;
                margin-bottom: 15px;
                position: relative;
                z-index: 1;
                animation: bounce-icon 2s ease-in-out infinite;
            }}
            @keyframes bounce-icon {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-10px); }}
            }}
            .stat-card .value {{
                font-size: 2.8rem;
                font-weight: 900;
                color: #fff;
                text-shadow: 0 0 20px rgba(0,200,255,0.7);
                position: relative;
                z-index: 1;
            }}
            .stat-card .label {{
                color: #aaa;
                font-size: 1rem;
                margin-top: 10px;
                position: relative;
                z-index: 1;
            }}
            .revenue-section {{
                background: linear-gradient(145deg, rgba(40,40,90,0.95), rgba(20,20,50,0.95));
                border-radius: 30px;
                padding: 40px;
                text-align: center;
                margin-bottom: 40px;
                border: 1px solid rgba(255,215,0,0.4);
                box-shadow: 0 15px 40px rgba(0,0,0,0.6), 0 0 30px rgba(255,215,0,0.2);
                position: relative;
                overflow: hidden;
            }}
            .revenue-section::before {{
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,215,0,0.1), transparent 70%);
                animation: pulse-bg 3s ease-in-out infinite;
            }}
            @keyframes pulse-bg {{
                0%, 100% {{ transform: scale(1); opacity: 0.5; }}
                50% {{ transform: scale(1.2); opacity: 1; }}
            }}
            .revenue-section h2 {{
                color: #FFD700;
                font-size: 1.8rem;
                margin-bottom: 20px;
                position: relative;
                z-index: 1;
            }}
            .revenue-section .amount {{
                font-size: 4rem;
                font-weight: 900;
                background: linear-gradient(45deg, #FFD700, #FF8C00, #FFD700);
                background-size: 200% 200%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gradient-shift 2s ease infinite;
                position: relative;
                z-index: 1;
            }}
            .quick-actions {{
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                justify-content: center;
                margin-top: 30px;
            }}
            .quick-actions a {{
                background: linear-gradient(145deg, #222244, #111133);
                color: #fff;
                padding: 15px 30px;
                border-radius: 50px;
                text-decoration: none;
                font-size: 1rem;
                border: 1px solid rgba(255,255,255,0.25);
                transition: all 0.4s;
                position: relative;
                overflow: hidden;
            }}
            .quick-actions a::before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }}
            .quick-actions a:hover::before {{
                left: 100%;
            }}
            .quick-actions a:hover {{
                background: #00c8ff;
                color: #000;
                transform: scale(1.1);
                box-shadow: 0 0 30px rgba(0,200,255,0.6);
            }}
        </style>
    </head>
    <body>
        <div class="main-container">
            <div class="header">
                <h1>🦅 نوح - لوحة القيادة الخيالية</h1>
                <p class="subtitle">النظام المالي الأسطوري الذي لا يُهزم</p>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="icon">📚</div>
                    <div class="value" data-target="{accounts}">0</div>
                    <div class="label">الحسابات</div>
                </div>
                <div class="stat-card">
                    <div class="icon">👥</div>
                    <div class="value" data-target="{customers}">0</div>
                    <div class="label">العملاء</div>
                </div>
                <div class="stat-card">
                    <div class="icon">📦</div>
                    <div class="value" data-target="{suppliers}">0</div>
                    <div class="label">الموردون</div>
                </div>
                <div class="stat-card">
                    <div class="icon">🧾</div>
                    <div class="value" data-target="{invoices}">0</div>
                    <div class="label">الفواتير</div>
                </div>
                <div class="stat-card">
                    <div class="icon">📦</div>
                    <div class="value" data-target="{products}">0</div>
                    <div class="label">المنتجات</div>
                </div>
            </div>

            <div class="revenue-section">
                <h2>💰 إجمالي الإيرادات</h2>
                <div class="amount" id="revenue-counter">{revenue}</div>
            </div>

            <div class="quick-actions">
                <a href="/accounts">📚 الحسابات</a>
                <a href="/customers">👥 العملاء</a>
                <a href="/suppliers">📦 الموردون</a>
                <a href="/invoices">🧾 الفواتير</a>
                <a href="/products">📦 المنتجات</a>
                <a href="/logout">🚪 خروج</a>
            </div>
        </div>

        <script>
            // جزيئات متحركة
            for (let i = 0; i < 50; i++) {{
                const particle = document.createElement('div');
                particle.classList.add('particle');
                particle.style.left = Math.random() * 100 + '%';
                particle.style.width = Math.random() * 5 + 2 + 'px';
                particle.style.height = particle.style.width;
                particle.style.animationDuration = Math.random() * 10 + 5 + 's';
                particle.style.animationDelay = Math.random() * 10 + 's';
                document.body.appendChild(particle);
            }}

            // عدادات متحركة
            document.querySelectorAll('.value').forEach(el => {{
                const target = parseInt(el.getAttribute('data-target'));
                let current = 0;
                const step = Math.max(1, Math.floor(target / 50));
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

            // عداد الإيرادات
            const revEl = document.getElementById('revenue-counter');
            const revTarget = parseInt(revEl.textContent);
            let revCurrent = 0;
            const revInterval = setInterval(() => {{
                revCurrent += Math.max(1, Math.floor(revTarget / 100));
                if (revCurrent >= revTarget) {{
                    revEl.textContent = revTarget;
                    clearInterval(revInterval);
                }} else {{
                    revEl.textContent = revCurrent;
                }}
            }}, 20);
        </script>
    </body>
    </html>
    '''


# ========== لوحة التحكم الساحرة ==========
@app.route('/magical')
def magical():
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
    c.execute("SELECT COALESCE(SUM(stock),0) FROM products")
    total_stock = c.fetchone()[0]
    conn.close()

    # حساب نسبة المخزون (افتراض أن الحد الأقصى 1000)
    stock_percent = min(total_stock / 10, 100) if total_stock > 0 else 0

    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🦅 نوح - السحر المالي</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: Tahoma, sans-serif;
                background: #000011;
                color: #fff;
                min-height: 100vh;
                overflow-x: hidden;
                position: relative;
                cursor: default;
            }}
            /* نجوم متحركة */
            .star {{
                position: fixed;
                border-radius: 50%;
                background: #fff;
                pointer-events: none;
                animation: twinkle ease-in-out infinite;
            }}
            @keyframes twinkle {{
                0%, 100% {{ opacity: 0.3; transform: scale(1); }}
                50% {{ opacity: 1; transform: scale(1.5); }}
            }}
            /* مجرة دوارة */
            .galaxy {{
                position: fixed;
                top: 50%;
                left: 50%;
                width: 800px;
                height: 800px;
                background: radial-gradient(circle, rgba(100,50,200,0.15), transparent 60%);
                border-radius: 50%;
                pointer-events: none;
                animation: rotate-galaxy 30s linear infinite;
                z-index: 0;
            }}
            @keyframes rotate-galaxy {{
                from {{ transform: translate(-50%, -50%) rotate(0deg); }}
                to {{ transform: translate(-50%, -50%) rotate(360deg); }}
            }}
            .main-container {{
                position: relative;
                z-index: 2;
                max-width: 1200px;
                margin: 0 auto;
                padding: 30px 20px;
            }}
            /* ساعة حية */
            .clock {{
                position: absolute;
                top: 20px;
                left: 20px;
                color: #FFD700;
                font-size: 1.2rem;
                text-shadow: 0 0 10px rgba(255,215,0,0.5);
                z-index: 10;
            }}
            .header {{
                text-align: center;
                margin-bottom: 50px;
            }}
            .header h1 {{
                font-size: 3.5rem;
                font-weight: 900;
                background: linear-gradient(45deg, #FFD700, #FF8C00, #FFD700, #FF8C00);
                background-size: 300% 300%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gradient-shift 3s ease infinite, pulse-glow 2s ease-in-out infinite alternate;
                margin-bottom: 15px;
                cursor: default;
            }}
            @keyframes gradient-shift {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            @keyframes pulse-glow {{
                from {{ text-shadow: 0 0 10px #FFD700, 0 0 20px #FFA500; }}
                to {{ text-shadow: 0 0 30px #FFD700, 0 0 60px #FF8C00; }}
            }}
            .header .subtitle {{
                color: #ccc;
                font-size: 1.2rem;
                letter-spacing: 2px;
                animation: fade-in-out 3s ease-in-out infinite;
            }}
            @keyframes fade-in-out {{
                0%, 100% {{ opacity: 0.6; }}
                50% {{ opacity: 1; }}
            }}
            /* بطاقات ثلاثية الأبعاد */
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 25px;
                margin-bottom: 40px;
                perspective: 1000px;
            }}
            .stat-card {{
                background: linear-gradient(145deg, rgba(30,30,70,0.9), rgba(15,15,40,0.9));
                border-radius: 25px;
                padding: 30px 20px;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.15);
                box-shadow: 0 10px 40px rgba(0,0,0,0.5), 0 0 20px rgba(0,200,255,0.1) inset;
                transition: transform 0.1s ease-out;
                cursor: pointer;
                position: relative;
                overflow: hidden;
                transform-style: preserve-3d;
            }}
            .stat-card::before {{
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: conic-gradient(from 0deg, transparent, rgba(0,200,255,0.2), transparent, rgba(255,215,0,0.2), transparent);
                animation: rotate-border 4s linear infinite;
            }}
            @keyframes rotate-border {{
                100% {{ transform: rotate(360deg); }}
            }}
            .stat-card .icon {{
                font-size: 3.5rem;
                margin-bottom: 15px;
                position: relative;
                z-index: 1;
                animation: bounce-icon 2s ease-in-out infinite;
                filter: drop-shadow(0 0 10px rgba(0,200,255,0.5));
            }}
            @keyframes bounce-icon {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-10px); }}
            }}
            .stat-card .value {{
                font-size: 2.8rem;
                font-weight: 900;
                color: #fff;
                text-shadow: 0 0 20px rgba(0,200,255,0.7);
                position: relative;
                z-index: 1;
            }}
            .stat-card .label {{
                color: #aaa;
                font-size: 1rem;
                margin-top: 10px;
                position: relative;
                z-index: 1;
            }}
            /* قسم الإيرادات */
            .revenue-section {{
                background: linear-gradient(145deg, rgba(40,40,90,0.95), rgba(20,20,50,0.95));
                border-radius: 30px;
                padding: 40px;
                text-align: center;
                margin-bottom: 30px;
                border: 1px solid rgba(255,215,0,0.4);
                box-shadow: 0 15px 40px rgba(0,0,0,0.6), 0 0 30px rgba(255,215,0,0.2);
                position: relative;
                overflow: hidden;
            }}
            .revenue-section::before {{
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,215,0,0.15), transparent 70%);
                animation: pulse-bg 3s ease-in-out infinite;
            }}
            @keyframes pulse-bg {{
                0%, 100% {{ transform: scale(1); opacity: 0.5; }}
                50% {{ transform: scale(1.3); opacity: 1; }}
            }}
            .revenue-section h2 {{
                color: #FFD700;
                font-size: 1.8rem;
                margin-bottom: 20px;
                position: relative;
                z-index: 1;
            }}
            .revenue-section .amount {{
                font-size: 4rem;
                font-weight: 900;
                background: linear-gradient(45deg, #FFD700, #FF8C00, #FFD700);
                background-size: 200% 200%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gradient-shift 2s ease infinite;
                position: relative;
                z-index: 1;
            }}
            /* شريط التقدم */
            .progress-container {{
                margin: 30px 0;
                background: rgba(0,0,0,0.3);
                border-radius: 20px;
                padding: 20px;
            }}
            .progress-bar {{
                width: 100%;
                height: 30px;
                background: #1a1a3e;
                border-radius: 15px;
                overflow: hidden;
                position: relative;
            }}
            .progress-fill {{
                height: 100%;
                background: linear-gradient(90deg, #00c8ff, #FFD700);
                border-radius: 15px;
                animation: progress-shine 2s ease-in-out infinite;
                transition: width 1s ease-out;
            }}
            @keyframes progress-shine {{
                0% {{ filter: brightness(1); }}
                50% {{ filter: brightness(1.5); }}
                100% {{ filter: brightness(1); }}
            }}
            .progress-label {{
                color: #ccc;
                margin-top: 10px;
                text-align: center;
            }}
            /* أزرار سريعة */
            .quick-actions {{
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                justify-content: center;
                margin-top: 30px;
            }}
            .quick-actions a {{
                background: linear-gradient(145deg, #222244, #111133);
                color: #fff;
                padding: 15px 30px;
                border-radius: 50px;
                text-decoration: none;
                font-size: 1rem;
                border: 1px solid rgba(255,255,255,0.25);
                transition: all 0.4s;
                position: relative;
                overflow: hidden;
            }}
            .quick-actions a::before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
                transition: left 0.5s;
            }}
            .quick-actions a:hover::before {{
                left: 100%;
            }}
            .quick-actions a:hover {{
                background: #00c8ff;
                color: #000;
                transform: scale(1.1);
                box-shadow: 0 0 30px rgba(0,200,255,0.6);
            }}
        </style>
    </head>
    <body>
        <div class="clock" id="clock"></div>
        <div class="galaxy"></div>

        <div class="main-container">
            <div class="header">
                <h1>🦅 نوح - السحر المالي</h1>
                <p class="subtitle">حيث تلتقي القوة بالذكاء والبراعة</p>
            </div>

            <div class="stats-grid" id="stats-grid">
                <div class="stat-card" data-tilt>
                    <div class="icon">📚</div>
                    <div class="value" data-target="{accounts}">0</div>
                    <div class="label">الحسابات</div>
                </div>
                <div class="stat-card" data-tilt>
                    <div class="icon">👥</div>
                    <div class="value" data-target="{customers}">0</div>
                    <div class="label">العملاء</div>
                </div>
                <div class="stat-card" data-tilt>
                    <div class="icon">📦</div>
                    <div class="value" data-target="{suppliers}">0</div>
                    <div class="label">الموردون</div>
                </div>
                <div class="stat-card" data-tilt>
                    <div class="icon">🧾</div>
                    <div class="value" data-target="{invoices}">0</div>
                    <div class="label">الفواتير</div>
                </div>
                <div class="stat-card" data-tilt>
                    <div class="icon">📦</div>
                    <div class="value" data-target="{products}">0</div>
                    <div class="label">المنتجات</div>
                </div>
            </div>

            <div class="revenue-section">
                <h2>💰 إجمالي الإيرادات</h2>
                <div class="amount" id="revenue-counter">{revenue}</div>
            </div>

            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" id="stock-bar" style="width: 0%;"></div>
                </div>
                <div class="progress-label">📊 مستوى المخزون: <span id="stock-percent">0%</span></div>
            </div>

            <div class="quick-actions">
                <a href="/accounts">📚 الحسابات</a>
                <a href="/customers">👥 العملاء</a>
                <a href="/suppliers">📦 الموردون</a>
                <a href="/invoices">🧾 الفواتير</a>
                <a href="/products">📦 المنتجات</a>
                <a href="/logout">🚪 خروج</a>
            </div>
        </div>

        <script>
            // ساعة حية
            function updateClock() {{
                const now = new Date();
                const time = now.toLocaleTimeString('ar');
                const date = now.toLocaleDateString('ar', {{ weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }});
                document.getElementById('clock').innerHTML = date + ' - ' + time;
            }}
            updateClock();
            setInterval(updateClock, 1000);

            // نجوم متلألئة
            for (let i = 0; i < 100; i++) {{
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

            // عدادات متحركة
            document.querySelectorAll('.value').forEach(el => {{
                const target = parseInt(el.getAttribute('data-target'));
                let current = 0;
                const step = Math.max(1, Math.floor(target / 60));
                const interval = setInterval(() => {{
                    current += step;
                    if (current >= target) {{
                        el.textContent = target;
                        clearInterval(interval);
                    }} else {{
                        el.textContent = current;
                    }}
                }}, 25);
            }});

            // عداد الإيرادات
            const revEl = document.getElementById('revenue-counter');
            const revTarget = parseInt(revEl.textContent);
            let revCurrent = 0;
            const revInterval = setInterval(() => {{
                revCurrent += Math.max(1, Math.floor(revTarget / 120));
                if (revCurrent >= revTarget) {{
                    revEl.textContent = revTarget;
                    clearInterval(revInterval);
                }} else {{
                    revEl.textContent = revCurrent;
                }}
            }}, 15);

            // شريط المخزون
            setTimeout(() => {{
                document.getElementById('stock-bar').style.width = '{stock_percent}%';
                document.getElementById('stock-percent').textContent = '{stock_percent:.1f}%';
            }}, 500);

            // تأثير ثلاثي الأبعاد عند تحريك الماوس
            document.querySelectorAll('[data-tilt]').forEach(card => {{
                card.addEventListener('mousemove', (e) => {{
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;
                    const rotateX = (y - centerY) / 20;
                    const rotateY = (centerX - x) / 20;
                    card.style.transform = `perspective(1000px) rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg) translateY(-10px)`;
                }});
                card.addEventListener('mouseleave', () => {{
                    card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
                }});
            }});
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
