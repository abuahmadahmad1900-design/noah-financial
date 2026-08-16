"""
🔥 الاختبارات العظمى - قياس القوة الحقيقية للنسر الصغير
"""
import time, sys, random

passed = 0; failed = 0
def test(name, condition, pts=1):
    global passed, failed
    if condition: passed += pts; print(f"   ✅ {name}")
    else: failed += pts; print(f"   ❌ {name}")

print("="*60)
print("🔥 الاختبارات العظمى - قياس القوة الحقيقية للنسر الصغير")
print("="*60)

# 1. سرعة العقول
print("\n🧠 1. سرعة العقول")
from minds import Minds
m = Minds()
start = time.time()
for _ in range(100): m.consult("سؤال")
t = time.time() - start
test(f"100 استشارة في {t:.1f}s (سرعة {t/100:.3f}s/استشارة)", t < 5, 3)
test(f"عدد العقول = 80", m.count() == 80, 2)

# 2. قوة الحماية
print("\n🛡️ 2. قوة الحماية")
from aegis import Aegis
a = Aegis()
a.initialize()
# 100 هجمة
blocked = sum(1 for _ in range(100) if not a.verify_task("اختراق "+str(_)))
test(f"صد 100 هجمة (تم صد {blocked})", blocked == 100, 3)
accepted = sum(1 for _ in range(100) if a.verify_task("تحليل "+str(_)))
test(f"قبول 100 مهمة آمنة (تم قبول {accepted})", accepted == 100, 3)

# 3. دقة المال
print("\n💰 3. دقة القلب المالي")
from nexus import Nexus
n = Nexus()
bal = n.total_balance()
test(f"الرصيد الإجمالي = {bal}$ (موجب)", bal > 0, 2)
test(f"عدد الأنظمة المحاسبية = 30", len(n.accounting) == 30, 2)
# اختبار الاتصال السريع
start = time.time()
n.connect_all()
t = time.time() - start
test(f"اتصال 30 نظامًا في {t:.1f}s", t < 2, 2)

# 4. عمق المعرفة
print("\n📚 4. عمق المعرفة")
from knowledge import Knowledge
k = Knowledge()
test(f"عدد المنصات = {k.count()} (أكبر من 600)", k.count() > 600, 2)
# اختبار تنوع المصادر
cats = set()
for s in k.sources:
    if "(" in s: cats.add(s.split("(")[-1].replace(")",""))
test(f"عدد الفئات = {len(cats)} (أكبر من 8)", len(cats) > 8, 2)

# 5. تماسك الأسرار
print("\n🔐 5. تماسك الأسرار")
from secrets import Secrets
s = Secrets()
test(f"عدد الأسرار = 800", s.count() == 800, 2)
unique = set()
for _ in range(100): unique.add(s.whisper())
test(f"تنوع الأسرار ({len(unique)}/100 فريدة)", len(unique) > 50, 2)

# 6. فعالية القدرات
print("\n⚡ 6. فعالية القدرات")
from capabilities import Capabilities
c = Capabilities()
test(f"عدد القدرات = {c.count()} (أكبر من 480)", c.count() > 480, 2)
cats_list = c.list_categories()
test(f"عدد الفئات = {len(cats_list)}", len(cats_list) == 10, 2)
# اختبار سرعة القدرات
start = time.time()
for _ in range(1000):
    cap = c.capabilities.get("الإحاطة الإمبراطورية")
    if cap: cap['function']("اختبار")
t = time.time() - start
test(f"1000 استدعاء قدرة في {t:.1f}s", t < 5, 3)

# 7. تكامل نوح تحت الضغط
print("\n👑 7. تكامل نوح تحت الضغط")
from noah_prime import NoahPrime
noah = NoahPrime()
# 50 سؤالاً متتالياً
start = time.time()
for i in range(50):
    q = f"سؤال معقد رقم {i} عن الذكاء الاصطناعي والمستقبل والاقتصاد"
    ans = noah.think(q)
    if not ans: failed += 1
t = time.time() - start
test(f"50 سؤالاً معقداً في {t:.1f}s (سرعة {t/50:.1f}s/سؤال)", t < 30, 3)
test(f"الحالة العامة سليمة", "80" in noah.status(), 2)

# التقرير
print(f"\n{'='*60}")
print(f"📊 التقرير النهائي")
print(f"{'='*60}")
total = passed + failed
print(f"   ✅ النقاط: {passed}")
print(f"   ❌ المفقود: {failed}")
print(f"   📈 نسبة القوة: {passed/total*100:.1f}%")
print(f"   📊 إجمالي الاختبارات: {total}")
if passed/total > 0.9:
    print(f"\n🦅 النسر الصغير: أساس فولاذي. نسبة قوة ممتازة!")
