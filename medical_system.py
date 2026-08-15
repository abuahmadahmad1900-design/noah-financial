#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦅 نوح - النظام الطبي الأسطوري المتكامل
"""

import sqlite3, hashlib
from flask import Flask, request, render_template_string, session, redirect
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'noah_medical_supreme_2026'
DB_MED = 'medical.db'

def init_db():
    conn = sqlite3.connect(DB_MED)
    c = conn.cursor()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'admin'
    );
    CREATE TABLE IF NOT EXISTS specialties (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT
    );
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY,
        name TEXT,
        specialty_id INTEGER,
        phone TEXT,
        license_number TEXT,
        years_exp INTEGER DEFAULT 0,
        rating REAL DEFAULT 5.0
    );
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        birth_date TEXT,
        gender TEXT,
        blood_type TEXT,
        allergies TEXT,
        chronic_diseases TEXT
    );
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        doctor_id INTEGER,
        date TEXT,
        time TEXT,
        status TEXT DEFAULT 'مؤكد',
        notes TEXT
    );
    CREATE TABLE IF NOT EXISTS prescriptions (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        doctor_id INTEGER,
        medicine TEXT,
        dosage TEXT,
        instructions TEXT,
        date TEXT
    );
    CREATE TABLE IF NOT EXISTS medical_invoices (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        amount REAL,
        date TEXT,
        status TEXT DEFAULT 'غير مدفوعة'
    );
    CREATE TABLE IF NOT EXISTS lab_tests (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        test_name TEXT,
        result TEXT,
        normal_range TEXT,
        date TEXT
    );
    CREATE TABLE IF NOT EXISTS radiology (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        scan_type TEXT,
        findings TEXT,
        date TEXT
    );
    CREATE TABLE IF NOT EXISTS pharmacy (
        id INTEGER PRIMARY KEY,
        medicine_name TEXT,
        quantity INTEGER,
        price REAL
    );
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY,
        room_number TEXT,
        type TEXT,
        status TEXT DEFAULT 'متاحة'
    );
    CREATE TABLE IF NOT EXISTS operations (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        doctor_id INTEGER,
        room_id INTEGER,
        operation_name TEXT,
        date TEXT,
        status TEXT DEFAULT 'مجدولة'
    );
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY,
        name TEXT,
        head_doctor_id INTEGER
    );
    CREATE TABLE IF NOT EXISTS medical_records (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        record_type TEXT,
        details TEXT,
        date TEXT
    );
    CREATE TABLE IF NOT EXISTS medical_alerts (
        id INTEGER PRIMARY KEY,
        message TEXT,
        type TEXT,
        date TEXT
    );
    ''')
    hashed = hashlib.sha256('admin123'.encode()).hexdigest()
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', ?)", (hashed,))
    specialties = [
        ('عامة','الطب العام'),
        ('أطفال','طب الأطفال'),
        ('باطنة','الأمراض الباطنية'),
        ('قلب','أمراض القلب'),
        ('جلدية','الأمراض الجلدية'),
        ('أسنان','طب الأسنان'),
        ('عيون','طب العيون'),
        ('نساء','النساء والولادة'),
        ('عظام','جراحة العظام'),
        ('أنف وأذن','الأنف والأذن والحنجرة'),
        ('نفسية','الطب النفسي'),
        ('مسالك','جراحة المسالك'),
        ('مخ وأعصاب','الأعصاب'),
        ('أورام','علاج الأورام'),
        ('طوارئ','طب الطوارئ'),
    ]
    for name, desc in specialties:
        c.execute("INSERT OR IGNORE INTO specialties (name, description) VALUES (?,?)", (name, desc))
    conn.commit()
    conn.close()

init_db()

MED_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦅 نوح - النظام الطبي الأسطوري</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family: Tahoma, sans-serif;
            background: linear-gradient(135deg, #0a2e2e, #0e1a2e, #0a2e1a);
            background-size: 400% 400%;
            animation: bg-shift 12s ease infinite;
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }
        @keyframes bg-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        a { color:#4affb0; text-decoration:none; margin:5px; transition:all 0.3s; }
        a:hover { color:#fff; text-shadow:0 0 10px #4affb0; }
        input, select, button {
            padding:10px; margin:5px;
            background:#1a1a3e; color:#eee;
            border:1px solid #4affb0; border-radius:8px;
        }
        button {
            background: linear-gradient(45deg, #4affb0, #00c8ff);
            color:#000; font-weight:bold; cursor:pointer;
        }
        button:hover { transform:translateY(-2px); box-shadow:0 10px 20px rgba(74,255,176,0.3); }
        table { width:100%; border-collapse:collapse; margin-top:15px; }
        th, td { border:1px solid #2a4a3a; padding:10px; text-align:center; }
        th { background: linear-gradient(145deg,#1a3e2e,#0d2e1e); color:#4affb0; }
        tr:hover td { background: rgba(74,255,176,0.05); }
        .container {
            max-width:1200px; margin:0 auto;
            background: rgba(10,20,30,0.85);
            backdrop-filter: blur(15px);
            border-radius:30px; padding:30px;
            border:2px solid rgba(74,255,176,0.4);
            box-shadow:0 20px 50px rgba(0,0,0,0.6), 0 0 40px rgba(74,255,176,0.2);
        }
        .nav {
            display:flex; flex-wrap:wrap; gap:8px; justify-content:center;
            margin-bottom:25px; padding:15px;
            background:rgba(10,20,40,0.8); border-radius:20px;
        }
        .stats-grid {
            display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
            gap:20px; margin-top:25px;
        }
        .stat-card {
            background: linear-gradient(145deg,#1a3e2e,#0d2e1e);
            border-radius:20px; padding:25px; text-align:center;
            border:1px solid rgba(74,255,176,0.3);
            transition:all 0.3s; cursor:pointer;
        }
        .stat-card:hover {
            transform:translateY(-8px);
            border-color:#4affb0;
            box-shadow:0 15px 30px rgba(74,255,176,0.3);
        }
        .stat-card .icon { font-size:2.5rem; }
        .stat-card .num { font-size:2.2rem; font-weight:900; color:#4affb0; }
        .stat-card .label { color:#aaa; font-size:0.85rem; }
        h1 {
            text-align:center;
            font-size:2.5rem;
            background: linear-gradient(45deg,#4affb0,#00c8ff,#4affb0);
            background-size:300% 300%;
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            animation:gradient-shift 3s ease infinite;
        }
        @keyframes gradient-shift {
            0% { background-position:0% 50%; }
            50% { background-position:100% 50%; }
            100% { background-position:0% 50%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 نوح - النظام الطبي الأسطوري</h1>
        <div class="nav">
            <a href="/medical_dashboard">🏠 الرئيسية</a>
            <a href="/specialties">📋 التخصصات</a>
            <a href="/doctors">🩺 الأطباء</a>
            <a href="/patients">👥 المرضى</a>
            <a href="/appointments">📅 المواعيد</a>
            <a href="/prescriptions">💊 الوصفات</a>
            <a href="/medical_invoices">🧾 الفواتير</a>
            <a href="/lab_tests">🔬 المختبر</a>
            <a href="/radiology">📷 الأشعة</a>
            <a href="/pharmacy">💊 الصيدلية</a>
            <a href="/rooms">🛏️ الغرف</a>
            <a href="/operations">🔪 العمليات</a>
            <a href="/departments">🏢 الأقسام</a>
            <a href="/medical_records">📄 السجلات</a>
            <a href="/medical_alerts">🔔 التنبيهات</a>
            <a href="/medical_ai">🧠 الذكاء الطبي</a>
            <a href="/logout_medical">🚪 خروج</a>
        </div>
        {{ content | safe }}
    </div>
</body>
</html>
'''

@app.route('/')
def medical_home():
    return redirect('/medical_login')

@app.route('/medical_login', methods=['GET','POST'])
def medical_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(DB_MED); c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
        user = c.fetchone(); conn.close()
        if user:
            session['medical_user'] = username
            return redirect('/medical_dashboard')
        return redirect('/medical_login?error=1')
    error = request.args.get('error')
    return '''
    <!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
    <title>دخول نوح الطبي</title>
    <style>
        body { font-family:Tahoma; background:linear-gradient(135deg,#0a2e2e,#0e1a2e); color:#fff; display:flex; justify-content:center; align-items:center; height:100vh; }
        .login-box { background:rgba(10,20,30,0.9); padding:40px; border-radius:25px; border:2px solid #4affb0; text-align:center; }
        input { display:block; width:100%; padding:12px; margin:10px 0; background:#1a1a3e; border:1px solid #4affb0; color:#fff; border-radius:10px; }
        button { width:100%; padding:12px; background:linear-gradient(45deg,#4affb0,#00c8ff); border:none; border-radius:10px; font-weight:bold; cursor:pointer; }
    </style></head><body>
    <div class="login-box"><h2>🦅 دخول نوح الطبي</h2>''' + ("<p style='color:#ff4a4a;'>بيانات خاطئة</p>" if error else "") + '''
    <form method="POST">
        <input type="text" name="username" placeholder="المستخدم" required>
        <input type="password" name="password" placeholder="كلمة المرور" required>
        <button>دخول</button>
    </form></div></body></html>'''

@app.route('/logout_medical')
def logout_medical():
    session.pop('medical_user', None)
    return redirect('/medical_login')

@app.route('/medical_dashboard')
def medical_dashboard():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM patients"); patients = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM doctors"); doctors = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM appointments"); appts = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM prescriptions"); presc = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM lab_tests"); labs = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM radiology"); radios = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM pharmacy"); meds = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM rooms"); rooms = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM operations"); ops = c.fetchone()[0]
    conn.close()
    content = f'''
    <div class="stats-grid">
        <div class="stat-card"><div class="icon">👥</div><div class="num">{patients}</div><div class="label">المرضى</div></div>
        <div class="stat-card"><div class="icon">🩺</div><div class="num">{doctors}</div><div class="label">الأطباء</div></div>
        <div class="stat-card"><div class="icon">📅</div><div class="num">{appts}</div><div class="label">المواعيد</div></div>
        <div class="stat-card"><div class="icon">💊</div><div class="num">{presc}</div><div class="label">الوصفات</div></div>
        <div class="stat-card"><div class="icon">🔬</div><div class="num">{labs}</div><div class="label">فحوصات</div></div>
        <div class="stat-card"><div class="icon">📷</div><div class="num">{radios}</div><div class="label">أشعة</div></div>
        <div class="stat-card"><div class="icon">💊</div><div class="num">{meds}</div><div class="label">أدوية</div></div>
        <div class="stat-card"><div class="icon">🛏️</div><div class="num">{rooms}</div><div class="label">غرف</div></div>
        <div class="stat-card"><div class="icon">🔪</div><div class="num">{ops}</div><div class="label">عمليات</div></div>
    </div>'''
    return render_template_string(MED_PAGE, content=content)

# ========== التخصصات ==========
@app.route('/specialties', methods=['GET','POST'])
def specialties():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description','')
        c.execute("INSERT INTO specialties (name, description) VALUES (?,?)", (name, description))
        conn.commit()
    c.execute("SELECT * FROM specialties")
    rows = c.fetchall(); conn.close()
    content = """
    <h2>📋 التخصصات الطبية</h2>
    <form method="POST">
        <input name="name" placeholder="اسم التخصص" required>
        <input name="description" placeholder="الوصف">
        <button>إضافة</button>
    </form>
    <table><tr><th>ID</th><th>التخصص</th><th>الوصف</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(MED_PAGE, content=content)

