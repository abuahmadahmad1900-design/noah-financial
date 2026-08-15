from flask import Flask, request, session, redirect, render_template_string

app = Flask(__name__)
app.secret_key = 'final_finance_2026'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form.get('username', 'admin')
        return redirect('/')
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>🦅 دخول نوح المالي</title>
        <style>
            body { font-family:Tahoma; background:#0a0a2e; color:#fff; display:flex; justify-content:center; align-items:center; height:100vh; }
            .box { background:#1a1a3e; padding:40px; border-radius:25px; border:2px solid #FFD700; text-align:center; box-shadow:0 0 40px rgba(255,215,0,0.4); }
            h2 { color:#FFD700; }
            input { display:block; width:100%; padding:12px; margin:10px 0; background:#222; border:1px solid #FFD700; color:#fff; border-radius:10px; }
            button { width:100%; padding:12px; background:#FFD700; border:none; border-radius:10px; font-weight:bold; cursor:pointer; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>🦅 نوح المالي</h2>
            <form method="POST">
                <input type="text" name="username" placeholder="المستخدم (أي اسم)">
                <input type="password" name="password" placeholder="كلمة المرور (أي شيء)">
                <button type="submit">🚀 دخول</button>
            </form>
        </div>
    </body>
    </html>
    ''')

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')
    return f"<h1 style='text-align:center;color:#FFD700;font-family:Tahoma;'>🦅 مرحباً {session['user']} في نوح المالي</h1>"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
