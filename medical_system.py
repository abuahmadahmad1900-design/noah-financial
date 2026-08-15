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
        ('صدرية','أمراض الصدر والتنفس'),
        ('دم','أمراض الدم'),
        ('جهاز هضمي','المعدة والأمعاء'),
        ('كلى','أمراض الكلى'),
        ('غدد صماء','السكري والهرمونات'),
        ('عدوى','الأمراض المعدية'),
        ('تخدير','التخدير والعناية'),
        ('أشعة تشخيصية','التصوير الطبي'),
        ('باثولوجيا','علم الأمراض'),
        ('تمريض','التمريض'),
        ('عناية مركزة','الحالات الحرجة'),
        ('طب مسنين','رعاية كبار السن'),
        ('تأهيل','العلاج الطبيعي'),
        ('صيدلة سريرية','الصيدلة'),
        ('سمعيات','السمع والتوازن'),
    ]
    c.execute("DELETE FROM specialties")
    for name, desc in specialties:
        c.execute("INSERT INTO specialties (name, description) VALUES (?,?)", (name, desc))
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
        @keyframes float-circle {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        @keyframes spin-icon {
            0%, 100% { transform: rotate(0deg); }
            50% { transform: rotate(10deg); }
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
        <div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-bottom:25px;padding:20px;background:linear-gradient(145deg,rgba(26,26,62,0.95),rgba(13,13,32,0.95));border-radius:25px;border:2px solid rgba(74,255,176,0.3);box-shadow:0 10px 30px rgba(0,0,0,0.5),inset 0 0 20px rgba(74,255,176,0.05);">
            <a href="/medical_dashboard" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #FFD700;box-shadow:0 0 15px rgba(255,215,0,0.3);text-decoration:none;color:#FFD700;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:0s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">🏠</span>الرئيسية</a>
            <a href="/specialties" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #4affb0;box-shadow:0 0 15px rgba(74,255,176,0.3);text-decoration:none;color:#4affb0;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:0.2s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">📋</span>التخصصات</a>
            <a href="/doctors" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #00c8ff;box-shadow:0 0 15px rgba(0,200,255,0.3);text-decoration:none;color:#00c8ff;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:0.4s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">🩺</span>الأطباء</a>
            <a href="/patients" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #4affb0;box-shadow:0 0 15px rgba(74,255,176,0.3);text-decoration:none;color:#4affb0;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:0.6s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">👥</span>المرضى</a>
            <a href="/appointments" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #FFD700;box-shadow:0 0 15px rgba(255,215,0,0.3);text-decoration:none;color:#FFD700;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:0.8s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">📅</span>المواعيد</a>
            <a href="/prescriptions" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #4affb0;box-shadow:0 0 15px rgba(74,255,176,0.3);text-decoration:none;color:#4affb0;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:1s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">💊</span>الوصفات</a>
            <a href="/medical_invoices" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #00c8ff;box-shadow:0 0 15px rgba(0,200,255,0.3);text-decoration:none;color:#00c8ff;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:1.2s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">🧾</span>الفواتير</a>
            <a href="/lab_tests" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #4affb0;box-shadow:0 0 15px rgba(74,255,176,0.3);text-decoration:none;color:#4affb0;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:1.4s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">🔬</span>المختبر</a>
            <a href="/radiology" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #FFD700;box-shadow:0 0 15px rgba(255,215,0,0.3);text-decoration:none;color:#FFD700;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:1.6s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">📷</span>الأشعة</a>
            <a href="/pharmacy" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #4affb0;box-shadow:0 0 15px rgba(74,255,176,0.3);text-decoration:none;color:#4affb0;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:1.8s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">💊</span>الصيدلية</a>
            <a href="/rooms" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #00c8ff;box-shadow:0 0 15px rgba(0,200,255,0.3);text-decoration:none;color:#00c8ff;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:2s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">🛏️</span>الغرف</a>
            <a href="/operations" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #ff4a4a;box-shadow:0 0 15px rgba(255,74,74,0.3);text-decoration:none;color:#ff4a4a;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:2.2s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">🔪</span>العمليات</a>
            <a href="/departments" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #FFD700;box-shadow:0 0 15px rgba(255,215,0,0.3);text-decoration:none;color:#FFD700;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:2.4s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">🏢</span>الأقسام</a>
            <a href="/medical_records" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #4affb0;box-shadow:0 0 15px rgba(74,255,176,0.3);text-decoration:none;color:#4affb0;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:2.6s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">📄</span>السجلات</a>
            <a href="/medical_alerts" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #ff4a4a;box-shadow:0 0 15px rgba(255,74,74,0.3);text-decoration:none;color:#ff4a4a;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:2.8s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">🔔</span>التنبيهات</a>
            <a href="/medical_ai" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #00c8ff;box-shadow:0 0 15px rgba(0,200,255,0.3);text-decoration:none;color:#00c8ff;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:3s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">🧠</span>الذكاء</a>
            <a href="/medical_encyclopedia" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #FFD700;box-shadow:0 0 25px rgba(255,215,0,0.5);text-decoration:none;color:#FFD700;font-size:0.75rem;animation:float-circle 3s ease-in-out infinite;"><span style="font-size:1.5rem;">📚</span>الموسوعة</a>
        <a href="/emergency" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #ff4a4a;box-shadow:0 0 15px rgba(255,74,74,0.3);text-decoration:none;color:#ff4a4a;font-size:0.75rem;animation:float-circle 3s ease-in-out infinite;"><span style="font-size:1.5rem;">🚑</span>الطوارئ</a>
        <a href="/insurance" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #FFD700;box-shadow:0 0 15px rgba(255,215,0,0.3);text-decoration:none;color:#FFD700;font-size:0.75rem;animation:float-circle 3s ease-in-out infinite;"><span style="font-size:1.5rem;">🏥</span>التأمين</a>
        <a href="/vaccinations" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #4affb0;box-shadow:0 0 15px rgba(74,255,176,0.3);text-decoration:none;color:#4affb0;font-size:0.75rem;animation:float-circle 3s ease-in-out infinite;"><span style="font-size:1.5rem;">💉</span>التطعيمات</a>
        <a href="/incubators" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #FFD700;box-shadow:0 0 15px rgba(255,215,0,0.3);text-decoration:none;color:#FFD700;font-size:0.75rem;animation:float-circle 3s ease-in-out infinite;"><span style="font-size:1.5rem;">👶</span>الحضانات</a>
        <a href="/medical_apps" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #00c8ff;box-shadow:0 0 25px rgba(0,200,255,0.5);text-decoration:none;color:#00c8ff;font-size:0.75rem;animation:float-circle 3s ease-in-out infinite;"><span style="font-size:1.5rem;">📱</span>التطبيقات</a>
        <a href="/logout_medical" style="display:flex;flex-direction:column;align-items:center;gap:5px;padding:15px;border-radius:50%;width:90px;height:90px;justify-content:center;background:linear-gradient(145deg,#1a1a4e,#0d0d2e);border:2px solid #ff4a4a;box-shadow:0 0 15px rgba(255,74,74,0.3);text-decoration:none;color:#ff4a4a;font-size:0.75rem;transition:all 0.3s;animation:float-circle 3s ease-in-out infinite;animation-delay:3.2s;"><span style="font-size:1.5rem;animation:spin-icon 4s linear infinite;">🚪</span>خروج</a>
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
    error_msg = "<p style='color:#ff4a4a;font-weight:bold;'>❌ بيانات خاطئة</p>" if error else ""
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🦅 دخول نوح الطبي</title>
        <style>
            * { margin:0; padding:0; box-sizing:border-box; }
            body {
                font-family: Tahoma, sans-serif;
                background: linear-gradient(135deg, #0a2e2e, #1a0a3e, #0e1a2e);
                background-size: 400% 400%;
                animation: bg-shift 8s ease infinite;
                color: #fff;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            @keyframes bg-shift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            .login-box {
                width: 100%;
                max-width: 450px;
                background: rgba(10,20,30,0.9);
                padding: 50px 40px;
                border-radius: 30px;
                border: 2px solid #4affb0;
                text-align: center;
                box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 50px rgba(74,255,176,0.4);
                animation: glow-box 3s ease-in-out infinite alternate;
            }
            @keyframes glow-box {
                from { box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 30px rgba(74,255,176,0.3); }
                to { box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 70px rgba(74,255,176,0.7); }
            }
            .logo {
                font-size: 4rem;
                animation: bounce 2s ease-in-out infinite;
            }
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-15px); }
            }
            h2 {
                font-size: 2rem;
                background: linear-gradient(45deg, #4affb0, #00c8ff, #FFD700);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gradient-shift 3s ease infinite;
            }
            @keyframes gradient-shift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            .subtitle { color: #aaa; margin: 20px 0 30px; }
            input {
                display: block;
                width: 100%;
                padding: 15px;
                margin: 15px 0;
                background: rgba(255,255,255,0.05);
                border: 2px solid #4affb0;
                color: #fff;
                border-radius: 15px;
                font-size: 1rem;
                outline: none;
            }
            input:focus {
                border-color: #FFD700;
                box-shadow: 0 0 25px rgba(255,215,0,0.4);
            }
            button {
                width: 100%;
                padding: 15px;
                background: linear-gradient(45deg, #4affb0, #00c8ff);
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 1.1rem;
                cursor: pointer;
                color: #000;
                margin-top: 10px;
            }
            button:hover {
                transform: translateY(-3px);
                box-shadow: 0 15px 35px rgba(74,255,176,0.5);
            }
        </style>
    </head>
    <body>
        <div class="login-box">
            <div class="logo">🏥</div>
            <h2>🦅 نوح الطبي</h2>
            <p class="subtitle">النظام الطبي الأسطوري المتكامل</p>
            """ + error_msg + """
            <form method="POST">
                <input type="text" name="username" placeholder="👤 اسم المستخدم" required>
                <input type="password" name="password" placeholder="🔒 كلمة المرور" required>
                <button type="submit">🚀 دخول</button>
            </form>
        </div>
    </body>
    </html>
    """

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
    <div style="background:linear-gradient(145deg,rgba(26,26,62,0.9),rgba(13,13,32,0.9));border-radius:25px;padding:30px;margin-bottom:30px;border:2px solid rgba(74,255,176,0.4);box-shadow:0 15px 40px rgba(0,0,0,0.5),0 0 40px rgba(74,255,176,0.2),inset 0 0 30px rgba(74,255,176,0.05);text-align:center;animation:glow-border 3s ease-in-out infinite alternate;">
        <h3 style="color:#FFD700;margin-bottom:20px;font-size:1.3rem;text-shadow:0 0 15px rgba(255,215,0,0.5);">⚡ الأنظمة المتقدمة</h3>
        <div style="display:flex;flex-wrap:wrap;gap:15px;justify-content:center;">
            <a href="/vital_systems" style="background:linear-gradient(45deg,#ff4a4a,#ff8c00);color:#fff;padding:15px 30px;border-radius:25px;text-decoration:none;font-weight:bold;box-shadow:0 0 25px rgba(255,74,74,0.6);transition:all 0.3s;animation:pulse-red 2s infinite;">🏥 الأنظمة الحيوية</a>
            <a href="/vital_systems2" style="background:linear-gradient(45deg,#8b5cf6,#ec4899);color:#fff;padding:15px 30px;border-radius:25px;text-decoration:none;font-weight:bold;box-shadow:0 0 25px rgba(139,92,246,0.6);transition:all 0.3s;animation:pulse-purple 2s infinite;">🚀 الأنظمة المتقدمة</a>
            <a href="/medical_ai" style="background:linear-gradient(45deg,#f59e0b,#ef4444);color:#fff;padding:15px 30px;border-radius:25px;text-decoration:none;font-weight:bold;box-shadow:0 0 25px rgba(245,158,11,0.6);transition:all 0.3s;animation:pulse-orange 2s infinite;">🧠 الذكاء الطبي</a>
        </div>
    </div>
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
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #4affb0;display:block;text-decoration:none;margin:5px;"><strong style="color:#4affb0;">💊 {s}</strong></a>'
    content = f'<h2>💊 نظام تفاعلات الأدوية + 10 داعمة</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/medical_history')
def medical_history():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["سجل الأمراض السابقة","سجل العمليات","سجل الحساسية","سجل الأدوية الحالية","التاريخ العائلي","سجل التطعيمات","سجل الحمل","سجل الحوادث","سجل الدخول للمستشفى","ملف المريض الكامل"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #00c8ff;display:block;text-decoration:none;"><strong style="color:#00c8ff;">📋 {s}</strong></a>'
    content = f'<h2>📋 التاريخ المرضي + 10 داعمة</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/emergency_alerts')
def emergency_alerts():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["تنبيه فوري للأطباء","تنبيه غرفة الطوارئ","تنبيه العناية المركزة","تنبيه الصيدلية","تنبيه المختبر","تنبيه الأشعة","تنبيه الإدارة","تنبيه الأمن","تنبيه الإسعاف","تنبيه العائلة"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #ff4a4a;display:block;text-decoration:none;"><strong style="color:#ff4a4a;">🚨 {s}</strong></a>'
    content = f'<h2>🚨 تنبيهات الطوارئ + 10 داعمة</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/surgical_consent')
def surgical_consent():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["موافقة العملية","موافقة التخدير","موافقة نقل الدم","موافقة العلاج الكيماوي","موافقة الإشعاع","موافقة التجارب","موافقة الأطفال","موافقة الطوارئ","موافقة التبرع","موافقة الخروج"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #FFD700;display:block;text-decoration:none;"><strong style="color:#FFD700;">📜 {s}</strong></a>'
    content = f'<h2>📜 موافقات العمليات + 10 داعمة</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/data_privacy')
def data_privacy():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["تشفير السجلات","صلاحيات الوصول","سجل الدخول","نسخ احتياطي مشفر","إخفاء الهوية","قفل الملفات","تدقيق الخصوصية","حماية كلمة المرور","مصادقة ثنائية","تسجيل الخروج التلقائي"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #4affb0;display:block;text-decoration:none;"><strong style="color:#4affb0;">🔐 {s}</strong></a>'
    content = f'<h2>🔐 خصوصية البيانات + 10 داعمة</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

SYSTEM_DETAILS = {
    "فحص التعارض الدوائي": ("💊", "يكتشف التعارض بين الأدوية", ["فحص فوري", "تنبيهات", "قاعدة بيانات"]),
    "قاعدة بيانات الأدوية": ("💊", "مكتبة شاملة للأدوية", ["10,000+ دواء", "تحديث يومي", "بحث"]),
    "تنبيهات الجرعات": ("💊", "مراقبة الجرعات", ["حساب تلقائي", "تنبيه", "سجل"]),
    "تفاعلات الأعشاب": ("🌿", "تفاعل الأعشاب مع الأدوية", ["قاعدة أعشاب", "تحذيرات", "توصيات"]),
    "تفاعلات الحساسية": ("⚠️", "كشف حساسية الأدوية", ["سجل", "تنبيه", "بدائل"]),
    "فحص الأدوية للحوامل": ("🤰", "أمان الأدوية للحوامل", ["تصنيف", "بدائل", "استشارات"]),
    "فحص أدوية الأطفال": ("👶", "جرعات الأطفال", ["حسب الوزن", "حسب العمر", "تحذيرات"]),
    "تفاعلات الأغذية": ("🍽️", "تفاعل الأدوية مع الأطعمة", ["قائمة", "تحذيرات", "توصيات"]),
    "تنبيهات الفشل الكلوي": ("🫘", "جرعات مرضى الكلى", ["تصفية", "تعديل", "متابعة"]),
    "تنبيهات الفشل الكبدي": ("🫁", "جرعات مرضى الكبد", ["فحص", "تعديل", "تحذيرات"]),
    "سجل الأمراض السابقة": ("📋", "سجل الأمراض", ["تاريخ", "تصنيف", "تقارير"]),
    "سجل العمليات": ("🔪", "سجل الجراحات", ["تفاصيل", "متابعة", "تقارير"]),
    "سجل الحساسية": ("⚠️", "حساسية المريض", ["أنواع", "شدة", "تنبيهات"]),
    "سجل الأدوية الحالية": ("💊", "أدوية المريض", ["قائمة", "جرعات", "مدة"]),
    "التاريخ العائلي": ("👨‍👩‍👧‍👦", "أمراض العائلة", ["شجرة", "وراثة", "توصيات"]),
    "سجل التطعيمات": ("💉", "تطعيمات المريض", ["جدول", "تذكير", "شهادات"]),
    "سجل الحمل": ("🤰", "متابعة الحمل", ["دورية", "فحوصات", "تنبيهات"]),
    "سجل الحوادث": ("🚑", "الحوادث والإصابات", ["تفاصيل", "إصابات", "علاج"]),
    "سجل الدخول للمستشفى": ("🏥", "سجل التنويم", ["مدة", "أقسام", "علاج"]),
    "ملف المريض الكامل": ("📄", "ملف شامل", ["كل البيانات", "تقارير", "متابعة"]),
    "تنبيه فوري للأطباء": ("🔔", "تنبيه الأطباء", ["فوري", "مباشر", "سجل"]),
    "تنبيه غرفة الطوارئ": ("🚨", "تنبيه الطوارئ", ["فوري", "فريق", "استجابة"]),
    "تنبيه العناية المركزة": ("🏥", "تنبيه العناية", ["مراقبة", "تنبيه", "استجابة"]),
    "تنبيه الصيدلية": ("💊", "تنبيه الصيدلية", ["تجهيز", "تنبيه", "تسليم"]),
    "تنبيه المختبر": ("🔬", "تنبيه المختبر", ["فحوصات", "نتائج", "تنبيه"]),
    "تنبيه الأشعة": ("📷", "تنبيه الأشعة", ["تصوير", "نتائج", "تنبيه"]),
    "تنبيه الإدارة": ("📋", "تنبيه الإدارة", ["تقارير", "متابعة", "قرارات"]),
    "تنبيه الأمن": ("🔐", "تنبيه الأمن", ["حماية", "مراقبة", "استجابة"]),
    "تنبيه الإسعاف": ("🚑", "تنبيه الإسعاف", ["استدعاء", "تجهيز", "نقل"]),
    "تنبيه العائلة": ("👨‍👩‍👧‍👦", "إبلاغ العائلة", ["إبلاغ", "تحديث", "دعم"]),
    "موافقة العملية": ("📜", "موافقة جراحية", ["نموذج", "توقيع", "سجل"]),
    "موافقة التخدير": ("😴", "موافقة تخدير", ["نموذج", "توقيع", "سجل"]),
    "موافقة نقل الدم": ("🩸", "موافقة نقل دم", ["نموذج", "توقيع", "سجل"]),
    "موافقة العلاج الكيماوي": ("💉", "موافقة كيماوي", ["نموذج", "توقيع", "سجل"]),
    "موافقة الإشعاع": ("☢️", "موافقة إشعاع", ["نموذج", "توقيع", "سجل"]),
    "موافقة التجارب": ("🧪", "موافقة تجارب", ["نموذج", "توقيع", "سجل"]),
    "موافقة الأطفال": ("👶", "موافقة ولي أمر", ["نموذج", "توقيع", "سجل"]),
    "موافقة الطوارئ": ("🚨", "موافقة طارئة", ["نموذج", "توقيع", "سجل"]),
    "موافقة التبرع": ("🎁", "موافقة تبرع", ["نموذج", "توقيع", "سجل"]),
    "موافقة الخروج": ("🚪", "موافقة خروج", ["نموذج", "توقيع", "سجل"]),
    "تشفير السجلات": ("🔐", "تشفير البيانات", ["AES-256", "تلقائي", "آمن"]),
    "صلاحيات الوصول": ("👥", "إدارة الصلاحيات", ["أدوار", "مستويات", "سجل"]),
    "سجل الدخول": ("📋", "تسجيل الدخول", ["تلقائي", "كامل", "تدقيق"]),
    "نسخ احتياطي مشفر": ("💾", "نسخ مشفر", ["تلقائي", "مشفر", "استعادة"]),
    "إخفاء الهوية": ("🎭", "حماية الهوية", ["إخفاء", "ترميز", "حماية"]),
    "قفل الملفات": ("🔒", "قفل السجلات", ["قفل", "فتح", "سجل"]),
    "تدقيق الخصوصية": ("🔍", "تدقيق الخصوصية", ["تدقيق", "تقارير", "امتثال"]),
    "حماية كلمة المرور": ("🔑", "حماية كلمات المرور", ["تشفير", "قوة", "تغيير"]),
    "مصادقة ثنائية": ("📱", "مصادقة ثنائية", ["OTP", "تطبيق", "رسائل"]),
    "تسجيل الخروج التلقائي": ("⏱️", "خروج تلقائي", ["مؤقت", "تلقائي", "آمن"]),
}

@app.route('/system_details/<system_name>')
def system_details(system_name):
    if 'medical_user' not in session: return redirect('/medical_login')
    icon, desc, features = SYSTEM_DETAILS.get(system_name, ("📄", "نظام طبي", []))
    features_html = "".join([f'<li style="color:#ccc;text-align:right;padding:5px;">✅ {f}</li>' for f in features])
    content = f'''
    <h2 style="text-align:center;font-size:2.5rem;background:linear-gradient(45deg,#4affb0,#00c8ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{icon} {system_name}</h2>
    <div style="background:linear-gradient(145deg,#1a1a4e,#0d0d2e);padding:40px;border-radius:25px;border:2px solid #4affb0;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,0.6),0 0 30px rgba(74,255,176,0.3);animation:glow-green 2s infinite;">
        <div style="font-size:4rem;margin-bottom:20px;">{icon}</div>
        <h3 style="color:#4affb0;font-size:1.5rem;">✅ النظام مفعل</h3>
        <p style="color:#ccc;margin:20px 0;font-size:1.1rem;">{desc}</p>
        <h3 style="color:#FFD700;margin:25px 0 15px;font-size:1.3rem;">⚡ المميزات الخارقة:</h3>
        <ul style="list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;">{features_html}</ul>
        <a href="/vital_systems" style="display:inline-block;margin-top:25px;padding:12px 30px;background:linear-gradient(45deg,#4affb0,#00c8ff);color:#000;border-radius:25px;text-decoration:none;font-weight:bold;">🏠 العودة</a>
    </div>'''
    return render_template_string(MED_PAGE, content=content)





@app.route('/ventilation')
def ventilation():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["مراقبة التنفس","ضبط الأكسجين","تنبيه انسداد","مراقبة الضغط","إعدادات المريض","سجل التنفس","تنبيه انقطاع","مراقبة التشبع","إدارة الأنبوب","تنظيف تلقائي"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #00c8ff;display:block;text-decoration:none;margin:5px;"><strong style="color:#00c8ff;">🫁 {s}</strong></a>'
    content = f'<h2>🫁 نظام التنفس الصناعي</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/blood_bank')
def blood_bank():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["إدارة المتبرعين","فصائل الدم","مخزون الدم","فحص الدم","توافق الدم","توزيع الدم","تنبيه نقص","سجل التبرع","فحص الأمراض","تخزين آمن"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #ff4a4a;display:block;text-decoration:none;margin:5px;"><strong style="color:#ff4a4a;">🩸 {s}</strong></a>'
    content = f'<h2>🩸 بنك الدم</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/advanced_lab')
def advanced_lab():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["تحليل الدم الشامل","تحليل البول","تحليل الهرمونات","تحليل الأورام","تحليل الجينات","تحليل المناعة","تحليل البكتيريا","تحليل الفيروسات","تحليل المعادن","نتائج فورية"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #4affb0;display:block;text-decoration:none;margin:5px;"><strong style="color:#4affb0;">🧪 {s}</strong></a>'
    content = f'<h2>🧪 المختبر المتقدم</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/infection_control')
def infection_control():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["تعقيم الأدوات","عزل المرضى","مكافحة البكتيريا","مكافحة الفيروسات","تعقيم الغرف","مراقبة العدوى","تقارير العدوى","تدريب الوقاية","مواد التعقيم","سجل التعقيم"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #FFD700;display:block;text-decoration:none;margin:5px;"><strong style="color:#FFD700;">🦠 {s}</strong></a>'
    content = f'<h2>🦠 مكافحة العدوى</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/iv_fluids')
def iv_fluids():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["معدل التنقيط","نوع المحلول","مراقبة الوريد","تنبيه التسرب","متابعة السوائل","حساب الجرعة","سجل المحاليل","تنبيه الانتهاء","إدارة المضخة","مراقبة التوازن"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #00c8ff;display:block;text-decoration:none;margin:5px;"><strong style="color:#00c8ff;">💉 {s}</strong></a>'
    content = f'<h2>💉 المحاليل الوريدية</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/cardiac_monitor')
def cardiac_monitor():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["مراقبة النبض","مراقبة الضغط","رسم القلب","تنبيه عدم انتظام","سجل القلب","مراقبة الأكسجين","تنبيه السكتة","متابعة دائمة","تحليل الإيقاع","تنبيه فوري"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #ff4a4a;display:block;text-decoration:none;margin:5px;"><strong style="color:#ff4a4a;">🫀 {s}</strong></a>'
    content = f'<h2>🫀 مراقبة القلب</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/neuro_monitor')
def neuro_monitor():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["مراقبة الوعي","مراقبة الضغط الدماغي","رسم المخ","تنبيه التشنج","متابعة الأعصاب","سجل المخ","تنبيه السكتة","مراقبة الحدقة","تحليل الاستجابة","تنبيه فوري"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #4affb0;display:block;text-decoration:none;margin:5px;"><strong style="color:#4affb0;">🧠 {s}</strong></a>'
    content = f'<h2>🧠 مراقبة المخ</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/neonatal')
def neonatal():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["مراقبة المواليد","الحضانات","مراقبة الوزن","مراقبة التغذية","مراقبة التنفس","مراقبة الصفار","سجل المواليد","تنبيه فوري","رعاية خاصة","متابعة النمو"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #FFD700;display:block;text-decoration:none;margin:5px;"><strong style="color:#FFD700;">👶 {s}</strong></a>'
    content = f'<h2>👶 حديثي الولادة</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/air_ambulance')
def air_ambulance():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["تنسيق الطيران","تجهيز الطائرة","فريق طبي جوي","مراقبة المريض","تواصل أرضي","تنسيق المستشفى","سجل الرحلات","تنبيه فوري","معدات الطيران","إدارة الوقود"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #00c8ff;display:block;text-decoration:none;margin:5px;"><strong style="color:#00c8ff;">🚑 {s}</strong></a>'
    content = f'<h2>🚑 الإسعاف الجوي</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/remote_monitor')
def remote_monitor():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["مراقبة من المنزل","أجهزة استشعار","تطبيق متابعة","تنبيه الأطباء","سجل القياسات","مراقبة السكر","مراقبة الضغط","مراقبة القلب","تواصل مرئي","تقارير دورية"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #4affb0;display:block;text-decoration:none;margin:5px;"><strong style="color:#4affb0;">📡 {s}</strong></a>'
    content = f'<h2>📡 المراقبة عن بعد</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)



@app.route('/vital_systems2')
def vital_systems2():
    if 'medical_user' not in session: return redirect('/medical_login')
    content = '''
    <h2>🏥 جميع الأنظمة الحيوية</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;">
        <a href="/ventilation" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #00c8ff;"><h3>🫁 التنفس الصناعي</h3><p style="color:#aaa;">11 نظام</p></a>
        <a href="/blood_bank" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #ff4a4a;"><h3>🩸 بنك الدم</h3><p style="color:#aaa;">11 نظام</p></a>
        <a href="/advanced_lab" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #4affb0;"><h3>🧪 المختبر المتقدم</h3><p style="color:#aaa;">11 نظام</p></a>
        <a href="/infection_control" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #FFD700;"><h3>🦠 مكافحة العدوى</h3><p style="color:#aaa;">11 نظام</p></a>
        <a href="/iv_fluids" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #00c8ff;"><h3>💉 المحاليل</h3><p style="color:#aaa;">11 نظام</p></a>
        <a href="/cardiac_monitor" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #ff4a4a;"><h3>🫀 مراقبة القلب</h3><p style="color:#aaa;">11 نظام</p></a>
        <a href="/neuro_monitor" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #4affb0;"><h3>🧠 مراقبة المخ</h3><p style="color:#aaa;">11 نظام</p></a>
        <a href="/neonatal" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #FFD700;"><h3>👶 حديثي الولادة</h3><p style="color:#aaa;">11 نظام</p></a>
        <a href="/air_ambulance" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #00c8ff;"><h3>🚑 إسعاف جوي</h3><p style="color:#aaa;">11 نظام</p></a>
        <a href="/remote_monitor" style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;border:2px solid #4affb0;"><h3>📡 مراقبة عن بعد</h3><p style="color:#aaa;">11 نظام</p></a>
    </div>'''
    return render_template_string(MED_PAGE, content=content)

# ========== الموسوعة الطبية الشاملة ==========
MEDICAL_ENCYCLOPEDIA = [
    # منصات طبية عالمية
    ("🌍", "منظمة الصحة العالمية WHO", "https://www.who.int", "منصة عالمية"),
    ("🌍", "Medscape", "https://www.medscape.com", "منصة تعليمية"),
    ("🌍", "WebMD", "https://www.webmd.com", "موسوعة طبية"),
    ("🌍", "Mayo Clinic", "https://www.mayoclinic.org", "مرجع طبي"),
    ("🌍", "Cleveland Clinic", "https://my.clevelandclinic.org", "مرجع طبي"),
    ("🌍", "Johns Hopkins Medicine", "https://www.hopkinsmedicine.org", "مرجع طبي"),
    ("🌍", "NIH - National Institutes of Health", "https://www.nih.gov", "معهد صحي"),
    ("🌍", "CDC - Centers for Disease Control", "https://www.cdc.gov", "مركز أمراض"),
    ("🌍", "NHS - National Health Service", "https://www.nhs.uk", "خدمة صحية"),
    ("🌍", "PubMed", "https://pubmed.ncbi.nlm.nih.gov", "مكتبة أبحاث"),
    ("🌍", "UpToDate", "https://www.uptodate.com", "مرجع سريري"),
    ("🌍", "BMJ - British Medical Journal", "https://www.bmj.com", "مجلة طبية"),
    ("🌍", "The Lancet", "https://www.thelancet.com", "مجلة طبية"),
    ("🌍", "JAMA - Journal of American Medical Association", "https://jamanetwork.com", "مجلة طبية"),
    ("🌍", "NEJM - New England Journal of Medicine", "https://www.nejm.org", "مجلة طبية"),
    ("🌍", "Cochrane Library", "https://www.cochranelibrary.com", "مكتبة مراجعات"),
    ("🌍", "ClinicalTrials.gov", "https://clinicaltrials.gov", "تجارب سريرية"),
    ("🌍", "Drugs.com", "https://www.drugs.com", "موسوعة أدوية"),
    ("🌍", "RxList", "https://www.rxlist.com", "موسوعة أدوية"),
    ("🌍", "MedlinePlus", "https://medlineplus.gov", "موسوعة طبية"),
    ("🌍", "Healthline", "https://www.healthline.com", "موسوعة صحية"),
    ("🌍", "Medical News Today", "https://www.medicalnewstoday.com", "أخبار طبية"),
    ("🌍", "ScienceDirect", "https://www.sciencedirect.com", "مكتبة علمية"),
    ("🌍", "Springer Medicine", "https://www.springer.com/medicine", "ناشر طبي"),
    ("🌍", "Oxford Medical", "https://academic.oup.com", "مرجع أكاديمي"),
    ("🌍", "Cambridge Medicine", "https://www.cambridge.org/medicine", "مرجع أكاديمي"),
    ("🌍", "Radiopaedia", "https://radiopaedia.org", "موسوعة أشعة"),
    ("🌍", "Pathology Outlines", "https://www.pathologyoutlines.com", "مرجع باثولوجيا"),
    ("🌍", "DermNet", "https://dermnetnz.org", "موسوعة جلدية"),
    ("🌍", "OrthoInfo", "https://orthoinfo.aaos.org", "مرجع عظام"),
    ("🌍", "American Heart Association", "https://www.heart.org", "مرجع قلب"),
    ("🌍", "American Diabetes Association", "https://www.diabetes.org", "مرجع سكري"),
    ("🌍", "American Cancer Society", "https://www.cancer.org", "مرجع أورام"),
    ("🌍", "Alzheimer's Association", "https://www.alz.org", "مرجع زهايمر"),
    ("🌍", "Arthritis Foundation", "https://www.arthritis.org", "مرجع مفاصل"),
    ("🌍", "Asthma and Allergy Foundation", "https://www.aafa.org", "مرجع حساسية"),
    ("🌍", "Epilepsy Foundation", "https://www.epilepsy.com", "مرجع صرع"),
    ("🌍", "National Kidney Foundation", "https://www.kidney.org", "مرجع كلى"),
    ("🌍", "American Lung Association", "https://www.lung.org", "مرجع رئة"),
    ("🌍", "American Academy of Pediatrics", "https://www.aap.org", "مرجع أطفال"),
    ("🌍", "American College of Surgeons", "https://www.facs.org", "مرجع جراحة"),
    ("🌍", "American Psychiatric Association", "https://www.psychiatry.org", "مرجع نفسية"),
    ("🌍", "World Medical Association", "https://www.wma.net", "جمعية طبية"),
    ("🌍", "Doctors Without Borders", "https://www.msf.org", "منظمة إغاثة"),
    ("🌍", "World Health Academy", "https://www.who.int/academy", "أكاديمية"),
    ("🌍", "Khan Academy Medicine", "https://www.khanacademy.org/science/health-and-medicine", "تعليم طبي"),
    ("🌍", "Coursera Medicine", "https://www.coursera.org/browse/health", "دورات طبية"),
    ("🌍", "edX Medicine", "https://www.edx.org/learn/medicine", "دورات طبية"),
    ("🌍", "Udemy Medicine", "https://www.udemy.com/courses/health-and-fitness/medicine/", "دورات طبية"),
    ("🌍", "FutureLearn Medicine", "https://www.futurelearn.com/subjects/healthcare-medicine-courses", "دورات طبية"),
    ("🌍", "Medical Reference App", "https://www.medscape.com/app", "تطبيق طبي"),
    ("🌍", "Epocrates", "https://www.epocrates.com", "مرجع أدوية"),
    ("🌍", "VisualDX", "https://www.visualdx.com", "تشخيص بصري"),
    ("🌍", "Osmosis", "https://www.osmosis.org", "تعليم طبي"),
    ("🌍", "Amboss", "https://www.amboss.com", "مرجع تعليمي"),
    ("🌍", "Lecturio", "https://www.lecturio.com", "تعليم طبي"),
    ("🌍", "Sketchy Medical", "https://www.sketchy.com", "تعليم بصري"),
    ("🌍", "Picmonic", "https://www.picmonic.com", "تعليم بصري"),
    ("🌍", "Radiology Assistant", "https://radiologyassistant.nl", "مرجع أشعة"),
    ("🌍", "ECG Library", "https://ecglibrary.com", "مرجع قلب"),
    ("🌍", "DermIS", "https://www.dermis.net", "موسوعة جلدية"),
    ("🌍", "Orphanet", "https://www.orpha.net", "أمراض نادرة"),
    ("🌍", "Genetics Home Reference", "https://ghr.nlm.nih.gov", "مرجع وراثة"),
    ("🌍", "DrugBank", "https://www.drugbank.com", "قاعدة أدوية"),
    ("🌍", "PharmGKB", "https://www.pharmgkb.org", "وراثة دوائية"),
    ("🌍", "ClinicalKey", "https://www.clinicalkey.com", "مرجع سريري"),
    ("🌍", "AccessMedicine", "https://accessmedicine.mhmedical.com", "مرجع تعليمي"),
    ("🌍", "STAT Pearls", "https://www.statpearls.com", "مرجع تعليمي"),
    ("🌍", "Medbullets", "https://medbullets.com", "تعليم طبي"),
    ("🌍", "TeachMeSurgery", "https://teachmesurgery.com", "تعليم جراحة"),
    ("🌍", "Geeky Medics", "https://geekymedics.com", "تعليم طبي"),
    ("🌍", "Almost Doctor", "https://almostadoctor.co.uk", "تعليم طبي"),
    ("🌍", "Medical Student", "https://www.medicalstudent.com", "بوابة طلاب"),
    ("🌍", "World Journal of Medicine", "https://www.wjgnet.com", "مجلة طبية"),
    ("🌍", "International Journal of Medicine", "https://www.ijmedicine.com", "مجلة طبية"),
    ("🌍", "Open Medicine", "https://www.openmedicine.org", "مجلة مفتوحة"),
    ("🌍", "PLOS Medicine", "https://journals.plos.org/plosmedicine/", "مجلة مفتوحة"),
    ("🌍", "BMC Medicine", "https://bmcmedicine.biomedcentral.com", "مجلة مفتوحة"),
    ("🌍", "Nature Medicine", "https://www.nature.com/nm/", "مجلة علمية"),
    ("🌍", "Science Translational Medicine", "https://www.science.org/journal/stm", "مجلة علمية"),
    ("🌍", "Cell Medicine", "https://www.cell.com/medicine", "مجلة علمية"),
    ("🌍", "WHO Academy", "https://www.who.int/academy", "أكاديمية"),
    ("🌍", "Medical Education Online", "https://www.tandfonline.com", "تعليم طبي"),
    ("🌍", "Health Education England", "https://www.hee.nhs.uk", "تعليم صحي"),
    ("🌍", "Royal College of Physicians", "https://www.rcplondon.ac.uk", "كلية طبية"),
    ("🌍", "Royal College of Surgeons", "https://www.rcseng.ac.uk", "كلية جراحة"),
    ("🌍", "American Medical Association", "https://www.ama-assn.org", "جمعية طبية"),
    ("🌍", "British Medical Association", "https://www.bma.org.uk", "جمعية طبية"),
    ("🌍", "World Federation for Medical Education", "https://wfme.org", "اتحاد تعليم"),
    ("🌍", "International Federation of Medical Students", "https://ifmsa.org", "اتحاد طلاب"),
    ("🌍", "Medical Council of Canada", "https://mcc.ca", "مجلس طبي"),
    ("🌍", "General Medical Council UK", "https://www.gmc-uk.org", "مجلس طبي"),
    ("🌍", "Australian Medical Council", "https://www.amc.org.au", "مجلس طبي"),
    ("🌍", "Medical Board of California", "https://www.mbc.ca.gov", "مجلس طبي"),
    ("📚", "MSD Manual", "https://www.msdmanuals.com", "مرجع طبي شامل"),
    ("📚", "Merck Manual", "https://www.merckmanuals.com", "موسوعة طبية"),
    ("📚", "Harrison's Principles", "https://accessmedicine.mhmedical.com", "مرجع باطنة"),
    ("📚", "Gray's Anatomy", "https://www.bartleby.com/lit-hub/anatomy-of-the-human-body", "مرجع تشريح"),
    ("📚", "Netter Images", "https://www.netterimages.com", "أطلس تشريح"),
    ("🔬", "Google Scholar", "https://scholar.google.com", "بحث علمي"),
    ("🔬", "ResearchGate", "https://www.researchgate.net", "شبكة باحثين"),
    ("🔬", "ORCID", "https://orcid.org", "معرفات الباحثين"),
    ("🔬", "Scopus", "https://www.scopus.com", "قاعدة بيانات علمية"),
    ("🔬", "Web of Science", "https://www.webofscience.com", "فهرس علمي"),
    ("💊", "FDA", "https://www.fda.gov", "إدارة الغذاء والدواء"),
    ("💊", "EMA", "https://www.ema.europa.eu", "وكالة الأدوية الأوروبية"),
    ("💊", "PDR", "https://www.pdr.net", "مرجع الأدوية"),
    ("💊", "Micromedex", "https://www.micromedexsolutions.com", "معلومات دوائية"),
    ("💊", "Lexicomp", "https://online.lexi.com", "مرجع أدوية"),
    ("🩺", "MedCram", "https://www.medcram.com", "فيديوهات طبية"),
    ("🩺", "Dr. Najeeb", "https://www.drnajeeblectures.com", "محاضرات طبية"),
    ("🩺", "Armando Hasudungan", "https://www.youtube.com/user/armandohasudungan", "رسوم تعليمية"),
    ("🩺", "Zero to Finals", "https://zerotofinals.com", "تعليم طبي"),
    ("🩺", "PassMedicine", "https://www.passmedicine.com", "أسئلة تدريب"),
    ("🌍", "UNICEF", "https://www.unicef.org", "منظمة طفولة"),
    ("🌍", "Red Cross", "https://www.icrc.org", "صليب أحمر"),
    ("🌍", "World Bank Health", "https://www.worldbank.org/en/topic/health", "بنك صحي"),
    ("🌍", "UNESCO Health", "https://www.unesco.org/en/health-education", "تعليم صحي"),
    ("🌍", "FAO Health", "https://www.fao.org/nutrition/en", "صحة غذائية"),
    ("🏥", "Cleveland Clinic Abu Dhabi", "https://www.clevelandclinicabudhabi.ae", "مستشفى عالمي"),
    ("🏥", "King Faisal Specialist Hospital", "https://www.kfshrc.edu.sa", "مستشفى تخصصي"),
    ("🏥", "Sheba Medical Center", "https://www.shebaonline.org", "مستشفى عالمي"),
    ("🏥", "Singapore General Hospital", "https://www.sgh.com.sg", "مستشفى عالمي"),
    ("🏥", "Charité Berlin", "https://www.charite.de", "مستشفى جامعي"),
    ("📱", "Figure 1", "https://www.figure1.com", "مشاركة حالات"),
    ("📱", "MedCalc", "https://www.medcalc.org", "حاسبة طبية"),
    ("📱", "Calculate by QxMD", "https://qxmd.com/calculate", "أدوات سريرية"),
    ("📱", "Read by QxMD", "https://qxmd.com/read", "مجلات طبية"),
    ("📱", "MDCalc", "https://www.mdcalc.com", "حاسبات طبية"),
    ("🇸🇦", "وزارة الصحة السعودية", "https://www.moh.gov.sa", "وزارة صحة"),
    ("🇦🇪", "وزارة الصحة الإماراتية", "https://www.mohap.gov.ae", "وزارة صحة"),
    ("🇪🇬", "وزارة الصحة المصرية", "https://www.mohp.gov.eg", "وزارة صحة"),
    ("🇯🇴", "وزارة الصحة الأردنية", "https://www.moh.gov.jo", "وزارة صحة"),
    ("🇲🇦", "وزارة الصحة المغربية", "https://www.sante.gov.ma", "وزارة صحة"),
    ("🇮🇶", "وزارة الصحة العراقية", "https://moh.gov.iq", "وزارة صحة"),
    ("🇩🇿", "وزارة الصحة الجزائرية", "https://www.sante.gov.dz", "وزارة صحة"),
    ("🇹🇳", "وزارة الصحة التونسية", "https://www.santetunisie.rns.tn", "وزارة صحة"),
    ("🇱🇧", "وزارة الصحة اللبنانية", "https://www.moph.gov.lb", "وزارة صحة"),
    ("🇸🇾", "وزارة الصحة السورية", "https://www.moh.gov.sy", "وزارة صحة"),
    ("🇸🇩", "وزارة الصحة السودانية", "https://www.fmoh.gov.sd", "وزارة صحة"),
    ("🇾🇪", "وزارة الصحة اليمنية", "https://www.moh.gov.ye", "وزارة صحة"),
    ("🇱🇾", "وزارة الصحة الليبية", "https://www.health.gov.ly", "وزارة صحة"),
    ("🇵🇸", "وزارة الصحة الفلسطينية", "https://www.moh.ps", "وزارة صحة"),
    ("📚", "الطبي", "https://www.altibbi.com", "موسوعة طبية عربية"),
    ("📚", "ويب طب", "https://www.webteb.com", "موسوعة صحية عربية"),
    ("📚", "صحتي", "https://www.sehati.gov.sa", "منصة صحية سعودية"),
    ("📚", "طبيب دوت كوم", "https://www.tabeeb.com", "استشارات طبية"),
    ("📚", "كل يوم معلومة طبية", "https://www.dailymedicalinfo.com", "معلومات طبية"),
    ("📚", "الكونسلتو", "https://www.elconsolto.com", "موسوعة طبية"),
    ("📚", "طب ويب", "https://www.tabibweb.com", "موسوعة طبية"),
    ("📚", "صحتك", "https://www.sehatok.com", "منصة صحية"),
    ("📚", "الطبيبة", "https://www.altabeba.com", "استشارات نسائية"),
    ("📚", "طب العرب", "https://www.tebarab.com", "موسوعة طبية"),
    ("🎓", "جامعة الملك سعود - الطب", "https://medicine.ksu.edu.sa", "كلية طب"),
    ("🎓", "جامعة الملك عبدالعزيز - الطب", "https://medicine.kau.edu.sa", "كلية طب"),
    ("🎓", "جامعة القاهرة - الطب", "https://www.medicine.cu.edu.eg", "كلية طب"),
    ("🎓", "جامعة عين شمس - الطب", "https://www.asu.edu.eg", "كلية طب"),
    ("🎓", "الجامعة الأمريكية في بيروت - الطب", "https://www.aub.edu.lb/fm", "كلية طب"),
    ("🎓", "جامعة دمشق - الطب", "https://www.damascusuniversity.edu.sy", "كلية طب"),
    ("🎓", "جامعة بغداد - الطب", "https://www.med.uobaghdad.edu.iq", "كلية طب"),
    ("🏥", "مستشفى الملك فيصل التخصصي", "https://www.kfshrc.edu.sa", "مستشفى تخصصي"),
    ("🏥", "مستشفى الملك فهد", "https://www.kfsh.med.sa", "مستشفى"),
    ("🏥", "مستشفى سليمان الحبيب", "https://hmg.com", "مجموعة طبية"),
    ("🏥", "مستشفى المواساة", "https://www.mouwasat.com", "مستشفى"),
    ("🏥", "المستشفى التخصصي", "https://www.specialty-hospital.com", "مستشفى"),
    ("🏥", "مستشفى الأردن", "https://www.jordan-hospital.com", "مستشفى"),
    ("🏥", "مستشفى السلام", "https://www.alsalamhospital.com", "مستشفى"),
    ("🏥", "مستشفى السعودي الألماني", "https://saudigerman.com", "مجموعة مستشفيات"),
    ("📚", "MSD Manual", "https://www.msdmanuals.com", "مرجع طبي شامل"),
    ("📚", "Merck Manual", "https://www.merckmanuals.com", "موسوعة طبية"),
    ("📚", "Harrison's Principles", "https://accessmedicine.mhmedical.com", "مرجع باطنة"),
    ("📚", "Gray's Anatomy", "https://www.bartleby.com/lit-hub/anatomy-of-the-human-body", "مرجع تشريح"),
    ("📚", "Netter Images", "https://www.netterimages.com", "أطلس تشريح"),
    ("🔬", "Google Scholar", "https://scholar.google.com", "بحث علمي"),
    ("🔬", "ResearchGate", "https://www.researchgate.net", "شبكة باحثين"),
    ("🔬", "ORCID", "https://orcid.org", "معرفات الباحثين"),
    ("🔬", "Scopus", "https://www.scopus.com", "قاعدة بيانات علمية"),
    ("🔬", "Web of Science", "https://www.webofscience.com", "فهرس علمي"),
    ("💊", "FDA", "https://www.fda.gov", "إدارة الغذاء والدواء"),
    ("💊", "EMA", "https://www.ema.europa.eu", "وكالة الأدوية الأوروبية"),
    ("💊", "PDR", "https://www.pdr.net", "مرجع الأدوية"),
    ("💊", "Micromedex", "https://www.micromedexsolutions.com", "معلومات دوائية"),
    ("💊", "Lexicomp", "https://online.lexi.com", "مرجع أدوية"),
    ("🩺", "MedCram", "https://www.medcram.com", "فيديوهات طبية"),
    ("🩺", "Dr. Najeeb", "https://www.drnajeeblectures.com", "محاضرات طبية"),
    ("🩺", "Armando Hasudungan", "https://www.youtube.com/user/armandohasudungan", "رسوم تعليمية"),
    ("🩺", "Zero to Finals", "https://zerotofinals.com", "تعليم طبي"),
    ("🩺", "PassMedicine", "https://www.passmedicine.com", "أسئلة تدريب"),
    ("🌍", "UNICEF", "https://www.unicef.org", "منظمة طفولة"),
    ("🌍", "Red Cross", "https://www.icrc.org", "صليب أحمر"),
    ("🌍", "World Bank Health", "https://www.worldbank.org/en/topic/health", "بنك صحي"),
    ("🌍", "UNESCO Health", "https://www.unesco.org/en/health-education", "تعليم صحي"),
    ("🌍", "FAO Health", "https://www.fao.org/nutrition/en", "صحة غذائية"),
    ("🏥", "Cleveland Clinic Abu Dhabi", "https://www.clevelandclinicabudhabi.ae", "مستشفى عالمي"),
    ("🏥", "Sheba Medical Center", "https://www.shebaonline.org", "مستشفى عالمي"),
    ("🏥", "Singapore General Hospital", "https://www.sgh.com.sg", "مستشفى عالمي"),
    ("🏥", "Charité Berlin", "https://www.charite.de", "مستشفى جامعي"),
    ("📱", "Figure 1", "https://www.figure1.com", "مشاركة حالات"),
    ("📱", "MedCalc", "https://www.medcalc.org", "حاسبة طبية"),
    ("📱", "Calculate by QxMD", "https://qxmd.com/calculate", "أدوات سريرية"),
    ("📱", "Read by QxMD", "https://qxmd.com/read", "مجلات طبية"),
    ("📱", "MDCalc", "https://www.mdcalc.com", "حاسبات طبية"),
]

@app.route('/medical_encyclopedia')
def medical_encyclopedia():
    if 'medical_user' not in session: return redirect('/medical_login')
    html = ""
    for icon, name, url, desc in MEDICAL_ENCYCLOPEDIA:
        html += f'<a href="{url}" target="_blank" style="background:#1a1a4e;padding:15px;border-radius:12px;text-align:center;border:1px solid #4affb0;display:block;text-decoration:none;margin:5px;"><span style="font-size:2rem;">{icon}</span><br><strong style="color:#4affb0;">{name}</strong><br><small style="color:#aaa;">{desc}</small></a>'
    content = f'<h2>📚 الموسوعة الطبية الشاملة - {len(MEDICAL_ENCYCLOPEDIA)} مصدر</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

# ========== التطبيقات والتواصل الاجتماعي ==========
MEDICAL_APPS = [
    ("💼", "LinkedIn Medical", "https://www.linkedin.com", "شبكة مهنية"),
    ("🐦", "Twitter X Medical", "https://twitter.com", "أخبار طبية"),
    ("📘", "Facebook Medical Groups", "https://www.facebook.com", "مجموعات طبية"),
    ("📱", "Telegram Medical", "https://t.me", "قنوات طبية"),
    ("💬", "WhatsApp Medical", "https://www.whatsapp.com", "مجموعات استشارية"),
    ("📺", "YouTube Medical", "https://www.youtube.com", "فيديوهات طبية"),
    ("📸", "Instagram Medical", "https://www.instagram.com", "توعية صحية"),
    ("🎵", "TikTok Medical", "https://www.tiktok.com", "فيديوهات قصيرة"),
    ("👽", "Reddit Medical", "https://www.reddit.com", "منتديات طبية"),
    ("❓", "Quora Medical", "https://www.quora.com", "أسئلة وأجوبة"),
    ("🤖", "Ada", "https://ada.com", "تشخيص الأعراض"),
    ("🏥", "Babylon", "https://www.babylonhealth.com", "استشارات"),
    ("📞", "Teladoc", "https://www.teladoc.com", "طب عن بعد"),
    ("💻", "Amwell", "https://www.amwell.com", "استشارات"),
    ("🩺", "Doctor on Demand", "https://www.doctorondemand.com", "طب فوري"),
]

@app.route('/medical_apps')
def medical_apps():
    if 'medical_user' not in session: return redirect('/medical_login')
    html = ""
    for icon, name, url, desc in MEDICAL_APPS:
        html += f'<a href="{url}" target="_blank" style="background:#1a1a4e;padding:15px;border-radius:12px;text-align:center;border:1px solid #00c8ff;display:block;text-decoration:none;margin:5px;"><span style="font-size:2rem;">{icon}</span><br><strong style="color:#00c8ff;">{name}</strong><br><small style="color:#aaa;">{desc}</small></a>'
    content = f'<h2>📱 التطبيقات والتواصل الطبي - {len(MEDICAL_APPS)} تطبيق</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

# ========== الطوارئ ==========
@app.route('/emergency')
def emergency():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["استقبال الطوارئ","فرز الحالات","سيارات الإسعاف","غرفة الإنعاش","طوارئ القلب","طوارئ الحوادث","طوارئ الأطفال","طوارئ الحروق","طوارئ التسمم","طوارئ نفسية"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #ff4a4a;display:block;text-decoration:none;margin:5px;"><strong style="color:#ff4a4a;">🚑 {s}</strong></a>'
    content = f'<h2>🚑 نظام الطوارئ</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

# ========== التأمين الصحي ==========
@app.route('/insurance')
def insurance():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["شركات التأمين","الموافقات","المطالبات","تغطية العلاج","نسبة التحمل","سقف التأمين","التأمين الشامل","تأمين الأسنان","تأمين الأدوية","تأمين العمليات"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #FFD700;display:block;text-decoration:none;margin:5px;"><strong style="color:#FFD700;">🏥 {s}</strong></a>'
    content = f'<h2>🏥 التأمين الصحي</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

# ========== التطعيمات ==========
@app.route('/vaccinations')
def vaccinations():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["جدول التطعيمات","تطعيمات الأطفال","تطعيمات الكبار","تطعيمات الحوامل","تطعيمات السفر","تطعيم الإنفلونزا","تطعيم كورونا","متابعة الجرعات","تنبيه المواعيد","سجل التطعيمات"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #4affb0;display:block;text-decoration:none;margin:5px;"><strong style="color:#4affb0;">💉 {s}</strong></a>'
    content = f'<h2>💉 التطعيمات</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

# ========== الحضانات ==========
@app.route('/incubators')
def incubators():
    if 'medical_user' not in session: return redirect('/medical_login')
    systems = ["حضانات المواليد","مراقبة الوزن","مراقبة التنفس","مراقبة الحرارة","مراقبة التغذية","مراقبة الصفار","رعاية الخدج","متابعة النمو","تنبيه فوري","سجل المواليد"]
    html = ""
    for s in systems:
        html += f'<a href="/system_details/{s}" style="background:#1a1a4e;padding:15px;border-radius:10px;text-align:center;border:1px solid #FFD700;display:block;text-decoration:none;margin:5px;"><strong style="color:#FFD700;">👶 {s}</strong></a>'
    content = f'<h2>👶 الحضانات</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">{html}</div>'
    return render_template_string(MED_PAGE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=False)

@app.route('/medical_reports')
def medical_reports():
    if 'medical_user' not in session: return redirect('/medical_login')
    conn = sqlite3.connect(DB_MED); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM patients"); patients = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM doctors"); doctors = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM appointments"); appts = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM prescriptions"); presc = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM medical_invoices"); total_rev = c.fetchone()[0]
    conn.close()
    content = '<h2>📊 التقارير</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:15px;">'
    content += f'<div style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;"><h3 style="color:#4affb0;">{patients}</h3>مرضى</div>'
    content += f'<div style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;"><h3 style="color:#4affb0;">{doctors}</h3>أطباء</div>'
    content += f'<div style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;"><h3 style="color:#4affb0;">{appts}</h3>مواعيد</div>'
    content += f'<div style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;"><h3 style="color:#4affb0;">{presc}</h3>وصفات</div>'
    content += f'<div style="background:#1a1a4e;padding:25px;border-radius:15px;text-align:center;"><h3 style="color:#FFD700;">{total_rev}</h3>إيرادات</div>'
    content += '</div>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/medical_search')
def medical_search():
    if 'medical_user' not in session: return redirect('/medical_login')
    query = request.args.get('q', '')
    results = []
    if query:
        conn = sqlite3.connect(DB_MED); c = conn.cursor()
        c.execute("SELECT 'مريض', name FROM patients WHERE name LIKE ?", (f'%{query}%',))
        results.extend(c.fetchall())
        c.execute("SELECT 'طبيب', name FROM doctors WHERE name LIKE ?", (f'%{query}%',))
        results.extend(c.fetchall())
        c.execute("SELECT 'تخصص', name FROM specialties WHERE name LIKE ?", (f'%{query}%',))
        results.extend(c.fetchall())
        c.execute("SELECT 'دواء', medicine_name FROM pharmacy WHERE medicine_name LIKE ?", (f'%{query}%',))
        results.extend(c.fetchall())
        conn.close()
    content = f'<h2>🔍 البحث</h2><form method="GET"><input name="q" placeholder="ابحث..." value="{query}"><button>بحث</button></form><table><tr><th>النوع</th><th>الاسم</th></tr>'
    for r in results:
        content += f'<tr><td>{r[0]}</td><td>{r[1]}</td></tr>'
    content += '</table>'
    return render_template_string(MED_PAGE, content=content)

@app.route('/medical_notifications')
def medical_notifications():
    if 'medical_user' not in session: return redirect('/medical_login')
    notifications = ["📅 تذكير بموعد المريض غداً","💊 تنبيه: دواء قارب على الانتهاء","🔬 نتيجة فحص جاهزة","🏥 غرفة 101 أصبحت متاحة"]
    html = "".join([f'<div style="background:#1a1a4e;padding:15px;border-radius:10px;margin:5px;border:1px solid #4affb0;">🔔 {n}</div>' for n in notifications])
    content = f'<h2>🔔 الإشعارات</h2>{html}'
    return render_template_string(MED_PAGE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=False)
