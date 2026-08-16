#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, request, render_template_string, redirect, url_for
import csv, io

app = Flask(__name__)

# ========== قاعدة البيانات ==========
def init_db():
    conn = sqlite3.connect('accounting_ultra.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        type TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        description TEXT,
        debit_account TEXT,
        credit_account TEXT,
        amount REAL
    )''')
    default_accounts = [
        ('الصندوق', 'أصول'), ('البنك', 'أصول'), ('رأس المال', 'حقوق ملكية'),
        ('المبيعات', 'إيرادات'), ('المشتريات', 'مصاريف'), ('المصاريف العامة', 'مصاريف')
    ]
    for name, typ in default_accounts:
        c.execute("INSERT OR IGNORE INTO accounts (name, type) VALUES (?, ?)", (name, typ))
    conn.commit()
    conn.close()

init_db()

# ========== ذاكرة سريعة ==========
cache = {'accounts': None, 'transactions': None}

def refresh_cache():
    conn = sqlite3.connect('accounting_ultra.db')
    c = conn.cursor()
    c.execute("SELECT id, name, type FROM accounts ORDER BY type, name")
    cache['accounts'] = c.fetchall()
    c.execute("SELECT id, date, description, debit_account, credit_account, amount FROM transactions ORDER BY date DESC, id DESC")
    cache['transactions'] = c.fetchall()
    conn.close()

refresh_cache()

# ========== دوال حساب ==========
def get_balance_fast(account):
    debit = sum(t[5] for t in cache['transactions'] if t[3] == account)
    credit = sum(t[5] for t in cache['transactions'] if t[4] == account)
    return debit - credit

def total_by_type(typ):
    accounts = [a[1] for a in cache['accounts'] if a[2] == typ]
    return sum(get_balance_fast(a) for a in accounts)

# ========== واجهة ==========
BASE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نوح للمحاسبة الفائقة</title>
    <style>
        body { font-family: Tahoma; background: #0a0a1a; color: #eee; padding: 20px; }
        a { color: #4a4aff; text-decoration: none; margin: 5px; }
        input, select, button { padding: 8px; margin: 5px; border-radius: 5px; border: 1px solid #555; background: #222; color: #eee; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #444; padding: 8px; text-align: center; }
        th { background: #333; }
        .nav { background: #1a1a3e; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
        .summary { display: flex; gap: 20px; margin: 15px 0; }
        .card { background: #151530; border: 1px solid #4a4aff; border-radius: 10px; padding: 15px; flex: 1; text-align: center; }
        .card h3 { color: #ffd700; }
        .card p { font-size: 1.5em; }
        .search-box { width: 100%; padding: 10px; background: #1a1a3e; border: 1px solid #4a4aff; color: #eee; border-radius: 5px; }
        .danger { background: #5e1111; }
    </style>
</head>
<body>
    <h1>🦅 نوح للمحاسبة الفائقة</h1>
    <div class="nav">
        <a href="/">🏠 الرئيسية</a>
        <a href="/accounts">📚 الحسابات</a>
        <a href="/transactions">✍️ القيود</a>
        <a href="/ledger">📒 دفتر الأستاذ</a>
        <a href="/trial_balance">⚖️ ميزان المراجعة</a>
        <a href="/income_statement">📈 قائمة الدخل</a>
        <a href="/balance_sheet">📊 الميزانية العمومية</a>
        <a href="/export">📥 تصدير</a>
    </div>
    <div class="summary">
        <div class="card"><h3>إجمالي الأصول</h3><p>{{ assets }}</p></div>
        <div class="card"><h3>إجمالي الإيرادات</h3><p>{{ revenues }}</p></div>
        <div class="card"><h3>صافي الربح</h3><p>{{ net }}</p></div>
    </div>
    {% block content %}{% endblock %}
</body>
</html>
"""

@app.context_processor
def inject_summary():
    assets = total_by_type('أصول')
    revenues = total_by_type('إيرادات')
    expenses = total_by_type('مصاريف')
    net = revenues - expenses
    return dict(assets=assets, revenues=revenues, net=net)

# ========== الرئيسية ==========
@app.route('/')
def index():
    content = "<h2>اختر من القائمة أعلاه</h2>"
    return render_template_string(BASE, content=content)

# ========== الحسابات ==========
@app.route('/accounts', methods=['GET', 'POST'])
def accounts():
    if request.method == 'POST':
        name = request.form['name'].strip()
        typ = request.form['type']
        if name:
            conn = sqlite3.connect('accounting_ultra.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO accounts (name, type) VALUES (?, ?)", (name, typ))
                conn.commit()
            except sqlite3.IntegrityError:
                pass
            conn.close()
            refresh_cache()
        return redirect('/accounts')
    content = """
        <h2>📚 إدارة الحسابات</h2>
        <input type="text" class="search-box" id="accSearch" placeholder="🔍 بحث فوري في الحسابات...">
        <form method="POST">
            <input type="text" name="name" placeholder="اسم الحساب" required>
            <select name="type">
                <option>أصول</option><option>خصوم</option><option>حقوق ملكية</option>
                <option>إيرادات</option><option>مصاريف</option>
            </select>
            <button type="submit">➕ إضافة</button>
        </form>
        <table id="accTable">
            <tr><th>الاسم</th><th>النوع</th></tr>
            {% for acc in accounts %}
            <tr><td>{{ acc[1] }}</td><td>{{ acc[2] }}</td></tr>
            {% endfor %}
        </table>
        <script>
        document.getElementById('accSearch').addEventListener('input', function() {
            let q = this.value.toLowerCase();
            let rows = document.querySelectorAll('#accTable tr');
            rows.forEach((row, i) => {
                if (i === 0) return;
                row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
            });
        });
        </script>
    """
    return render_template_string(BASE, content=content, accounts=cache['accounts'])

# ========== القيود ==========
@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        date = request.form['date']
        desc = request.form['description']
        debit = request.form['debit']
        credit = request.form['credit']
        amount = float(request.form['amount'])
        conn = sqlite3.connect('accounting_ultra.db')
        c = conn.cursor()
        c.execute("INSERT INTO transactions (date, description, debit_account, credit_account, amount) VALUES (?,?,?,?,?)",
                  (date, desc, debit, credit, amount))
        conn.commit()
        conn.close()
        refresh_cache()
        return redirect('/transactions')
    acc_names = [a[1] for a in cache['accounts']]
    content = """
        <h2>✍️ إضافة قيد مزدوج</h2>
        <form method="POST">
            <input type="date" name="date" required>
            <input type="text" name="description" placeholder="البيان" required>
            <select name="debit" required>{% for n in acc_names %}<option>{{ n }}</option>{% endfor %}</select>
            <select name="credit" required>{% for n in acc_names %}<option>{{ n }}</option>{% endfor %}</select>
            <input type="number" step="0.01" name="amount" placeholder="المبلغ" required>
            <button type="submit">➕ إضافة قيد</button>
        </form>
        <h3>أحدث القيود</h3>
        <table>
            <tr><th>التاريخ</th><th>البيان</th><th>مدين</th><th>دائن</th><th>المبلغ</th></tr>
            {% for t in trans %}
            <tr><td>{{ t[1] }}</td><td>{{ t[2] }}</td><td>{{ t[3] }}</td><td>{{ t[4] }}</td><td>{{ t[5] }}</td></tr>
            {% endfor %}
        </table>
    """
    return render_template_string(BASE, content=content, acc_names=acc_names, trans=cache['transactions'])

# ========== دفتر الأستاذ ==========
@app.route('/ledger')
def ledger():
    ledger_data = []
    for acc in cache['accounts']:
        name = acc[1]
        moves = [t for t in cache['transactions'] if t[3] == name or t[4] == name]
        ledger_data.append((name, moves, get_balance_fast(name)))
    content = """
        <h2>📒 دفتر الأستاذ</h2>
        {% for name, moves, bal in ledger %}
        <h3>{{ name }} (الرصيد: {{ bal }})</h3>
        <table>
            <tr><th>التاريخ</th><th>البيان</th><th>المبلغ</th><th>النوع</th></tr>
            {% for m in moves %}
            <tr><td>{{ m[1] }}</td><td>{{ m[2] }}</td><td>{{ m[5] }}</td><td>{{ 'مدين' if m[3] == name else 'دائن' }}</td></tr>
            {% endfor %}
        </table>
        {% endfor %}
    """
    return render_template_string(BASE, content=content, ledger=ledger_data)

# ========== ميزان المراجعة ==========
@app.route('/trial_balance')
def trial_balance():
    tb = []
    for acc in cache['accounts']:
        name = acc[1]
        bal = get_balance_fast(name)
        tb.append((name, bal if bal > 0 else 0, -bal if bal < 0 else 0))
    content = """
        <h2>⚖️ ميزان المراجعة</h2>
        <table>
            <tr><th>الحساب</th><th>مدين</th><th>دائن</th></tr>
            {% for row in tb %}
            <tr><td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>{{ row[2] }}</td></tr>
            {% endfor %}
        </table>
    """
    return render_template_string(BASE, content=content, tb=tb)

# ========== قائمة الدخل ==========
@app.route('/income_statement')
def income_statement():
    revenues = total_by_type('إيرادات')
    expenses = total_by_type('مصاريف')
    net = revenues - expenses
    content = f"""
        <h2>📈 قائمة الدخل</h2>
        <table>
            <tr><th>الإيرادات</th><td>{revenues}</td></tr>
            <tr><th>المصاريف</th><td>{expenses}</td></tr>
            <tr><th>صافي الربح</th><td>{net}</td></tr>
        </table>
    """
    return render_template_string(BASE, content=content)

# ========== الميزانية العمومية ==========
@app.route('/balance_sheet')
def balance_sheet():
    assets = total_by_type('أصول')
    liabilities = total_by_type('خصوم')
    equity = total_by_type('حقوق ملكية')
    content = f"""
        <h2>📊 الميزانية العمومية</h2>
        <table>
            <tr><th>الأصول</th><td>{assets}</td></tr>
            <tr><th>الخصوم</th><td>{liabilities}</td></tr>
            <tr><th>حقوق الملكية</th><td>{equity}</td></tr>
            <tr><th>التحقق</th><td>{'✅ متوازن' if abs(assets - (liabilities + equity)) < 0.01 else '❌ غير متوازن'}</td></tr>
        </table>
    """
    return render_template_string(BASE, content=content)

# ========== تصدير ==========
@app.route('/export')
def export_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['التاريخ', 'البيان', 'مدين', 'دائن', 'المبلغ'])
    for t in cache['transactions']:
        writer.writerow([t[1], t[2], t[3], t[4], t[5]])
    return f"<pre>{output.getvalue()}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)
