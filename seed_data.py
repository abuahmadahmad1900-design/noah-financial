import sqlite3

DB = 'core_finance.db'

def seed_all():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # حسابات
    c.execute("DELETE FROM accounts")
    accounts = [
        ('النقدية', 'أصول', 75000),
        ('البنك الأهلي', 'أصول', 250000),
        ('الاستثمارات', 'أصول', 180000),
        ('المبيعات', 'إيرادات', 450000),
        ('خدمات', 'إيرادات', 120000),
        ('المشتريات', 'مصاريف', 180000),
        ('رواتب', 'مصاريف', 95000),
        ('إيجار', 'مصاريف', 36000),
        ('قرض بنكي', 'خصوم', 150000),
        ('موردون', 'خصوم', 75000),
        ('رأس المال', 'حقوق ملكية', 300000),
    ]
    for name, type_acc, bal in accounts:
        c.execute("INSERT INTO accounts (name, type, balance) VALUES (?,?,?)", (name, type_acc, bal))
    
    # عملاء
    c.execute("DELETE FROM customers")
    customers = [
        ('شركة الأمل التجارية', '0501111111'),
        ('مؤسسة النور', '0502222222'),
        ('شركة المستقبل', '0503333333'),
        ('مجموعة البركة', '0504444444'),
        ('شركة الاتحاد', '0505555555'),
        ('مؤسسة الفجر', '0506666666'),
        ('شركة الريادة', '0507777777'),
        ('مؤسسة السلام', '0508888888'),
    ]
    for name, phone in customers:
        c.execute("INSERT INTO customers (name, phone) VALUES (?,?)", (name, phone))
    
    # منتجات
    c.execute("DELETE FROM products")
    products = [
        ('منتج أ', 150, 80),
        ('منتج ب', 250, 45),
        ('منتج ج', 350, 30),
        ('منتج د', 450, 20),
        ('منتج هـ', 550, 15),
        ('منتج و', 650, 10),
    ]
    for name, price, stock in products:
        c.execute("INSERT INTO products (name, price, stock) VALUES (?,?,?)", (name, price, stock))
    
    # فواتير
    c.execute("DELETE FROM invoices")
    invoices = [
        (1, 15000, '2026-08-01'),
        (2, 25000, '2026-08-03'),
        (3, 10000, '2026-08-05'),
        (4, 30000, '2026-08-07'),
        (5, 20000, '2026-08-09'),
        (6, 35000, '2026-08-11'),
        (7, 28000, '2026-08-13'),
        (8, 22000, '2026-08-15'),
    ]
    for cust_id, amount, date in invoices:
        c.execute("INSERT INTO invoices (customer_id, amount, date) VALUES (?,?,?)", (cust_id, amount, date))
    
    # حركات بنكية
    c.execute("DELETE FROM bank_moves")
    bank_moves = [
        ('2026-08-01', 'إيداع تأسيسي', 300000),
        ('2026-08-02', 'مبيعات', 45000),
        ('2026-08-03', 'سحب مصاريف', -25000),
        ('2026-08-04', 'إيداع', 35000),
        ('2026-08-05', 'دفع موردين', -40000),
        ('2026-08-06', 'مبيعات', 55000),
        ('2026-08-07', 'رواتب', -30000),
        ('2026-08-08', 'إيجار', -12000),
        ('2026-08-09', 'مبيعات', 48000),
        ('2026-08-10', 'سداد قرض', -20000),
        ('2026-08-11', 'إيداع', 38000),
        ('2026-08-12', 'مصاريف تشغيل', -15000),
        ('2026-08-13', 'مبيعات', 52000),
        ('2026-08-14', 'سحب', -18000),
        ('2026-08-15', 'إيداع', 42000),
    ]
    for date, desc, amount in bank_moves:
        c.execute("INSERT INTO bank_moves (date, desc, amount) VALUES (?,?,?)", (date, desc, amount))
    
    conn.commit()
    conn.close()
    print("✅ تمت إضافة البيانات الشاملة")

if __name__ == '__main__':
    seed_all()