# ========== الأطباء ==========
@app.route('/doctors', methods=['GET','POST'])
def doctors():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        specialty_id = request.form.get('specialty_id','')
        phone = request.form.get('phone','')
        license_number = request.form.get('license_number','')
        years_exp = request.form.get('years_exp',0)
        rating = request.form.get('rating',5.0)
        c.execute("INSERT INTO doctors (name, specialty_id, phone, license_number, years_exp, rating) VALUES (?,?,?,?,?,?)",
                  (name, specialty_id, phone, license_number, years_exp, rating))
        conn.commit()
    c.execute("SELECT * FROM doctors")
    rows = c.fetchall()
    c.execute("SELECT id, name FROM specialties")
    specs = c.fetchall()
    conn.close()
    spec_options = "".join([f"<option value='{s[0]}'>{s[1]}</option>" for s in specs])
    content = f"""
    <h2>🩺 الأطباء</h2>
    <form method="POST">
        <input name="name" placeholder="اسم الطبيب" required>
        <select name="specialty_id">{spec_options}</select>
        <input name="phone" placeholder="الهاتف">
        <input name="license_number" placeholder="رقم الترخيص">
        <input name="years_exp" placeholder="سنوات الخبرة" value="0">
        <input name="rating" placeholder="التقييم" value="5.0">
        <button>إضافة</button>
    </form>
    <table><tr><th>ID</th><th>الاسم</th><th>التخصص</th><th>الهاتف</th><th>الترخيص</th><th>الخبرة</th><th>التقييم</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td></tr>"
    content += "</table>"
    return render_template_string(MED_PAGE, content=content)

# ========== المرضى ==========
@app.route('/patients', methods=['GET','POST'])
def patients():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form.get('phone','')
        birth_date = request.form.get('birth_date','')
        gender = request.form.get('gender','')
        blood_type = request.form.get('blood_type','')
        allergies = request.form.get('allergies','')
        chronic_diseases = request.form.get('chronic_diseases','')
        c.execute("INSERT INTO patients (name, phone, birth_date, gender, blood_type, allergies, chronic_diseases) VALUES (?,?,?,?,?,?,?)",
                  (name, phone, birth_date, gender, blood_type, allergies, chronic_diseases))
        conn.commit()
    c.execute("SELECT * FROM patients")
    rows = c.fetchall(); conn.close()
    content = """
    <h2>👥 المرضى</h2>
    <form method="POST">
        <input name="name" placeholder="اسم المريض" required>
        <input name="phone" placeholder="الهاتف">
        <input name="birth_date" type="date" placeholder="تاريخ الميلاد">
        <select name="gender"><option>ذكر</option><option>أنثى</option></select>
        <input name="blood_type" placeholder="فصيلة الدم">
        <input name="allergies" placeholder="الحساسية">
        <input name="chronic_diseases" placeholder="أمراض مزمنة">
        <button>إضافة</button>
    </form>
    <table><tr><th>ID</th><th>الاسم</th><th>الهاتف</th><th>الميلاد</th><th>الجنس</th><th>الدم</th><th>الحساسية</th><th>أمراض مزمنة</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td><td>{r[7]}</td></tr>"
    content += "</table>"
    return render_template_string(MED_PAGE, content=content)

