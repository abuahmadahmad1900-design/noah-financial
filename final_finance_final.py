from flask import Flask, request, session, redirect, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'final_finance_2026'
DB = 'new_finance.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
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
    """)
    conn.commit()
    conn.close()

def seed_finance_data():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM accounts")
    if c.fetchone()[0] == 0:
        for name, type_acc, bal in [('النقدية','أصول',50000),('البنك','أصول',150000),('المبيعات','إيرادات',200000),('المشتريات','مصاريف',80000)]:
            c.execute("INSERT INTO accounts (name, type, balance) VALUES (?,?,?)", (name, type_acc, bal))
        for name, phone in [('شركة الأمل','0501234567'),('مؤسسة النور','0507654321'),('شركة المستقبل','0509876543')]:
            c.execute("INSERT INTO customers (name, phone) VALUES (?,?)", (name, phone))
        for name, price, stock in [('منتج أ',100,50),('منتج ب',200,30),('منتج ج',300,20)]:
            c.execute("INSERT INTO products (name, price, stock) VALUES (?,?,?)", (name, price, stock))
        for cust_id, amount, date in [(1,15000,'2026-08-01'),(2,25000,'2026-08-05'),(3,10000,'2026-08-10')]:
            c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (?,?,?)", (cust_id, amount, date))
        for date, desc, amount in [('2026-08-01','إيداع',50000),('2026-08-05','مبيعات',35000),('2026-08-10','سحب',-15000)]:
            c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES (?,?,?)", (date, desc, amount))
        conn.commit()
    conn.close()

def seed_finance_data():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM accounts")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO accounts (name, type, balance) VALUES ('النقدية','أصول',50000)")
        c.execute("INSERT INTO accounts (name, type, balance) VALUES ('البنك','أصول',150000)")
        c.execute("INSERT INTO accounts (name, type, balance) VALUES ('المبيعات','إيرادات',200000)")
        c.execute("INSERT INTO accounts (name, type, balance) VALUES ('المشتريات','مصاريف',80000)")
        c.execute("INSERT INTO customers (name, phone) VALUES ('شركة الأمل','0501234567')")
        c.execute("INSERT INTO customers (name, phone) VALUES ('مؤسسة النور','0507654321')")
        c.execute("INSERT INTO customers (name, phone) VALUES ('شركة المستقبل','0509876543')")
        c.execute("INSERT INTO products (name, price, stock) VALUES ('منتج أ',100,50)")
        c.execute("INSERT INTO products (name, price, stock) VALUES ('منتج ب',200,30)")
        c.execute("INSERT INTO products (name, price, stock) VALUES ('منتج ج',300,20)")
        c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (1,15000,'2026-08-01')")
        c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (2,25000,'2026-08-05')")
        c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (3,10000,'2026-08-10')")
        c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES ('2026-08-01','إيداع',50000)")
        c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES ('2026-08-05','إيداع مبيعات',35000)")
        c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES ('2026-08-10','سحب',-15000)")
        conn.commit()
    conn.close()

