#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, request, render_template_string, redirect, url_for
import csv
import io

app = Flask(__name__)

# ========== إنشاء قاعدة البيانات ==========
def init_db():
    conn = sqlite3.connect('accounting.db')
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
    # حسابات افتراضية
    default_accounts = [
        ('الصندوق', 'أصول'),
        ('البنك', 'أصول'),
        ('رأس المال', 'حقوق ملكية'),
        ('المبيعات', 'إيرادات'),
        ('المشتريات', 'مصاريف'),
        ('المصاريف العامة', 'مصاريف')
    ]
    for name, typ in default_accounts:
        c.execute("INSERT OR IGNORE INTO accounts (name, type) VALUES (?, ?)", (name, typ))
    conn.commit()
    conn.close()

init_db()

# ========== دوال مساعدة ==========
def get_accounts():
    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    c.execute("SELECT id, name, type FROM accounts ORDER BY type, name")
    rows = c.fetchall()
    conn.close()
    return rows

def get_account_names():
    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    c.execute("SELECT name FROM accounts ORDER BY name")
    rows = [r[0] for r in c.fetchall()]
    conn.close()
    return rows

def get_transactions():
    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    c.execute("SELECT date, description, debit_account, credit_account, amount FROM transactions ORDER BY date, id")
    rows = c.fetchall()
    conn.close()
    return rows

def get_balance(account):
    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE debit_account=?", (account,))
    debit = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE credit_account=?", (account,))
    credit = c.fetchone()[0]
    conn.close()
    return debit - credit