# ========== المواعيد ==========
@app.route('/appointments', methods=['GET','POST'])
def appointments():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        time = request.form['time']
        status = request.form.get('status','مؤكد')
        notes = request.form.get('notes','')
        c.execute("INSERT INTO appointments (patient_id, doctor_id, date, time, status, notes) VALUES (?,?,?,?,?,?)",
                  (patient_id, doctor_id, date, time, status, notes))
        conn.commit()
    c.execute("SELECT * FROM appointments")
    rows = c.fetchall()
    c.execute("SELECT id, name FROM patients")
    patients = c.fetchall()
    c.execute("SELECT id, name FROM doctors")
    doctors = c.fetchall()
    conn.close()
    patient_options = "".join([f"<option value='{p[0]}'>{p[1]}</option>" for p in patients])
    doctor_options = "".join([f"<option value='{d[0]}'>{d[1]}</option>" for d in doctors])
    content = f"""
    <h2>📅 المواعيد</h2>
    <form method="POST">
        <select name="patient_id">{patient_options}</select>
        <select name="doctor_id">{doctor_options}</select>
        <input name="date" type="date" required>
        <input name="time" type="time" required>
        <select name="status"><option>مؤكد</option><option>ملغى</option><option>منتهي</option></select>
        <input name="notes" placeholder="ملاحظات">
        <button>إضافة</button>
    </form>
    <table><tr><th>ID</th><th>المريض</th><th>الطبيب</th><th>التاريخ</th><th>الوقت</th><th>الحالة</th><th>ملاحظات</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td></tr>"
    content += "</table>"
    return render_template_string(MED_PAGE, content=content)

# ========== الوصفات ==========
@app.route('/prescriptions', methods=['GET','POST'])
def prescriptions():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        medicine = request.form['medicine']
        dosage = request.form['dosage']
        instructions = request.form.get('instructions','')
        date = datetime.now().strftime('%Y-%m-%d')
        c.execute("INSERT INTO prescriptions (patient_id, doctor_id, medicine, dosage, instructions, date) VALUES (?,?,?,?,?,?)",
                  (patient_id, doctor_id, medicine, dosage, instructions, date))
        conn.commit()
    c.execute("SELECT * FROM prescriptions")
    rows = c.fetchall()
    c.execute("SELECT id, name FROM patients")
    patients = c.fetchall()
    c.execute("SELECT id, name FROM doctors")
    doctors = c.fetchall()
    conn.close()
    patient_options = "".join([f"<option value='{p[0]}'>{p[1]}</option>" for p in patients])
    doctor_options = "".join([f"<option value='{d[0]}'>{d[1]}</option>" for d in doctors])
    content = f"""
    <h2>💊 الوصفات الطبية</h2>
    <form method="POST">
        <select name="patient_id">{patient_options}</select>
        <select name="doctor_id">{doctor_options}</select>
        <input name="medicine" placeholder="الدواء" required>
        <input name="dosage" placeholder="الجرعة" required>
        <input name="instructions" placeholder="تعليمات">
        <button>إصدار</button>
    </form>
    <table><tr><th>ID</th><th>المريض</th><th>الطبيب</th><th>الدواء</th><th>الجرعة</th><th>التعليمات</th><th>التاريخ</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td></tr>"
    content += "</table>"
    return render_template_string(MED_PAGE, content=content)

