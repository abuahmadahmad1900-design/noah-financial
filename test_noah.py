import sys
print("بدء الاختبارات...")
passed, failed = 0, 0

# 1. Minds
try:
    from minds import Minds
    m = Minds()
    if m.count() == 80: passed += 1
    else: failed += 1; print("FAIL: Minds count")
    r = m.consult("test")
    if r: passed += 1
    else: failed += 1; print("FAIL: Minds consult")
except Exception as e:
    failed += 2; print(f"Minds Error: {e}")

# 2. Aegis
try:
    from aegis import Aegis
    a = Aegis()
    a.initialize()
    if a.verify_task("تحليل"): passed += 1
    else: failed += 1; print("FAIL: Aegis accept")
    if not a.verify_task("اختراق"): passed += 1
    else: failed += 1; print("FAIL: Aegis block")
except Exception as e:
    failed += 2; print(f"Aegis Error: {e}")

# 3. Ethos
try:
    from ethos import Ethos
    e = Ethos()
    ok, _ = e.judge("مساعدة")
    if ok: passed += 1
    else: failed += 1; print("FAIL: Ethos good")
    ok, _ = e.judge("سرقة")
    if not ok: passed += 1
    else: failed += 1; print("FAIL: Ethos evil")
except Exception as e:
    failed += 2; print(f"Ethos Error: {e}")

# 4. Nexus
try:
    from nexus import Nexus
    n = Nexus()
    if len(n.accounting) == 30: passed += 1
    else: failed += 1; print("FAIL: Nexus acc count")
    if n.total_balance() > 0: passed += 1
    else: failed += 1; print("FAIL: Nexus balance")
except Exception as e:
    failed += 2; print(f"Nexus Error: {e}")

# 5. Knowledge
try:
    from knowledge import Knowledge
    k = Knowledge()
    if k.count() >= 300: passed += 1
    else: failed += 1; print("FAIL: Knowledge count")
    s = k.search("test")
    if s: passed += 1
    else: failed += 1; print("FAIL: Knowledge search")
except Exception as e:
    failed += 2; print(f"Knowledge Error: {e}")

# 6. Capabilities
try:
    from capabilities import Capabilities
    c = Capabilities()
    if c.count() >= 400: passed += 1
    else: failed += 1; print("FAIL: Capabilities count")
    if "الإحاطة الإمبراطورية" in c.capabilities: passed += 1
    else: failed += 1; print("FAIL: Capabilities key")
except Exception as e:
    failed += 2; print(f"Capabilities Error: {e}")

# 7. Secrets
try:
    from secrets import Secrets
    s = Secrets()
    if s.count() == 800: passed += 1
    else: failed += 1; print("FAIL: Secrets count")
    w = s.whisper()
    if w: passed += 1
    else: failed += 1; print("FAIL: Secrets whisper")
except Exception as e:
    failed += 2; print(f"Secrets Error: {e}")

# 8. Client
try:
    from client import Client
    cl = Client()
    if cl.count() == 25: passed += 1
    else: failed += 1; print("FAIL: Client count")
    if "25" in cl.onboard("X"): passed += 1
    else: failed += 1; print("FAIL: Client onboard")
except Exception as e:
    failed += 2; print(f"Client Error: {e}")

# 9. NoahPrime
try:
    from noah_prime import NoahPrime
    noah = NoahPrime()
    st = noah.status()
    if "80" in st: passed += 1
    else: failed += 1; print("FAIL: Noah status minds")
    if "50" in st: passed += 1
    else: failed += 1; print("FAIL: Noah status shields")
    ans = noah.think("تحليل السوق")
    if ans: passed += 1
    else: failed += 1; print("FAIL: Noah think")
except Exception as e:
    failed += 3; print(f"NoahPrime Error: {e}")

# Report
total = passed + failed
print(f"\n{'='*40}")
print(f"النتيجة: {passed}/{total} نجح | {failed} فشل")
print(f"نسبة النجاح: {passed/total*100:.1f}%")
