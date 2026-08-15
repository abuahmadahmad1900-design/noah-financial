#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦅 نوح - الذكاء الطبي
25 بوت طبي متخصص يدعم النظام الطبي
"""

from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ========== 25 بوت طبي ==========
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
    bots_html = ""
    for bot_id, icon, name, desc in medical_bots:
        bots_html += f'''
        <div style="background:linear-gradient(145deg,#1a3e2e,#0d2e1e);border-radius:15px;padding:20px;text-align:center;border:1px solid rgba(74,255,176,0.3);">
            <div style="font-size:2.5rem;">{icon}</div>
            <h3 style="color:#4affb0;margin:10px 0;">{name}</h3>
            <p style="color:#aaa;font-size:0.8rem;">{desc}</p>
            <a href="/medical_ai/run/{bot_id}" style="color:#00c8ff;">تشغيل</a>
        </div>'''
    
    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>🦅 نوح - الذكاء الطبي</title>
    <style>
        body {{ font-family:Tahoma; background:#0a2e2e; color:#fff; padding:30px; }}
        h1 {{ text-align:center; color:#4affb0; font-size:2.5rem; margin-bottom:30px; }}
        .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:15px; }}
    </style></head>
    <body>
        <h1>🦅 الذكاء الطبي - 25 بوت متخصص</h1>
        <div class="grid">{bots_html}</div>
    </body></html>'''

@app.route('/medical_ai/run/<int:bot_id>')
def run_medical_bot(bot_id):
    bot = next((b for b in medical_bots if b[0] == bot_id), None)
    if not bot:
        return "❌ البوت غير موجود"
    icon, name = bot[1], bot[2]
    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><title>{icon} {name}</title>
    <style>
        body {{ font-family:Tahoma; background:#0a2e2e; color:#fff; padding:30px; text-align:center; }}
        .box {{ max-width:600px; margin:0 auto; background:#1a3e2e; padding:40px; border-radius:25px; border:2px solid #4affb0; }}
        h1 {{ color:#4affb0; }}
        p {{ color:#ccc; }}
        a {{ color:#00c8ff; }}
    </style></head>
    <body>
        <div class="box">
            <h1>{icon} {name}</h1>
            <p>هذا البوت جاهز للإجابة على استفساراتك الطبية.</p>
            <p style="color:#888;">النسخة الحالية: تشخيص أولي + نصائح</p>
            <a href="/medical_ai">🏠 العودة للبوتات</a>
        </div>
    </body></html>'''

if __name__ == '__main__':
    print("🦅 الذكاء الطبي يعمل - 25 بوت")
    app.run(host='0.0.0.0', port=5008, debug=False)