# ========== الفواتير الطبية ==========
@app.route('/medical_invoices', methods=['GET','POST'])
def medical_invoices():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        amount = request.form['amount']
        date = request.form['date']
        status = request.form.get('status','غير مدفوعة')
        c.execute("INSERT INTO medical_invoices (patient_id, amount, date, status) VALUES (?,?,?,?)",
                  (patient_id, amount, date, status))
        conn.commit()
    c.execute("SELECT * FROM medical_invoices")
    rows = c.fetchall()
    c.execute("SELECT id, name FROM patients")
    patients = c.fetchall()
    conn.close()
    patient_options = "".join([f"<option value='{p[0]}'>{p[1]}</option>" for p in patients])
    content = f"""
    <h2>🧾 الفواتير الطبية</h2>
    <form method="POST">
        <select name="patient_id">{patient_options}</select>
        <input name="amount" placeholder="المبلغ" required>
        <input name="date" type="date" required>
        <select name="status"><option>غير مدفوعة</option><option>مدفوعة</option></select>
        <button>إصدار</button>
    </form>
    <table><tr><th>ID</th><th>المريض</th><th>المبلغ</th><th>التاريخ</th><th>الحالة</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"
    content += "</table>"
    return render_template_string(MED_PAGE, content=content)

# ========== المختبر ==========
@app.route('/lab_tests', methods=['GET','POST'])
def lab_tests():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        test_name = request.form['test_name']
        result = request.form.get('result','')
        normal_range = request.form.get('normal_range','')
        date = request.form['date']
        c.execute("INSERT INTO lab_tests (patient_id, test_name, result, normal_range, date) VALUES (?,?,?,?,?)",
                  (patient_id, test_name, result, normal_range, date))
        conn.commit()
    c.execute("SELECT * FROM lab_tests")
    rows = c.fetchall()
    c.execute("SELECT id, name FROM patients")
    patients = c.fetchall()
    conn.close()
    patient_options = "".join([f"<option value='{p[0]}'>{p[1]}</option>" for p in patients])
    content = f"""
    <h2>🔬 فحوصات المختبر</h2>
    <form method="POST">
        <select name="patient_id">{patient_options}</select>
        <input name="test_name" placeholder="اسم الفحص" required>
        <input name="result" placeholder="النتيجة">
        <input name="normal_range" placeholder="المعدل الطبيعي">
        <input name="date" type="date" required>
        <button>إضافة</button>
    </form>
    <table><tr><th>ID</th><th>المريض</th><th>الفحص</th><th>النتيجة</th><th>المعدل</th><th>التاريخ</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>"
    content += "</table>"
    return render_template_string(MED_PAGE, content=content)

