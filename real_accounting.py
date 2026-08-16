#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# إنشاء قاعدة البيانات
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
    conn.commit()
    conn.close()

init_db()

# واجهة المستخدم
PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نوح للمحاسبة الحقيقية</title>
    <style>
        body { font-family: Tahoma; background: #111; color: #eee; padding: 30px; }
        input, select, button { padding: 10px; margin: 5px; border-radius: 5px; border: 1px solid #555; background: #222; color: #eee; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #444; padding: 8px; text-align: center; }
        th { background: #333; }
    </style>
</head>
<body>
    <h1>🦅 نوح للمحاسبة الحقيقية</h1>
    <form action="/add_transaction" method="POST">
        <input type="date" name="date" required>
        <input type="text" name="description" placeholder="البيان" required>
        <input type="text" name="debit_account" placeholder="الحساب المدين" required>
        <input type="text" name="credit_account" placeholder="الحساب الدائن" required>
        <input type="number" step="0.01" name="amount" placeholder="المبلغ" required>
        <button type="submit">إضافة قيد</button>
    </form>
    <h2>ميزان المراجعة</h2>
    <table>
        <tr><th>الحساب</th><th>الرصيد</th></tr>
        {% for row in trial_balance %}
        <tr><td>{{ row[0] }}</td><td>{{ row[1] }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    c.execute("SELECT debit_account, SUM(amount) FROM transactions GROUP BY debit_account")
    debits = dict(c.fetchall())
    c.execute("SELECT credit_account, SUM(amount) FROM transactions GROUP BY credit_account")
    credits = dict(c.fetchall())
    accounts = set(debits.keys()) | set(credits.keys())
    trial_balance = []
    for acc in accounts:
        balance = debits.get(acc, 0) - credits.get(acc, 0)
        trial_balance.append((acc, balance))
    conn.close()
    return render_template_string(PAGE, trial_balance=trial_balance)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    date = request.form['date']
    description = request.form['description']
    debit = request.form['debit_account']
    credit = request.form['credit_account']
    amount = float(request.form['amount'])
    conn = sqlite3.connect('accounting.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (date, description, debit_account, credit_account, amount) VALUES (?,?,?,?,?)",
              (date, description, debit, credit, amount))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "تم إضافة القيد"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
