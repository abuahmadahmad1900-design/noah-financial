from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def portal():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🦅 نوح - البوابة الرئيسية</title>
        <style>
            * { margin:0; padding:0; box-sizing:border-box; }
            body {
                font-family: Tahoma, sans-serif;
                background: linear-gradient(135deg, #0a0a2e, #1a0a3e, #0a1a2e);
                background-size: 400% 400%;
                animation: bg-shift 8s ease infinite;
                color: #fff;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            @keyframes bg-shift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            .container { text-align: center; max-width: 1000px; }
            h1 {
                font-size: 3rem;
                background: linear-gradient(45deg, #FFD700, #FF8C00, #FFD700);
                background-size: 300% 300%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gradient-shift 3s ease infinite;
            }
            @keyframes gradient-shift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            .subtitle { color:#aaa; margin:10px 0 40px; }
            .cards { display:flex; gap:25px; flex-wrap:wrap; justify-content:center; }
            .card {
                background: rgba(20,20,50,0.9);
                padding: 40px 30px;
                border-radius: 25px;
                width: 280px;
                text-decoration: none;
                color: #fff;
                transition: all 0.3s;
                border: 2px solid;
                position: relative;
                overflow: hidden;
            }
            .card:hover { transform: translateY(-15px) scale(1.03); }
            .card .icon { font-size: 4rem; margin-bottom: 15px; }
            .card h2 { font-size: 1.5rem; margin-bottom: 10px; }
            .card p { color: #aaa; font-size: 0.9rem; }
            .card-1 { border-color: #00c8ff; box-shadow: 0 0 30px rgba(0,200,255,0.3); }
            .card-2 { border-color: #FFD700; box-shadow: 0 0 30px rgba(255,215,0,0.3); }
            .card-3 { border-color: #4affb0; box-shadow: 0 0 30px rgba(74,255,176,0.3); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🦅 إمبراطورية نوح</h1>
            <p class="subtitle">النظام المتكامل للعقول والمالية والطب</p>
            <div class="cards">
                <a href="https://noah-financial-1.onrender.com" class="card card-1">
                    <div class="icon">🧠</div>
                    <h2>العقول الذكية</h2>
                    <p>500 عقل ذكاء اصطناعي</p>
                </a>
                <a href="https://noah-financial-1.onrender.com/login" class="card card-2">
                    <div class="icon">💼</div>
                    <h2>النظام المالي</h2>
                    <p>محاسبة واقتصاد متكامل</p>
                </a>
                <a href="https://noah-financial-4.onrender.com/medical_login" class="card card-3">
                    <div class="icon">🏥</div>
                    <h2>النظام الطبي</h2>
                    <p>عيادات وطب متكامل</p>
                </a>
            </div>
        </div>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=False)