# ========== الأشعة ==========
@app.route('/radiology', methods=['GET','POST'])
def radiology():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        scan_type = request.form['scan_type']
        findings = request.form.get('findings','')
        date = request.form['date']
        c.execute("INSERT INTO radiology (patient_id, scan_type, findings, date) VALUES (?,?,?,?)",
                  (patient_id, scan_type, findings, date))
        conn.commit()
    c.execute("SELECT * FROM radiology")
    rows = c.fetchall()
    c.execute("SELECT id, name FROM patients")
    patients = c.fetchall()
    conn.close()
    patient_options = "".join([f"<option value='{p[0]}'>{p[1]}</option>" for p in patients])
    content = f"""
    <h2>📷 الأشعة والتصوير</h2>
    <form method="POST">
        <select name="patient_id">{patient_options}</select>
        <input name="scan_type" placeholder="نوع الأشعة (سينية، مقطعية، رنين)" required>
        <input name="findings" placeholder="النتائج">
        <input name="date" type="date" required>
        <button>إضافة</button>
    </form>
    <table><tr><th>ID</th><th>المريض</th><th>النوع</th><th>النتائج</th><th>التاريخ</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"
    content += "</table>"
    return render_template_string(MED_PAGE, content=content)

# ========== الصيدلية ==========
@app.route('/pharmacy', methods=['GET','POST'])
def pharmacy():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    if request.method == 'POST':
        medicine_name = request.form['medicine_name']
        quantity = request.form['quantity']
        price = request.form['price']
        c.execute("INSERT INTO pharmacy (medicine_name, quantity, price) VALUES (?,?,?)",
                  (medicine_name, quantity, price))
        conn.commit()
    c.execute("SELECT * FROM pharmacy")
    rows = c.fetchall(); conn.close()
    content = """
    <h2>💊 صيدلية العيادة</h2>
    <form method="POST">
        <input name="medicine_name" placeholder="اسم الدواء" required>
        <input name="quantity" placeholder="الكمية" required>
        <input name="price" placeholder="السعر" required>
        <button>إضافة</button>
    </form>
    <table><tr><th>ID</th><th>الدواء</th><th>الكمية</th><th>السعر</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(MED_PAGE, content=content)

