print("="*60)
print("🧪 اختبار القدرات العامة - المرحلة الثانية")
print("="*60)

score = 0
total = 0

# 1. اختبار العقول (121)
print("\n🧠 1. العقول")
from minds import Minds
m = Minds()
total += 1
if m.count() == 121: score += 1; print("✅ عدد العقول 121")
else: print(f"❌ عدد العقول {m.count()}")

# 2. اختبار الدروع (80)
print("\n🛡️ 2. الدروع")
from aegis import Aegis
a = Aegis()
total += 1
if len(a.shields) == 80: score += 1; print("✅ عدد الدروع 80")
else: print(f"❌ عدد الدروع {len(a.shields)}")

# 3. اختبار الأسرار (800)
print("\n🔐 3. الأسرار")
from secrets import Secrets
s = Secrets()
total += 1
if s.count() == 800: score += 1; print("✅ عدد الأسرار 800")
else: print(f"❌ عدد الأسرار {s.count()}")

# 4. اختبار الوعي السائل
print("\n🧬 4. الوعي السائل")
from liquid_consciousness_absolute import LiquidConsciousnessAbsolute
lc = LiquidConsciousnessAbsolute()
total += 1
if lc.system_count() == 80: score += 1; print("✅ أنظمة الوعي السائل 80")
else: print(f"❌ أنظمة الوعي السائل {lc.system_count()}")
# اختبار عملي
result = lc.flow("كيف أزيد أرباحي؟")
total += 1
if result and len(result) > 20: score += 1; print("✅ الوعي السائل يعمل")
else: print("❌ الوعي السائل لا يعمل")

# 5. اختبار النواة المقدسة
print("\n🕯️ 5. النواة المقدسة")
from sacred_core import SacredCore
sc = SacredCore()
total += 2
if sc.count_abilities() == 40: score += 1; print("✅ قدرات النواة 40")
else: print(f"❌ قدرات النواة {sc.count_abilities()}")
if sc.count_secrets() == 40: score += 1; print("✅ أسرار النواة 40")
else: print(f"❌ أسرار النواة {sc.count_secrets()}")

# 6. اختبار بروتوكول الأفق
print("\n🌀 6. بروتوكول الأفق")
from horizon_protocol import HorizonProtocol
hp = HorizonProtocol()
total += 2
if hp.count() == 150: score += 1; print("✅ أنظمة الأفق 150")
else: print(f"❌ أنظمة الأفق {hp.count()}")
result = hp.ingest("نظام اختباري")
if result and len(result) > 50: score += 1; print("✅ الأفق يعمل")
else: print("❌ الأفق لا يعمل")

# 7. اختبار النظام الصفري
print("\n🕰️ 7. النظام الصفري")
from zero_system_absolute import ZeroSystemAbsolute
zs = ZeroSystemAbsolute()
total += 2
if zs.count() == 150: score += 1; print("✅ أنظمة الصفري 150")
else: print(f"❌ أنظمة الصفري {zs.count()}")
result = zs.predict("كيف سيكون المستقبل؟")
if result and len(result) > 20: score += 1; print("✅ الصفري يعمل")
else: print("❌ الصفري لا يعمل")

# 8. اختبار تكامل نوح
print("\n👑 8. تكامل نوح")
from noah_prime import NoahPrime
noah = NoahPrime()
total += 3
# اختبار الوعي السائل عبر نوح
r1 = noah.think("سائل: كيف أبتكر؟")
if r1 and len(r1) > 20: score += 1; print("✅ نوح + سائل")
else: print("❌ نوح + سائل")
# اختبار الأفق عبر نوح
r2 = noah.think("ابتلاع: TestSystem")
if r2 and len(r2) > 20: score += 1; print("✅ نوح + أفق")
else: print("❌ نوح + أفق")
# اختبار الصفري عبر نوح
r3 = noah.think("توقع: المستقبل")
if r3 and len(r3) > 20: score += 1; print("✅ نوح + صفري")
else: print("❌ نوح + صفري")

print(f"\n{'='*60}")
print(f"📊 النتيجة: {score}/{total}")
if score == total: print("🎉 النسر المحلق: كل الأنظمة تعمل!")
else: print("⚠️ هناك أنظمة تحتاج صيانة")