# ========== قوالب HTML ==========
BASE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>نوح للمحاسبة الشاملة</title>
    <style>
        body { font-family: Tahoma; background: #111; color: #eee; padding: 20px; }
        a { color: #4a4aff; text-decoration: none; margin: 5px; }
        input, select, button { padding: 8px; margin: 5px; border-radius: 5px; border: 1px solid #555; background: #222; color: #eee; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #444; padding: 8px; text-align: center; }
        th { background: #333; }
        .nav { background: #222; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>🦅 نوح للمحاسبة الشاملة</h1>
    <div class="nav">
        <a href="/">🏠 الرئيسية</a>
        <a href="/accounts">📚 الحسابات</a>
        <a href="/transactions">✍️ القيود</a>
        <a href="/ledger">📒 دفتر الأستاذ</a>
        <a href="/trial_balance">⚖️ ميزان المراجعة</a>
        <a href="/income_statement">📈 قائمة الدخل</a>
        <a href="/balance_sheet">📊 الميزانية العمومية</a>
        <a href="/export">📥 تصدير CSV</a>
    </div>
    {% block content %}{% endblock %}
</body>
</html>
"""

# ========== الرئيسية ==========
@app.route('/')
def index():
    return render_template_string(BASE, content="""
        <h2>مرحباً بنوح</h2>
        <p>اختر من القائمة أعلاه.</p>
    """)

# ========== الحسابات ==========
@app.route('/accounts', methods=['GET', 'POST'])
def accounts():
    if request.method == 'POST':
        name = request.form['name'].strip()
        typ = request.form['type']
        if name:
            conn = sqlite3.connect('accounting.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO accounts (name, type) VALUES (?, ?)", (name, typ))
                conn.commit()
            except sqlite3.IntegrityError:
                pass
            conn.close()
        return redirect('/accounts')
    accs = get_accounts()
    content = """
        <h2>📚 إدارة الحسابات</h2>
        <form method="POST">
            <input type="text" name="name" placeholder="اسم الحساب" required>
            <select name="type">
                <option>أصول</option>
                <option>خصوم</option>
                <option>حقوق ملكية</option>
                <option>إيرادات</option>
                <option>مصاريف</option>
            </select>
            <button type="submit">➕ إضافة</button>
        </form>
        <table>
            <tr><th>الاسم</th><th>النوع</th></tr>
            {% for acc in accounts %}
            <tr><td>{{ acc[1] }}</td><td>{{ acc[2] }}</td></tr>
            {% endfor %}
        </table>
    """
    return render_template_string(BASE, content=content, accounts=accs)

# ========== القيود ==========
@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        date = request.form['date']
        desc = request.form['description']
        debit = request.form['debit']
        credit = request.form['credit']
        amount = float(request.form['amount'])
        conn = sqlite3.connect('accounting.db')
        c = conn.cursor()
        c.execute("INSERT INTO transactions (date, description, debit_account, credit_account, amount) VALUES (?,?,?,?,?)",
                  (date, desc, debit, credit, amount))
        conn.commit()
        conn.close()
        return redirect('/transactions')
    trans = get_transactions()
    acc_names = get_account_names()
    content = """
        <h2>✍️ إضافة قيد مزدوج</h2>
        <form method="POST">
            <input type="date" name="date" required>
            <input type="text" name="description" placeholder="البيان" required>
            <select name="debit" required>
                {% for n in acc_names %}<option>{{ n }}</option>{% endfor %}
            </select>
            <select name="credit" required>
                {% for n in acc_names %}<option>{{ n }}</option>{% endfor %}
            </select>
            <input type="number" step="0.01" name="amount" placeholder="المبلغ" required>
            <button type="submit">➕ إضافة قيد</button>
        </form>
        <h3>أحدث القيود</h3>
        <table>
            <tr><th>التاريخ</th><th>البيان</th><th>مدين</th><th>دائن</th><th>المبلغ</th></tr>
            {% for t in trans %}
            <tr><td>{{ t[0] }}</td><td>{{ t[1] }}</td><td>{{ t[2] }}</td><td>{{ t[3] }}</td><td>{{ t[4] }}</td></tr>
            {% endfor %}
        </table>
    """
    return render_template_string(BASE, content=content, acc_names=acc_names, trans=trans)

# ========== دفتر الأستاذ ==========
@app.route('/ledger')
def ledger():
    accs = get_accounts()
    ledger_data = []
    for acc in accs:
        name = acc[1]
        conn = sqlite3.connect('accounting.db')
        c = conn.cursor()
        c.execute("SELECT date, description, amount, 'مدين' FROM transactions WHERE debit_account=? ORDER BY date", (name,))
        debits = c.fetchall()
        c.execute("SELECT date, description, amount, 'دائن' FROM transactions WHERE credit_account=? ORDER BY date", (name,))
        credits = c.fetchall()
        conn.close()
        ledger_data.append((name, debits + credits, get_balance(name)))
    content = """
        <h2>📒 دفتر الأستاذ</h2>
        {% for name, moves, bal in ledger %}
        <h3>{{ name }} (الرصيد: {{ bal }})</h3>
        <table>
            <tr><th>التاريخ</th><th>البيان</th><th>المبلغ</th><th>النوع</th></tr>
            {% for m in moves %}
            <tr><td>{{ m[0] }}</td><td>{{ m[1] }}</td><td>{{ m[2] }}</td><td>{{ m[3] }}</td></tr>
            {% endfor %}
        </table>
        {% endfor %}
    """
    return render_template_string(BASE, content=content, ledger=ledger_data)

# ========== ميزان المراجعة ==========
@app.route('/trial_balance')
def trial_balance():
    accs = get_accounts()
    tb = []
    for acc in accs:
        name = acc[1]
        bal = get_balance(name)
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
    accs = get_accounts()
    revenues = sum(get_balance(a[1]) for a in accs if a[2] == 'إيرادات')
    expenses = sum(get_balance(a[1]) for a in accs if a[2] == 'مصاريف')
    net = revenues - expenses
    content = f"""
        <h2>📈 قائمة الدخل</h2>
        <table>
            <tr><th>الإيرادات</th><td>{revenues}</td></tr>
            <tr><th>المصاريف</th><td>{expenses}</td></tr>
            <tr><th>صافي الربح / الخسارة</th><td>{net}</td></tr>
        </table>
    """
    return render_template_string(BASE, content=content)

# ========== الميزانية العمومية ==========
@app.route('/balance_sheet')
def balance_sheet():
    accs = get_accounts()
    assets = sum(get_balance(a[1]) for a in accs if a[2] == 'أصول')
    liabilities = sum(get_balance(a[1]) for a in accs if a[2] == 'خصوم')
    equity = sum(get_balance(a[1]) for a in accs if a[2] == 'حقوق ملكية')
    content = f"""
        <h2>📊 الميزانية العمومية</h2>
        <table>
            <tr><th>الأصول</th><td>{assets}</td></tr>
            <tr><th>الخصوم</th><td>{liabilities}</td></tr>
            <tr><th>حقوق الملكية</th><td>{equity}</td></tr>
            <tr><th>التحقق (أصول = خصوم + حقوق)</th><td>{'✅ متوازن' if abs(assets - (liabilities + equity)) < 0.01 else '❌ غير متوازن'}</td></tr>
        </table>
    """
    return render_template_string(BASE, content=content)

# ========== تصدير CSV ==========
@app.route('/export')
def export_csv():
    trans = get_transactions()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['التاريخ', 'البيان', 'مدين', 'دائن', 'المبلغ'])
    for t in trans:
        writer.writerow(t)
    csv_data = output.getvalue()
    return f"<pre>{csv_data}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
