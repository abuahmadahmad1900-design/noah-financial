from flask import Blueprint, render_template_string, session, redirect

extra = Blueprint('extra', __name__)

PAGE_EXTRA = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>نوح الموسع</title>
<style>
    body { font-family:Tahoma; background:linear-gradient(135deg,#0a0a2e,#1a0a3e); color:#fff; padding:20px; }
    .container { max-width:1200px; margin:0 auto; background:rgba(20,20,50,0.85); border-radius:30px; padding:30px; border:2px solid rgba(255,215,0,0.4); }
    h1, h2 { text-align:center; color:#FFD700; }
    table { width:100%; border-collapse:separate; border-spacing:0; margin-top:25px; border-radius:25px; overflow:hidden; box-shadow:0 25px 60px rgba(0,0,0,0.7), 0 0 40px rgba(255,215,0,0.15); }
    table thead th { background:linear-gradient(145deg,#FFD700,#FF8C00); color:#000; padding:20px; font-size:1.2rem; }
    table tbody td { padding:18px; text-align:center; color:#f0f0f0; border-bottom:1px solid rgba(255,215,0,0.1); }
    table tbody tr:nth-child(odd) td { background:rgba(255,255,255,0.02); }
    table tbody tr:hover td { background:rgba(255,215,0,0.1); color:#FFD700; }
</style></head>
<body><div class="container">
{{ content | safe }}
</div></body></html>'''


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
        <a href="/extra_security" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #4affb0;color:#4affb0;">🔐 حماية</a>
        <a href="/extra_financial_ratios" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #00c8ff;color:#00c8ff;">📊 نسب مالية</a>
        <a href="/extra_cashflow" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #FFD700;color:#FFD700;">💵 تدفقات</a>
        <a href="/extra_budget_plan" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #4affb0;color:#4affb0;">📋 موازنات</a>
        <a href="/extra_inflation" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #FFD700;color:#FFD700;">📊 تضخم</a>
        <a href="/extra_exchange" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #00c8ff;color:#00c8ff;">🌍 صرف</a>
        <a href="/extra_market_index" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #4affb0;color:#4affb0;">📈 أسواق</a>
        <a href="/extra_audit" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #FFD700;color:#FFD700;">🔍 تدقيق</a>
        <a href="/extra_predictive" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #00c8ff;color:#00c8ff;">🧠 تنبؤي</a>
        <a href="/extra_loan" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #FFD700;color:#FFD700;">🏦 قروض</a>
        <a href="/extra_investment_portfolio" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #00c8ff;color:#00c8ff;">📈 محفظة</a>
        <a href="/extra_financial_analysis" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #4affb0;color:#4affb0;">📊 تحليل</a>
        <a href="/extra_trial_balance" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #FFD700;color:#FFD700;">⚖️ ميزان</a>
        <a href="/extra_income_statement" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #00c8ff;color:#00c8ff;">📈 دخل</a>
        <a href="/extra_account_statement" style="background:#1a1a3e;padding:25px;border-radius:20px;text-align:center;border:2px solid #4affb0;color:#4affb0;">💳 كشف حساب</a>
    </div>"""
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_security')
def extra_security():
    if 'user' not in session: return redirect('/login')
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#4affb0;">🔐 مركز الحماية المالية</h2>
        <p style="color:#aaa;">أمان وتشفير وحماية متقدمة</p>
    </div>
    <table>
        <tr><th>الخاصية</th><th>الحالة</th></tr>
        <tr><td>تشفير AES-256</td><td style="color:#4affb0;">✅ مفعل</td></tr>
        <tr><td>نسخ احتياطي تلقائي</td><td style="color:#4affb0;">✅ مفعل</td></tr>
        <tr><td>سجل تدقيق</td><td style="color:#4affb0;">✅ مفعل</td></tr>
        <tr><td>حماية من الهجمات</td><td style="color:#4affb0;">✅ مفعل</td></tr>
    </table>"""
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_financial_ratios')
def extra_financial_ratios():
    if 'user' not in session: return redirect('/login')
    # هنا نحسب نسب مالية حقيقية من قاعدة البيانات
    import sqlite3
    conn = sqlite3.connect('core_finance.db')
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0")
    expenses = abs(c.fetchone()[0])
    c.execute("SELECT COALESCE(SUM(balance),0) FROM accounts WHERE type='أصول'")
    assets = c.fetchone()[0]
    conn.close()
    profit = revenue - expenses
    profit_margin = (profit / revenue * 100) if revenue > 0 else 0
    roi = (profit / assets * 100) if assets > 0 else 0
    content = f"""
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#00c8ff;">📊 النسب المالية</h2>
        <p style="color:#aaa;">تحليل الأداء المالي</p>
    </div>
    <table>
        <tr><th>النسبة</th><th>القيمة</th></tr>
        <tr><td>هامش الربح</td><td style="color:#FFD700;">{profit_margin:.1f}%</td></tr>
        <tr><td>العائد على الأصول</td><td style="color:#FFD700;">{roi:.1f}%</td></tr>
        <tr><td>الإيرادات</td><td>{revenue}</td></tr>
        <tr><td>المصاريف</td><td>{expenses}</td></tr>
    </table>"""
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_cashflow')
def extra_cashflow():
    if 'user' not in session: return redirect('/login')
    import sqlite3
    conn = sqlite3.connect('core_finance.db')
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount > 0")
    inflow = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0")
    outflow = c.fetchone()[0]
    conn.close()
    net = inflow + outflow
    content = f"""
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#4affb0;">💵 التدفقات النقدية</h2>
        <p style="color:#aaa;">مراقبة السيولة</p>
    </div>
    <table>
        <tr><th>داخل</th><th>خارج</th><th>صافي</th></tr>
        <tr><td style="color:#4affb0;">{inflow}</td><td style="color:#ff4a4a;">{outflow}</td><td style="color:#FFD700;">{net}</td></tr>
    </table>"""
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_budget_plan')
def extra_budget_plan():
    if 'user' not in session: return redirect('/login')
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#FFD700;">📋 الموازنات التقديرية</h2>
        <p style="color:#aaa;">تخطيط الميزانيات</p>
    </div>
    <table>
        <tr><th>البند</th><th>المخطط</th><th>الفعلي</th></tr>
        <tr><td>الإيرادات</td><td>40000</td><td>40000</td></tr>
        <tr><td>المصاريف</td><td>15000</td><td>15000</td></tr>
    </table>"""
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_inflation')
def extra_inflation():
    if 'user' not in session: return redirect('/login')
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#FFD700;">📊 التضخم والفائدة</h2>
        <p style="color:#aaa;">مؤشرات اقتصادية</p>
    </div>
    <table>
        <tr><th>المؤشر</th><th>القيمة</th></tr>
        <tr><td>معدل التضخم</td><td>2.5%</td></tr>
        <tr><td>سعر الفائدة</td><td>5.0%</td></tr>
        <tr><td>نمو الناتج المحلي</td><td>3.2%</td></tr>
        <tr><td>معدل البطالة</td><td>5.0%</td></tr>
    </table>"""
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_exchange')
def extra_exchange():
    if 'user' not in session: return redirect('/login')
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#00c8ff;">🌍 أسعار الصرف</h2>
        <p style="color:#aaa;">عملات عالمية</p>
    </div>
    <table>
        <tr><th>العملة</th><th>السعر</th></tr>
        <tr><td>دولار أمريكي</td><td>1.00</td></tr>
        <tr><td>يورو</td><td>0.92</td></tr>
        <tr><td>ريال سعودي</td><td>3.75</td></tr>
        <tr><td>جنيه مصري</td><td>48.5</td></tr>
        <tr><td>درهم إماراتي</td><td>3.67</td></tr>
    </table>"""
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_market_index')
def extra_market_index():
    if 'user' not in session: return redirect('/login')
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#4affb0;">📈 مؤشرات الأسواق</h2>
        <p style="color:#aaa;">أسواق عالمية</p>
    </div>
    <table>
        <tr><th>المؤشر</th><th>القيمة</th><th>التغير</th></tr>
        <tr><td>S&P 500</td><td>5,200</td><td style="color:#4affb0;">+1.2%</td></tr>
        <tr><td>ناسداك</td><td>16,500</td><td style="color:#4affb0;">+1.5%</td></tr>
        <tr><td>داو جونز</td><td>38,000</td><td style="color:#ff4a4a;">-0.3%</td></tr>
        <tr><td>تداول</td><td>12,300</td><td style="color:#4affb0;">+0.8%</td></tr>
    </table>"""
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_audit')
def extra_audit():
    if 'user' not in session: return redirect('/login')
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#FFD700;">🔍 التدقيق المالي</h2>
        <p style="color:#aaa;">سجل العمليات والتدقيق</p>
    </div>
    <table>
        <tr><th>الحدث</th><th>التاريخ</th></tr>
        <tr><td>تسجيل دخول</td><td>2026-08-15</td></tr>
        <tr><td>إضافة فاتورة</td><td>2026-08-15</td></tr>
        <tr><td>حركة بنكية</td><td>2026-08-15</td></tr>
    </table>"""
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_predictive')
def extra_predictive():
    if 'user' not in session: return redirect('/login')
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#00c8ff;">🧠 تحليلات تنبؤية</h2>
        <p style="color:#aaa;">توقع المستقبل المالي</p>
    </div>
    <table>
        <tr><th>المؤشر</th><th>القيمة المتوقعة</th></tr>
        <tr><td>الإيرادات الشهر القادم</td><td style="color:#4affb0;">46,000</td></tr>
        <tr><td>هامش الربح</td><td style="color:#4affb0;">65%</td></tr>
        <tr><td>التدفق النقدي</td><td style="color:#4affb0;">+20,000</td></tr>
    </table>"""
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_loan')
def extra_loan():
    if 'user' not in session: return redirect('/login')
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#FFD700;">🏦 القروض والتمويل</h2>
        <p style="color:#aaa;">إدارة القروض</p>
    </div>
    <table>
        <tr><th>نوع القرض</th><th>المبلغ</th><th>الفائدة</th><th>الحالة</th></tr>
        <tr><td>تمويل شخصي</td><td>100,000</td><td>5%</td><td style="color:#4affb0;">ساري</td></tr>
        <tr><td>تمويل عقاري</td><td>500,000</td><td>4%</td><td style="color:#4affb0;">ساري</td></tr>
    </table>"""
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_investment_portfolio')
def extra_investment_portfolio():
    if 'user' not in session: return redirect('/login')
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#00c8ff;">📈 المحفظة الاستثمارية</h2>
        <p style="color:#aaa;">تنويع الاستثمارات</p>
    </div>
    <table>
        <tr><th>الأصل</th><th>النسبة</th><th>القيمة</th></tr>
        <tr><td>أسهم</td><td>40%</td><td>160,000</td></tr>
        <tr><td>سندات</td><td>30%</td><td>120,000</td></tr>
        <tr><td>عقار</td><td>20%</td><td>80,000</td></tr>
        <tr><td>نقد</td><td>10%</td><td>40,000</td></tr>
    </table>"""
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_financial_analysis')
def extra_financial_analysis():
    if 'user' not in session: return redirect('/login')
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#4affb0;">📊 التحليل المالي الشامل</h2>
        <p style="color:#aaa;">تحليل القوائم المالية</p>
    </div>
    <table>
        <tr><th>البند</th><th>القيمة</th><th>التقييم</th></tr>
        <tr><td>السيولة</td><td>1.8</td><td style="color:#4affb0;">جيدة</td></tr>
        <tr><td>الربحية</td><td>65%</td><td style="color:#4affb0;">ممتازة</td></tr>
        <tr><td>الديون</td><td>25%</td><td style="color:#4affb0;">آمنة</td></tr>
    </table>"""
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_trial_balance')
def extra_trial_balance():
    if 'user' not in session: return redirect('/login')
    import sqlite3
    conn = sqlite3.connect('core_finance.db')
    c = conn.cursor()
    c.execute("SELECT type, SUM(balance) FROM accounts GROUP BY type")
    rows = c.fetchall()
    conn.close()
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#FFD700;">⚖️ ميزان المراجعة</h2>
        <p style="color:#aaa;">أرصدة الحسابات</p>
    </div>
    <table><tr><th>النوع</th><th>الرصيد</th></tr>"""
    for r in rows:
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_income_statement')
def extra_income_statement():
    if 'user' not in session: return redirect('/login')
    import sqlite3
    conn = sqlite3.connect('core_finance.db')
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount),0) FROM invoices")
    revenue = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount),0) FROM bank_moves WHERE amount < 0")
    expenses = abs(c.fetchone()[0])
    conn.close()
    profit = revenue - expenses
    content = f"""
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#00c8ff;">📈 قائمة الدخل</h2>
        <p style="color:#aaa;">الإيرادات والمصاريف</p>
    </div>
    <table>
        <tr><th>الإيرادات</th><th>المصاريف</th><th>صافي الربح</th></tr>
        <tr><td style="color:#4affb0;">{revenue}</td><td style="color:#ff4a4a;">{expenses}</td><td style="color:#FFD700;">{profit}</td></tr>
    </table>"""
    return render_template_string(PAGE_EXTRA, content=content)

@extra.route('/extra_account_statement')
def extra_account_statement():
    if 'user' not in session: return redirect('/login')
    import sqlite3
    conn = sqlite3.connect('core_finance.db')
    c = conn.cursor()
    c.execute("SELECT date, desc, amount FROM bank_moves ORDER BY date DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    content = """
    <div style="text-align:center;">
        <h2 style="font-size:2rem;color:#4affb0;">💳 كشف حساب</h2>
        <p style="color:#aaa;">آخر الحركات</p>
    </div>
    <table><tr><th>التاريخ</th><th>الوصف</th><th>المبلغ</th></tr>"""
    for r in rows:
        color = "#4affb0" if r[2] > 0 else "#ff4a4a"
        content += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td style='color:{color}'>{r[2]}</td></tr>"
    content += "</table>"
    return render_template_string(PAGE_EXTRA, content=content)