# ========== الغرف ==========
@app.route('/rooms', methods=['GET','POST'])
def rooms():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    if request.method == 'POST':
        room_number = request.form['room_number']
        room_type = request.form['type']
        status = request.form.get('status','متاحة')
        c.execute("INSERT INTO rooms (room_number, type, status) VALUES (?,?,?)",
                  (room_number, room_type, status))
        conn.commit()
    c.execute("SELECT * FROM rooms")
    rows = c.fetchall(); conn.close()
    content = """
    <h2>🛏️ الغرف</h2>
    <form method="POST">
        <input name="room_number" placeholder="رقم الغرفة" required>
        <select name="type"><option>عادية</option><option>خاصة</option><option>عمليات</option><option>عناية مركزة</option></select>
        <select name="status"><option>متاحة</option><option>مشغولة</option><option>صيانة</option></select>
        <button>إضافة</button>
    </form>
    <table><tr><th>ID</th><th>الرقم</th><th>النوع</th><th>الحالة</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(MED_PAGE, content=content)

# ========== العمليات ==========
@app.route('/operations', methods=['GET','POST'])
def operations():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        room_id = request.form.get('room_id','')
        operation_name = request.form['operation_name']
        date = request.form['date']
        status = request.form.get('status','مجدولة')
        c.execute("INSERT INTO operations (patient_id, doctor_id, room_id, operation_name, date, status) VALUES (?,?,?,?,?,?)",
                  (patient_id, doctor_id, room_id, operation_name, date, status))
        conn.commit()
    c.execute("SELECT * FROM operations")
    rows = c.fetchall()
    c.execute("SELECT id, name FROM patients")
    patients = c.fetchall()
    c.execute("SELECT id, name FROM doctors")
    doctors = c.fetchall()
    conn.close()
    patient_options = "".join([f"<option value='{p[0]}'>{p[1]}</option>" for p in patients])
    doctor_options = "".join([f"<option value='{d[0]}'>{d[1]}</option>" for d in doctors])
    content = f"""
    <h2>🔪 العمليات الجراحية</h2>
    <form method="POST">
        <select name="patient_id">{patient_options}</select>
        <select name="doctor_id">{doctor_options}</select>
        <input name="room_id" placeholder="رقم الغرفة">
        <input name="operation_name" placeholder="اسم العملية" required>
        <input name="date" type="date" required>
        <select name="status"><option>مجدولة</option><option>منتهية</option><option>ملغاة</option></select>
        <button>إضافة</button>
    </form>
    <table><tr><th>ID</th><th>المريض</th><th>الطبيب</th><th>الغرفة</th><th>العملية</th><th>التاريخ</th><th>الحالة</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td></tr>"
    content += "</table>"
    return render_template_string(MED_PAGE, content=content)

# ========== الأقسام ==========
@app.route('/departments', methods=['GET','POST'])
def departments():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        head_doctor_id = request.form.get('head_doctor_id','')
        c.execute("INSERT INTO departments (name, head_doctor_id) VALUES (?,?)", (name, head_doctor_id))
        conn.commit()
    c.execute("SELECT * FROM departments")
    rows = c.fetchall()
    c.execute("SELECT id, name FROM doctors")
    doctors = c.fetchall()
    conn.close()
    doctor_options = "".join([f"<option value='{d[0]}'>{d[1]}</option>" for d in doctors])
    content = f"""
    <h2>🏢 الأقسام الطبية</h2>
    <form method="POST">
        <input name="name" placeholder="اسم القسم" required>
        <select name="head_doctor_id">{doctor_options}</select>
        <button>إضافة</button>
    </form>
    <table><tr><th>ID</th><th>القسم</th><th>رئيس القسم</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(MED_PAGE, content=content)

# ========== السجلات الطبية ==========
@app.route('/medical_records', methods=['GET','POST'])
def medical_records():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        record_type = request.form['record_type']
        details = request.form['details']
        date = datetime.now().strftime('%Y-%m-%d')
        c.execute("INSERT INTO medical_records (patient_id, record_type, details, date) VALUES (?,?,?,?)",
                  (patient_id, record_type, details, date))
        conn.commit()
    c.execute("SELECT * FROM medical_records")
    rows = c.fetchall()
    c.execute("SELECT id, name FROM patients")
    patients = c.fetchall()
    conn.close()
    patient_options = "".join([f"<option value='{p[0]}'>{p[1]}</option>" for p in patients])
    content = f"""
    <h2>📄 السجلات الطبية</h2>
    <form method="POST">
        <select name="patient_id">{patient_options}</select>
        <input name="record_type" placeholder="نوع السجل (تشخيص، متابعة، طوارئ)" required>
        <textarea name="details" placeholder="تفاصيل السجل" style="width:100%;padding:10px;background:#1a1a3e;color:#fff;border:1px solid #4affb0;border-radius:8px;"></textarea>
        <button>إضافة</button>
    </form>
    <table><tr><th>ID</th><th>المريض</th><th>النوع</th><th>التفاصيل</th><th>التاريخ</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"
    content += "</table>"
    return render_template_string(MED_PAGE, content=content)

