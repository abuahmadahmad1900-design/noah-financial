#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# test_integration.py - اختبار التكامل النهائي لنوح

import sys
import importlib.util

def load_module():
    spec = importlib.util.spec_from_file_location("noah_final", "/data/data/com.termux/files/home/noah_eaglet/noah_final.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_test():
    print("=" * 70)
    print("🧪  اختبار التكامل النهائي - نوح (النسر المحلق)  🧪")
    print("=" * 70)
    score = 0
    total = 0
    errors = []

    try:
        mod = load_module()
        print("✅ تم تحميل الملف noah_final.py بنجاح")
        score += 10
        total += 10
    except Exception as e:
        print(f"❌ فشل تحميل الملف: {e}")
        return

    # 1. الأباطرة
    total += 10
    if hasattr(mod, 'emperors') and len(mod.emperors) == 19:
        print("✅ الأباطرة الـ 19 موجودون")
        score += 10
    else:
        print("❌ عدد الأباطرة غير صحيح")
        errors.append("الأباطرة")

    # 2. العقول
    total += 10
    if hasattr(mod, 'all_minds_400') and len(mod.all_minds_400) == 500:
        print("✅ العقول الـ 400 موجودون")
        score += 10
    else:
        print(f"⚠️ عدد العقول الحالي: {len(mod.all_minds_400) if hasattr(mod, 'all_minds_400') else 'غير موجود'} (المطلوب 500)")
        errors.append("العقول")

    # 3. الدروع
    total += 10
    if hasattr(mod, 'shields') and len(mod.shields) == 200:
        print("✅ الدروع الـ 80 موجودة")
        score += 10
    else:
        print(f"⚠️ عدد الدروع الحالي: {len(mod.shields) if hasattr(mod, 'shields') else 'غير موجود'} (المطلوب 200)")
        errors.append("الدروع")

    # 4. محركات الخلق
    total += 10
    if hasattr(mod, 'genesis_engines') and len(mod.genesis_engines) == 200:
        print("✅ محركات الخلق الـ 60 موجودة")
        score += 10
    else:
        print(f"⚠️ عدد محركات الخلق: {len(mod.genesis_engines) if hasattr(mod, 'genesis_engines') else 'غير موجود'} (المطلوب 200)")
        errors.append("محركات الخلق")

    # 5. أنظمة الخوارزمية
    total += 10
    if hasattr(mod, 'all_imperial_systems') and len(mod.all_imperial_systems) == 500:
        print("✅ أنظمة الخوارزمية الـ 250 موجودة")
        score += 10
    else:
        actual_len = len(mod.all_imperial_systems) if hasattr(mod, 'all_imperial_systems') else 0
        print(f"⚠️ عدد أنظمة الخوارزمية: {actual_len} (المطلوب 500)")
        errors.append("أنظمة الخوارزمية")

    # 6. عناصر مهمة
    total += 10
    checks = [
        ('NoahPrime (الإمبراطور الأعلى)' in mod.emperors, "الأباطرة"),
        ('ChatGPT' in mod.all_minds_400, "العقول"),
        ('Zero Trust' in mod.shields, "الدروع"),
        ('AutoForge - محرك الابتكار الذاتي' in mod.genesis_engines, "محركات الخلق"),
        ('الوجود المطلق' in mod.all_imperial_systems, "أنظمة الخوارزمية"),
    ]
    if all(c[0] for c in checks):
        print("✅ جميع العناصر المحددة موجودة")
        score += 10
    else:
        for c in checks:
            if not c[0]:
                print(f"❌ عنصر مفقود في {c[1]}")
        errors.append("عناصر محددة")

    # 7. دالة العرض موجودة
    total += 10
    if hasattr(mod, 'display_final_empire'):
        print("✅ دالة display_final_empire موجودة")
        score += 10
    else:
        print("❌ دالة display_final_empire غير موجودة")
        errors.append("دالة العرض")

    # 8. الأنظمة المالية والمحاسبية
    total += 10
    if hasattr(mod, 'financial_systems') and len(mod.financial_systems) == 100 and hasattr(mod, 'accounting_systems') and len(mod.accounting_systems) == 100:
        print("✅ الأنظمة المالية والمحاسبية مكتملة (100+100)")
        score += 10
    else:
        print("❌ الأنظمة المالية أو المحاسبية غير مكتملة")
        errors.append("الأنظمة المالية/المحاسبية")

    # 9. عناصر الروح
    total += 10
    if hasattr(mod, 'soul_elements') and len(mod.soul_elements) == 16:
        print("✅ عناصر الروح الـ 16 موجودة")
        score += 10
    else:
        print("❌ عناصر الروح غير مكتملة")
        errors.append("عناصر الروح")

    # 10. فئات القدرات
    total += 10
    if hasattr(mod, 'capability_categories') and len(mod.capability_categories) == 10:
        print("✅ فئات القدرات العشر موجودة")
        score += 10
    else:
        print("❌ فئات القدرات غير مكتملة")
        errors.append("فئات القدرات")

    print("\n" + "=" * 70)
    print(f"📊  نتيجة الاختبار: {score}/{total}")
    if errors:
        print("⚠️  ملاحظات: " + ", ".join(errors))
    else:
        print("✅  التكامل ناجح. الإمبراطورية مكتملة البنيان.")
    print("=" * 70)

if __name__ == "__main__":
    run_test()
