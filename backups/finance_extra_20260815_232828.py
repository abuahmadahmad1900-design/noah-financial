from flask import Blueprint, render_template_string, session, redirect

extra = Blueprint('extra', __name__)

PAGE_EXTRA = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>نوح الموسع</title>
<style>
    body { font-family:Tahoma; background:linear-gradient(135deg,#0a0a2e,#1a0a3e); color:#fff; padding:20px; }
    .container { max-width:1200px; margin:0 auto; background:rgba(20,20,50,0.85); border-radius:30px; padding:30px; border:2px solid rgba(255,215,0,0.4); }
    h1 { text-align:center; color:#FFD700; }
    h2 { color:#FFD700; }
</style></head>
<body><div class="container">
{{ content | safe }}
</div></body></html>
'''

@extra.route('/extra_reports')
def extra_reports():
    if 'user' not in session: return redirect('/login')
    content = "<h2>📊 تقارير</h2><p>تقارير مالية مفصلة.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_ratios')
def extra_ratios():
    if 'user' not in session: return redirect('/login')
    content = "<h2>📈 نسب</h2><p>نسب السيولة والربحية.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_forecast')
def extra_forecast():
    if 'user' not in session: return redirect('/login')
    content = "<h2>🧠 تنبؤ</h2><p>توقع الإيرادات.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_scenarios')
def extra_scenarios():
    if 'user' not in session: return redirect('/login')
    content = "<h2>🔮 سيناريوهات</h2><p>أفضل وأسوأ الحالات.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_fraud')
def extra_fraud():
    if 'user' not in session: return redirect('/login')
    content = "<h2>⚠️ احتيال</h2><p>كشف عمليات مشبوهة.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_credit')
def extra_credit():
    if 'user' not in session: return redirect('/login')
    content = "<h2>💳 ائتمان</h2><p>إدارة ائتمان.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_market')
def extra_market():
    if 'user' not in session: return redirect('/login')
    content = "<h2>💰 سوق</h2><p>أسهم وعملات.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_economy')
def extra_economy():
    if 'user' not in session: return redirect('/login')
    content = "<h2>📈 اقتصاد</h2><p>مؤشرات اقتصادية.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_blockchain')
def extra_blockchain():
    if 'user' not in session: return redirect('/login')
    content = "<h2>🔗 بلوكتشين</h2><p>عقود ذكية.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_cloud')
def extra_cloud():
    if 'user' not in session: return redirect('/login')
    content = "<h2>☁️ سحابية</h2><p>تخزين سحابي.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_payments')
def extra_payments():
    if 'user' not in session: return redirect('/login')
    content = "<h2>💳 مدفوعات</h2><p>مدفوعات إلكترونية.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_investments')
def extra_investments():
    if 'user' not in session: return redirect('/login')
    content = "<h2>📈 استثمارات</h2><p>أسهم وسندات.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_banking')
def extra_banking():
    if 'user' not in session: return redirect('/login')
    content = "<h2>🏦 بنوك</h2><p>حسابات وقروض.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_tax')
def extra_tax():
    if 'user' not in session: return redirect('/login')
    content = "<h2>💰 ضرائب</h2><p>حسابات ضريبية.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_inventory')
def extra_inventory():
    if 'user' not in session: return redirect('/login')
    content = "<h2>📦 مخزون</h2><p>إدارة مخزون.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_supply')
def extra_supply():
    if 'user' not in session: return redirect('/login')
    content = "<h2>🚚 توريد</h2><p>سلسلة توريد.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_hr')
def extra_hr():
    if 'user' not in session: return redirect('/login')
    content = "<h2>👷 موارد</h2><p>موارد بشرية.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_crm')
def extra_crm():
    if 'user' not in session: return redirect('/login')
    content = "<h2>👥 CRM</h2><p>علاقات عملاء.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_analytics')
def extra_analytics():
    if 'user' not in session: return redirect('/login')
    content = "<h2>📊 تحليلات</h2><p>بيانات ورسوم.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_ai')
def extra_ai():
    if 'user' not in session: return redirect('/login')
    content = "<h2>🤖 ذكاء</h2><p>تعلم آلي.</p>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_home')
def extra_home():
    if 'user' not in session: return redirect('/login')
    content = """
    <h1>🦅 نوح المالي الموسع</h1>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin:30px 0;">
        <a href="/extra_reports" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #FFD700;color:#FFD700;">📊 تقارير</a>
        <a href="/extra_ratios" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #00c8ff;color:#00c8ff;">📈 نسب</a>
        <a href="/extra_forecast" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #4affb0;color:#4affb0;">🧠 تنبؤ</a>
        <a href="/extra_scenarios" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #FFD700;color:#FFD700;">🔮 سيناريوهات</a>
        <a href="/extra_fraud" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #ff4a4a;color:#ff4a4a;">⚠️ احتيال</a>
        <a href="/extra_credit" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #00c8ff;color:#00c8ff;">💳 ائتمان</a>
        <a href="/extra_market" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #4affb0;color:#4affb0;">💰 سوق</a>
        <a href="/extra_economy" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #FFD700;color:#FFD700;">📈 اقتصاد</a>
        <a href="/extra_blockchain" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #00c8ff;color:#00c8ff;">🔗 بلوكتشين</a>
        <a href="/extra_cloud" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #4affb0;color:#4affb0;">☁️ سحابية</a>
        <a href="/extra_payments" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #FFD700;color:#FFD700;">💳 مدفوعات</a>
        <a href="/extra_investments" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #00c8ff;color:#00c8ff;">📈 استثمارات</a>
        <a href="/extra_banking" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #4affb0;color:#4affb0;">🏦 بنوك</a>
        <a href="/extra_tax" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #FFD700;color:#FFD700;">💰 ضرائب</a>
        <a href="/extra_inventory" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #00c8ff;color:#00c8ff;">📦 مخزون</a>
        <a href="/extra_supply" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #4affb0;color:#4affb0;">🚚 توريد</a>
        <a href="/extra_hr" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #FFD700;color:#FFD700;">👷 موارد</a>
        <a href="/extra_crm" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #00c8ff;color:#00c8ff;">👥 CRM</a>
        <a href="/extra_analytics" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #4affb0;color:#4affb0;">📊 تحليلات</a>
        <a href="/extra_ai" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #FFD700;color:#FFD700;">🤖 ذكاء</a>
    </div>"""
    return render_template_string(PAGE_EXTRA, content=content)
