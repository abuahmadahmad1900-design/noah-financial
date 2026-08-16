print("="*60)
print("🔍 الفحص الشامل للنسر المحلق")
print("="*60)

results = []

# 1. العقول
from minds import Minds
m = Minds()
results.append(("العقول", m.count(), 120))

# 2. الدروع
from aegis import Aegis
a = Aegis()
results.append(("الدروع", len(a.shields), 80))

# 3. الأسرار
from secrets import Secrets
s = Secrets()
results.append(("الأسرار", s.count(), 800))

# 4. القدرات
from capabilities import Capabilities
c = Capabilities()
results.append(("القدرات", c.count(), 499))

# 5. المعرفة
from knowledge import Knowledge
k = Knowledge()
results.append(("المعرفة", k.count(), 980))

# 6. الوعي السائل
from liquid_consciousness_absolute import LiquidConsciousnessAbsolute
lc = LiquidConsciousnessAbsolute()
results.append(("الوعي السائل (أنظمة)", lc.system_count(), 80))
results.append(("الوعي السائل (عقول في البركة)", lc.count(), 121))

# 7. النواة المقدسة
from sacred_core import SacredCore
sc = SacredCore()
results.append(("النواة المقدسة (قدرات)", sc.count_abilities(), 40))
results.append(("النواة المقدسة (أسرار)", sc.count_secrets(), 40))

# 8. بروتوكول الأفق
from horizon_protocol import HorizonProtocol
hp = HorizonProtocol()
results.append(("بروتوكول الأفق", hp.count(), 150))

# 9. النظام الصفري
from zero_system_absolute import ZeroSystemAbsolute
zs = ZeroSystemAbsolute()
results.append(("النظام الصفري", zs.count(), 150))

# عرض النتائج
all_ok = True
for name, actual, expected in results:
    status = "✅" if actual == expected else "❌"
    if actual != expected:
        all_ok = False
    print(f"{status} {name}: {actual} (المتوقع: {expected})")

print("="*60)
if all_ok:
    print("🎉 كل المكونات مكتملة!")
else:
    print("⚠️ هناك مكونات غير مكتملة.")
