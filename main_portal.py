from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def portal():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🦅 نوح - البوابة الرئيسية</title>
        <style>
            body { font-family:Tahoma; background:#0a0a2e; color:#fff; display:flex; justify-content:center; align-items:center; min-height:100vh; }
            .container { text-align:center; }
            h1 { font-size:3rem; background:linear-gradient(45deg,#FFD700,#FF8C00); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
            .cards { display:flex; gap:20px; flex-wrap:wrap; justify-content:center; margin-top:40px; }
            .card { background:#1a1a3e; padding:40px; border-radius:25px; width:250px; border:2px solid #4affb0; text-decoration:none; color:#fff; }
            .card:hover { transform:translateY(-10px); box-shadow:0 20px 40px rgba(0,0,0,0.5); }
            .card .icon { font-size:4rem; }
            .card h2 { margin:15px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🦅 إمبراطورية نوح</h1>
            <div class="cards">
                <a href="https://noah-financial-1.onrender.com" class="card" style="border-color:#FFD700;"><div class="icon">🧠</div><h2>العقول</h2><p>500 عقل ذكي</p></a>
                <a href="https://noah-financial-1.onrender.com/login" class="card" style="border-color:#FFD700;"><div class="icon">💼</div><h2>المالي</h2><p>نظام محاسبي</p></a>
                <a href="https://noah-financial-4.onrender.com/medical_login" class="card" style="border-color:#4affb0;"><div class="icon">🏥</div><h2>الطبي</h2><p>نظام متكامل</p></a>
            </div>
        </div>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)