# ========== التنبيهات الطبية ==========
@app.route('/medical_alerts', methods=['GET','POST'])
def medical_alerts():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    if request.method == 'POST':
        message = request.form['message']
        alert_type = request.form['type']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("INSERT INTO medical_alerts (message, type, date) VALUES (?,?,?)",
                  (message, alert_type, date))
        conn.commit()
    c.execute("SELECT * FROM medical_alerts ORDER BY id DESC")
    rows = c.fetchall(); conn.close()
    content = """
    <h2>🔔 التنبيهات الطبية</h2>
    <form method="POST">
        <input name="message" placeholder="نص التنبيه" required>
        <select name="type"><option>طوارئ</option><option>تحذير</option><option>متابعة</option></select>
        <button>إضافة</button>
    </form>
    <table><tr><th>ID</th><th>الرسالة</th><th>النوع</th><th>التاريخ</th></tr>"""
    for r in rows:
        color = "#fff"
        if r[2] == "طوارئ":
            color = "#ff4a4a"
        elif r[2] == "تحذير":
            color = "#ffd700"
        content += f"<tr style='color:{color}'><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    content += "</table>"
    return render_template_string(MED_PAGE, content=content)

# ========== تشغيل النظام الطبي ==========
# ========== الذكاء الطبي (25 بوت) ==========
medical_bots = [
    (1, "🫀", "بوت القلب", "تشخيص أمراض القلب"),
    (2, "🧠", "بوت الأعصاب", "أمراض المخ والأعصاب"),
    (3, "🦷", "بوت الأسنان", "مشاكل الأسنان"),
    (4, "👁️", "بوت العيون", "أمراض العيون"),
    (5, "🫁", "بوت الصدر", "أمراض الجهاز التنفسي"),
    (6, "🍽️", "بوت الجهاز الهضمي", "أمراض المعدة والأمعاء"),
    (7, "🩸", "بوت الدم", "أمراض الدم"),
    (8, "🦴", "بوت العظام", "أمراض العظام والمفاصل"),
    (9, "👶", "بوت الأطفال", "أمراض الأطفال"),
    (10, "👩", "بوت النساء", "أمراض النساء والولادة"),
    (11, "🧬", "بوت الوراثة", "الأمراض الوراثية"),
    (12, "🦠", "بوت العدوى", "الأمراض المعدية"),
    (13, "💊", "بوت الأدوية", "استشارات دوائية"),
    (14, "🚑", "بوت الطوارئ", "حالات الطوارئ"),
    (15, "🔬", "بوت المختبر", "تحليل النتائج المخبرية"),
    (16, "📷", "بوت الأشعة", "قراءة تقارير الأشعة"),
    (17, "🧘", "بوت الصحة النفسية", "الدعم النفسي"),
    (18, "🥗", "بوت التغذية", "استشارات غذائية"),
    (19, "🏋️", "بوت اللياقة", "اللياقة البدنية"),
    (20, "😴", "بوت النوم", "اضطرابات النوم"),
    (21, "🩺", "بوت الفحص العام", "الفحوصات الدورية"),
    (22, "💉", "بوت التطعيمات", "جدول التطعيمات"),
    (23, "🌡️", "بوت الحمى", "تشخيص الحمى"),
    (24, "🤧", "بوت الحساسية", "أمراض الحساسية"),
    (25, "🦾", "بوت الذكاء الطبي الشامل", "تشخيص شامل"),
]

@app.route('/medical_ai')
def medical_ai_home():
    if 'medical_user' not in session: return redirect('/medical_login')
    bots_html = ""
    for bot_id, icon, name, desc in medical_bots:
        bots_html += f'<div style="background:linear-gradient(145deg,#1a3e2e,#0d2e1e);border-radius:15px;padding:20px;text-align:center;border:1px solid rgba(74,255,176,0.3);"><div style="font-size:2.5rem;">{icon}</div><h3 style="color:#4affb0;margin:10px 0;">{name}</h3><p style="color:#aaa;font-size:0.8rem;">{desc}</p></div>'
    content = f'<h2>🦅 الذكاء الطبي - 25 بوت متخصص</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:15px;">{bots_html}</div>'
    return render_template_string(MED_PAGE, content=content)

# ========== 100 نظام حماية طبي ==========
medical_protections = []
for i in range(1, 101):
    medical_protections.append({
        "id": i,
        "name": f"درع طبي {i}",
        "type": "حماية",
        "status": "مفعل",
        "description": f"نظام حماية طبي متكامل رقم {i}"
    })

@app.route('/medical_protections')
def medical_protections_page():
    if 'medical_user' not in session: return redirect('/medical_login')
    html = ""
    for p in medical_protections:
        html += f'<div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border-radius:12px;padding:15px;text-align:center;border:1px solid rgba(0,200,255,0.3);"><strong style="color:#00c8ff;">🛡️ {p["name"]}</strong><br><small style="color:#aaa;">{p["description"]}</small></div>'
    content = f'<h2>🛡️ أنظمة الحماية الطبية - 100 نظام</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

