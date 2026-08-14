from flask import Flask, render_template_string
app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🦅 نوح - الإمبراطورية الرقمية</title>
        <style>
            body { font-family:Tahoma; background:#0a0a2e; color:#fff; text-align:center; padding:40px; }
            h1 { font-size:3rem; background:linear-gradient(45deg,#FFD700,#FF8C00); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
            .cards { display:flex; flex-wrap:wrap; gap:20px; justify-content:center; margin:40px 0; }
            .card { background:#1a1a3e; border-radius:20px; padding:30px; width:250px; border:1px solid rgba(255,215,0,0.3); }
            .card h3 { color:#FFD700; }
            a { color:#00c8ff; text-decoration:none; margin:10px; display:inline-block; }
        </style>
    </head>
    <body>
        <h1>🦅 نوح - الإمبراطورية الرقمية</h1>
        <p>النظام المالي والمحاسبي الأقوى في العالم</p>
        <div class="cards">
            <div class="card"><h3>🧠 25 عقل ذكي</h3><p>ذكاء اصطناعي شامل</p></div>
            <div class="card"><h3>📊 50 نظام مالي</h3><p>محاسبة وإدارة متكاملة</p></div>
            <div class="card"><h3>🧬 10 أنظمة تطوير ذاتي</h3><p>تعلم وتكيف مستمر</p></div>
            <div class="card"><h3>🛡️ دروع وحماية</h3><p>اختبارات 100% ناجحة</p></div>
        </div>
        <p>
            <a href="/financial">💼 النظام المالي</a> |
            <a href="/features">⚡ القدرات</a> |
            <a href="/contact">📞 تواصل</a>
        </p>
    </body>
    </html>
    ''')

@app.route('/financial')
def financial():
    return "النظام المالي متاح على: <a href='https://noah-financial.onrender.com'>https://noah-financial.onrender.com</a>"

@app.route('/features')
def features():
    return '''
    <h2>⚡ قدرات نوح</h2>
    <p>25 عقل ذكاء اصطناعي</p>
    <p>50 نظام مالي ومحاسبي</p>
    <p>10 أنظمة تطوير ذاتي</p>
    <p>100+ قدرة محاسبية</p>
    <p>اختبارات أسطورية 100% نجاح</p>
    '''

@app.route('/contact')
def contact():
    return "<h2>📞 تواصل معنا</h2><p>للاستفسار والترخيص، راسلنا</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
