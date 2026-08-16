#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦅 نوح - واجهة تشغيل العقول
تشغيل أي عقل من المتصفح مباشرة.
"""

import json
from flask import Flask, request, render_template_string
from engine import run_by_id, run_by_name, _get_registry

app = Flask(__name__)

PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦅 نوح - السحر الأعلى</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family: Tahoma, sans-serif;
            background: linear-gradient(135deg, #0a0a2e, #1a0a3e, #0a1a2e, #0a0a2e);
            background-size: 400% 400%;
            animation: bg-shift 8s ease infinite;
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        @keyframes bg-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .container {
            max-width: 1100px;
            margin: 0 auto;
            background: rgba(20,20,50,0.85);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 40px;
            border: 2px solid rgba(255,215,0,0.5);
            box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 60px rgba(255,215,0,0.3), 0 0 100px rgba(0,200,255,0.2);
            animation: glow-pulse 3s ease-in-out infinite alternate;
        }
        @keyframes glow-pulse {
            from { box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 30px rgba(255,215,0,0.3); }
            to { box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 70px rgba(255,215,0,0.6), 0 0 120px rgba(0,200,255,0.4); }
        }
        h1 {
            text-align: center;
            font-size: 2.8rem;
            font-weight: 900;
            background: linear-gradient(45deg, #FFD700, #FF8C00, #FFD700);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient-shift 3s ease infinite;
            margin-bottom: 20px;
        }
        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .buttons-row {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
            margin-bottom: 30px;
        }
        .btn {
            padding: 15px 30px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1rem;
            display: inline-block;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
            letter-spacing: 0.5px;
        }
        .btn:hover {
            transform: translateY(-5px) scale(1.05);
        }
        .btn-gold {
            background: linear-gradient(45deg, #FFD700, #FF8C00);
            color: #000;
            box-shadow: 0 0 25px rgba(255,215,0,0.5);
            animation: pulse-gold 2s infinite;
        }
        @keyframes pulse-gold {
            0%, 100% { box-shadow: 0 0 20px rgba(255,215,0,0.4); }
            50% { box-shadow: 0 0 40px rgba(255,215,0,0.8); }
        }
        .btn-green {
            background: linear-gradient(45deg, #4affb0, #00c8ff);
            color: #000;
            box-shadow: 0 0 25px rgba(74,255,176,0.5);
            animation: pulse-green 2s infinite;
        }
        @keyframes pulse-green {
            0%, 100% { box-shadow: 0 0 20px rgba(74,255,176,0.4); }
            50% { box-shadow: 0 0 40px rgba(74,255,176,0.8); }
        }
        label {
            display: block;
            margin: 15px 0 5px;
            color: #ccc;
            font-size: 1rem;
        }
        input, textarea, select {
            width: 100%;
            padding: 14px;
            margin: 5px 0 15px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 12px;
            color: #fff;
            font-size: 1rem;
            transition: all 0.3s;
            outline: none;
        }
        input:focus, textarea:focus {
            border-color: #FFD700;
            box-shadow: 0 0 20px rgba(255,215,0,0.3);
        }
        textarea {
            min-height: 120px;
            font-family: monospace;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(45deg, #FFD700, #FF8C00);
            color: #000;
            font-weight: bold;
            font-size: 1.1rem;
            cursor: pointer;
            border: none;
            border-radius: 15px;
            transition: all 0.3s;
            letter-spacing: 1px;
        }
        button:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(255,215,0,0.4);
        }
        .result {
            background: rgba(0,200,255,0.1);
            border: 1px solid #00c8ff;
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            font-size: 1.2rem;
            text-align: center;
            animation: fade-in 0.5s ease;
        }
        @keyframes fade-in {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .links-row {
            text-align: center;
            margin-top: 20px;
        }
        .links-row a {
            color: #00c8ff;
            text-decoration: none;
            margin: 0 10px;
            transition: all 0.3s;
        }
        .links-row a:hover {
            color: #FFD700;
            text-shadow: 0 0 10px rgba(255,215,0,0.8);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🦅 نوح - السحر الأعلى</h1>
        <div class="buttons-row">
            <a href="https://noah-financial-1.onrender.com/login" class="btn btn-gold">💼 النظام المالي</a>
            <a href="https://noah-financial-4.onrender.com/medical_login" class="btn btn-green">🏥 النظام الطبي</a>
        </div>
        <form method="POST">
            <label>🧠 اسم العقل أو رقمه:</label>
            <input name="mind_id" placeholder="مثال: 26 أو حاسب الزكاة" required>
            <label>📊 بيانات JSON (اختياري):</label>
            <textarea name="data" placeholder='{"amount": 100000}'></textarea>
            <button type="submit">🚀 تشغيل العقل</button>
        </form>
        {% if result %}
        <div class="result">{{ result }}</div>
        {% endif %}
        <div class="links-row">
            <a href="/">🏠 الرئيسية</a> |
            <a href="/minds">🧠 كل العقول</a>
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        mind_input = request.form.get('mind_id', '').strip()
        data_str = request.form.get('data', '').strip()
        try:
            data = json.loads(data_str) if data_str else {}
        except json.JSONDecodeError:
            data = {}
        if mind_input.isdigit():
            result = run_by_id(int(mind_input), data)
        else:
            result = run_by_name(mind_input, data)
    return render_template_string(PAGE, result=result)

@app.route('/minds')
def minds():
    minds = _get_registry()
    content = '''
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>🧠 كل العقول</title>
    <style>
        body { font-family:Tahoma; background:#0a0a2e; color:#fff; padding:20px; }
        h1 { color:#FFD700; text-align:center; }
        .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:8px; margin-top:20px; }
        .mind { background:#1a1a3e; padding:10px; border-radius:8px; font-size:0.8rem; }
        a { color:#00c8ff; }
    </style>
    </head>
    <body>
        <h1>🧠 عقول نوح (500)</h1>
        <div class="grid">'''
    for m in minds:
        content += f'<div class="mind">{m["id"]}. {m["name"]}<br><small style="color:#aaa;">{m["emperor"]}</small></div>'
    content += '</div><br><a href="/">🏠 العودة</a></body></html>'
    return content

@app.route('/financial')
def financial():
    return redirect('https://noah-financial.onrender.com/login')

if __name__ == '__main__':
    print("🦅 واجهة تشغيل العقول تعمل")
    app.run(host='0.0.0.0', port=5004, debug=False)