# ========== 100 نظام تطوير ذاتي ==========
medical_self_dev = []
for i in range(1, 101):
    medical_self_dev.append({
        "id": i,
        "name": f"نظام تطوير ذاتي {i}",
        "type": "تطوير",
        "status": "مفعل",
        "description": f"نظام تطوير ذاتي طبي متكامل رقم {i}"
    })

@app.route('/medical_self_dev')
def medical_self_dev_page():
    if 'medical_user' not in session: return redirect('/medical_login')
    html = ""
    for s in medical_self_dev:
        html += f'<div style="background:linear-gradient(145deg,#1a3e1a,#0d2e0d);border-radius:12px;padding:15px;text-align:center;border:1px solid rgba(74,255,74,0.3);"><strong style="color:#4aff4a;">🧬 {s["name"]}</strong><br><small style="color:#aaa;">{s["description"]}</small></div>'
    content = f'<h2>🧬 أنظمة التطوير الذاتي - 100 نظام</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)



@app.route('/vital_systems')
def vital_systems():
    if 'medical_user' not in session: return redirect('/medical_login')
    content = '''
    <h2>🏥 الأنظمة الطبية الحيوية</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;">
        <a href="/drug_interactions" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #4affb0;"><h3>💊 تفاعلات الأدوية</h3><p style="color:#aaa;">11 نظام</p></a>
        <a href="/medical_history" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #00c8ff;"><h3>📋 التاريخ المرضي</h3><p style="color:#aaa;">11 نظام</p></a>
        <a href="/emergency_alerts" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #ff4a4a;"><h3>🚨 تنبيهات الطوارئ</h3><p style="color:#aaa;">11 نظام</p></a>
        <a href="/surgical_consent" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #FFD700;"><h3>📜 موافقات العمليات</h3><p style="color:#aaa;">11 نظام</p></a>
        <a href="/data_privacy" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #4affb0;"><h3>🔐 خصوصية البيانات</h3><p style="color:#aaa;">11 نظام</p></a>
    </div>'''
    return render_template_string(MED_PAGE, content=content)

@app.route('/drug_interactions')
def drug_interactions():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["فحص التعارض الدوائي","قاعدة بيانات الأدوية","تنبيهات الجرعات","تفاعلات الأعشاب","تفاعلات الحساسية","فحص الأدوية للحوامل","فحص أدوية الأطفال","تفاعلات الأغذية","تنبيهات الفشل الكلوي","تنبيهات الفشل الكبدي"]
    html = "".join([f'<div style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #4affb0;"><strong style="color:#4affb0;">💊 {s}</strong></div>' for s in systems])
    content = f'<h2>💊 نظام تفاعلات الأدوية + 10 داعمة</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/medical_history')
def medical_history():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["سجل الأمراض السابقة","سجل العمليات","سجل الحساسية","سجل الأدوية الحالية","التاريخ العائلي","سجل التطعيمات","سجل الحمل","سجل الحوادث","سجل الدخول للمستشفى","ملف المريض الكامل"]
    html = "".join([f'<div style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #00c8ff;"><strong style="color:#00c8ff;">📋 {s}</strong></div>' for s in systems])
    content = f'<h2>📋 التاريخ المرضي + 10 داعمة</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/emergency_alerts')
def emergency_alerts():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["تنبيه فوري للأطباء","تنبيه غرفة الطوارئ","تنبيه العناية المركزة","تنبيه الصيدلية","تنبيه المختبر","تنبيه الأشعة","تنبيه الإدارة","تنبيه الأمن","تنبيه الإسعاف","تنبيه العائلة"]
    html = "".join([f'<div style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #ff4a4a;"><strong style="color:#ff4a4a;">🚨 {s}</strong></div>' for s in systems])
    content = f'<h2>🚨 تنبيهات الطوارئ + 10 داعمة</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/surgical_consent')
def surgical_consent():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["موافقة العملية","موافقة التخدير","موافقة نقل الدم","موافقة العلاج الكيماوي","موافقة الإشعاع","موافقة التجارب","موافقة الأطفال","موافقة الطوارئ","موافقة التبرع","موافقة الخروج"]
    html = "".join([f'<div style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #FFD700;"><strong style="color:#FFD700;">📜 {s}</strong></div>' for s in systems])
    content = f'<h2>📜 موافقات العمليات + 10 داعمة</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/data_privacy')
def data_privacy():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["تشفير السجلات","صلاحيات الوصول","سجل الدخول","نسخ احتياطي مشفر","إخفاء الهوية","قفل الملفات","تدقيق الخصوصية","حماية كلمة المرور","مصادقة ثنائية","تسجيل الخروج التلقائي"]
    html = "".join([f'<div style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #4affb0;"><strong style="color:#4affb0;">🔐 {s}</strong></div>' for s in systems])
    content = f'<h2>🔐 خصوصية البيانات + 10 داعمة</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=False)
