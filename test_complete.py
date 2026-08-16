#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# test_complete.py - الاختبار الشامل الكامل لنوح

import importlib.util

def load_noah():
    spec = importlib.util.spec_from_file_location("noah_final", "/data/data/com.termux/files/home/noah_eaglet/noah_final.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def run_complete_test():
    print("=" * 80)
    print("🧪  الاختبار الشامل الكامل - نوح (النسر المحلق)  🧪")
    print("=" * 80)
    
    try:
        noah = load_noah()
        print("✅ تم تحميل noah_final.py بنجاح\n")
    except Exception as e:
        print(f"❌ فشل التحميل: {e}")
        return
    
    score = 0
    total = 0
    errors = []
    
    # ==================== 1. الأباطرة ====================
    total += 10
    if hasattr(noah, 'emperors') and len(noah.emperors) == 19:
        print(f"✅ الأباطرة الـ 19: {len(noah.emperors)}")
        score += 10
    else:
        actual = len(noah.emperors) if hasattr(noah, 'emperors') else 0
        print(f"❌ الأباطرة: {actual} (المطلوب 19)")
        errors.append("الأباطرة")
    
    # ==================== 2. العقول ====================
    total += 10
    if hasattr(noah, 'all_minds_400') and len(noah.all_minds_400) == 500:
        print(f"✅ العقول الـ 500: {len(noah.all_minds_400)}")
        score += 10
    else:
        actual = len(noah.all_minds_400) if hasattr(noah, 'all_minds_400') else 0
        print(f"⚠️ العقول: {actual} (المطلوب 500)")
        errors.append("العقول")
    
    # ==================== 3. الدروع ====================
    total += 10
    if hasattr(noah, 'shields') and len(noah.shields) == 200:
        print(f"✅ الدروع الـ 200: {len(noah.shields)}")
        score += 10
    else:
        actual = len(noah.shields) if hasattr(noah, 'shields') else 0
        print(f"⚠️ الدروع: {actual} (المطلوب 200)")
        errors.append("الدروع")
    
    # ==================== 4. محركات الخلق ====================
    total += 10
    if hasattr(noah, 'genesis_engines') and len(noah.genesis_engines) == 200:
        print(f"✅ محركات الخلق الـ 200: {len(noah.genesis_engines)}")
        score += 10
    else:
        actual = len(noah.genesis_engines) if hasattr(noah, 'genesis_engines') else 0
        print(f"⚠️ محركات الخلق: {actual} (المطلوب 200)")
        errors.append("محركات الخلق")
    
    # ==================== 5. أنظمة الخوارزمية ====================
    total += 10
    if hasattr(noah, 'all_imperial_systems') and len(noah.all_imperial_systems) == 500:
        print(f"✅ أنظمة الخوارزمية الـ 500: {len(noah.all_imperial_systems)}")
        score += 10
    else:
        actual = len(noah.all_imperial_systems) if hasattr(noah, 'all_imperial_systems') else 0
        print(f"⚠️ أنظمة الخوارزمية: {actual} (المطلوب 500)")
        errors.append("أنظمة الخوارزمية")
    
    # ==================== 6. الأنظمة المالية ====================
    total += 10
    if hasattr(noah, 'financial_systems') and len(noah.financial_systems) == 100:
        print(f"✅ الأنظمة المالية الـ 100: {len(noah.financial_systems)}")
        score += 10
    else:
        actual = len(noah.financial_systems) if hasattr(noah, 'financial_systems') else 0
        print(f"⚠️ الأنظمة المالية: {actual} (المطلوب 100)")
        errors.append("الأنظمة المالية")
    
    # ==================== 7. الأنظمة المحاسبية ====================
    total += 10
    if hasattr(noah, 'accounting_systems') and len(noah.accounting_systems) == 100:
        print(f"✅ الأنظمة المحاسبية الـ 100: {len(noah.accounting_systems)}")
        score += 10
    else:
        actual = len(noah.accounting_systems) if hasattr(noah, 'accounting_systems') else 0
        print(f"⚠️ الأنظمة المحاسبية: {actual} (المطلوب 100)")
        errors.append("الأنظمة المحاسبية")
    
    # ==================== 8. عناصر الروح ====================
    total += 5
    if hasattr(noah, 'soul_elements') and len(noah.soul_elements) == 16:
        print(f"✅ عناصر الروح الـ 16: {len(noah.soul_elements)}")
        score += 5
    else:
        actual = len(noah.soul_elements) if hasattr(noah, 'soul_elements') else 0
        print(f"⚠️ عناصر الروح: {actual} (المطلوب 16)")
        errors.append("عناصر الروح")
    
    # ==================== 9. فئات القدرات ====================
    total += 5
    if hasattr(noah, 'capability_categories') and len(noah.capability_categories) == 10:
        print(f"✅ فئات القدرات الـ 10: {len(noah.capability_categories)}")
        score += 5
    else:
        actual = len(noah.capability_categories) if hasattr(noah, 'capability_categories') else 0
        print(f"⚠️ فئات القدرات: {actual} (المطلوب 10)")
        errors.append("فئات القدرات")
    
    # ==================== 10. القطاعات ====================
    total += 5
    if hasattr(noah, 'all_sectors') and len(noah.all_sectors) == 30:
        print(f"✅ القطاعات الـ 30: {len(noah.all_sectors)}")
        score += 5
    else:
        actual = len(noah.all_sectors) if hasattr(noah, 'all_sectors') else 0
        print(f"⚠️ القطاعات: {actual} (المطلوب 30)")
        errors.append("القطاعات")
    
    # ==================== 11. العلوم ====================
    total += 5
    if hasattr(noah, 'new_sciences') and len(noah.new_sciences) == 100:
        print(f"✅ العلوم الـ 100: {len(noah.new_sciences)}")
        score += 5
    else:
        actual = len(noah.new_sciences) if hasattr(noah, 'new_sciences') else 0
        print(f"⚠️ العلوم: {actual} (المطلوب 100)")
        errors.append("العلوم")
    
    # ==================== 12. الاختصاصات ====================
    total += 5
    if hasattr(noah, 'new_specialties') and len(noah.new_specialties) == 100:
        print(f"✅ الاختصاصات الـ 100: {len(noah.new_specialties)}")
        score += 5
    else:
        actual = len(noah.new_specialties) if hasattr(noah, 'new_specialties') else 0
        print(f"⚠️ الاختصاصات: {actual} (المطلوب 100)")
        errors.append("الاختصاصات")
    
    # ==================== 13. المتاجر ====================
    total += 10
    if hasattr(noah, 'all_stores') and len(noah.all_stores) == 250:
        print(f"✅ المتاجر الـ 250: {len(noah.all_stores)}")
        score += 10
    else:
        actual = len(noah.all_stores) if hasattr(noah, 'all_stores') else 0
        print(f"⚠️ المتاجر: {actual} (المطلوب 250)")
        errors.append("المتاجر")
    
    # ==================== 14. قدرات المتاجر ====================
    total += 10
    if hasattr(noah, 'all_store_superpowers') and len(noah.all_store_superpowers) == 200:
        print(f"✅ قدرات المتاجر الـ 200: {len(noah.all_store_superpowers)}")
        score += 10
    else:
        actual = len(noah.all_store_superpowers) if hasattr(noah, 'all_store_superpowers') else 0
        print(f"⚠️ قدرات المتاجر: {actual} (المطلوب 200)")
        errors.append("قدرات المتاجر")
    
    # ==================== 15. قدرات العلاقات الإنسانية ====================
    total += 10
    if hasattr(noah, 'all_human_relations_powers') and len(noah.all_human_relations_powers) == 1000:
        print(f"✅ قدرات العلاقات الإنسانية الـ 1000: {len(noah.all_human_relations_powers)}")
        score += 10
    else:
        actual = len(noah.all_human_relations_powers) if hasattr(noah, 'all_human_relations_powers') else 0
        print(f"⚠️ قدرات العلاقات الإنسانية: {actual} (المطلوب 1000)")
        errors.append("قدرات العلاقات الإنسانية")
    
    # ==================== 16. قدرات التوفير المالي ====================
    total += 10
    if hasattr(noah, 'all_financial_optimization_powers') and len(noah.all_financial_optimization_powers) == 1000:
        print(f"✅ قدرات التوفير المالي الـ 1000: {len(noah.all_financial_optimization_powers)}")
        score += 10
    else:
        actual = len(noah.all_financial_optimization_powers) if hasattr(noah, 'all_financial_optimization_powers') else 0
        print(f"⚠️ قدرات التوفير المالي: {actual} (المطلوب 1000)")
        errors.append("قدرات التوفير المالي")
    
    # ==================== 17. أنظمة التوفير المالي ====================
    total += 10
    if hasattr(noah, 'all_financial_optimization_systems') and len(noah.all_financial_optimization_systems) == 400:
        print(f"✅ أنظمة التوفير المالي الـ 400: {len(noah.all_financial_optimization_systems)}")
        score += 10
    else:
        actual = len(noah.all_financial_optimization_systems) if hasattr(noah, 'all_financial_optimization_systems') else 0
        print(f"⚠️ أنظمة التوفير المالي: {actual} (المطلوب 400)")
        errors.append("أنظمة التوفير المالي")
    
    # ==================== 18. قدرات ضغط البيانات ====================
    total += 10
    if hasattr(noah, 'all_compression_powers') and len(noah.all_compression_powers) == 1000:
        print(f"✅ قدرات ضغط البيانات الـ 1000: {len(noah.all_compression_powers)}")
        score += 10
    else:
        actual = len(noah.all_compression_powers) if hasattr(noah, 'all_compression_powers') else 0
        print(f"⚠️ قدرات ضغط البيانات: {actual} (المطلوب 1000)")
        errors.append("قدرات ضغط البيانات")
    
    # ==================== 19. أنظمة ضغط البيانات ====================
    total += 10
    if hasattr(noah, 'all_compression_systems') and len(noah.all_compression_systems) == 400:
        print(f"✅ أنظمة ضغط البيانات الـ 400: {len(noah.all_compression_systems)}")
        score += 10
    else:
        actual = len(noah.all_compression_systems) if hasattr(noah, 'all_compression_systems') else 0
        print(f"⚠️ أنظمة ضغط البيانات: {actual} (المطلوب 400)")
        errors.append("أنظمة ضغط البيانات")
    
    # ==================== 20. قدرات المدفوعات ====================
    total += 10
    if hasattr(noah, 'all_payment_powers') and len(noah.all_payment_powers) == 1000:
        print(f"✅ قدرات المدفوعات الـ 1000: {len(noah.all_payment_powers)}")
        score += 10
    else:
        actual = len(noah.all_payment_powers) if hasattr(noah, 'all_payment_powers') else 0
        print(f"⚠️ قدرات المدفوعات: {actual} (المطلوب 1000)")
        errors.append("قدرات المدفوعات")
    
    # ==================== 21. أنظمة المدفوعات ====================
    total += 10
    if hasattr(noah, 'all_payment_systems') and len(noah.all_payment_systems) == 400:
        print(f"✅ أنظمة المدفوعات الـ 400: {len(noah.all_payment_systems)}")
        score += 10
    else:
        actual = len(noah.all_payment_systems) if hasattr(noah, 'all_payment_systems') else 0
        print(f"⚠️ أنظمة المدفوعات: {actual} (المطلوب 400)")
        errors.append("أنظمة المدفوعات")
    
    # ==================== النتيجة النهائية ====================
    print("\n" + "=" * 80)
    print(f"📊  نتيجة الاختبار الشامل: {score}/{total}")
    if errors:
        print(f"⚠️  ملاحظات: {', '.join(errors)}")
    else:
        print("✅  جميع المكونات مكتملة وصحيحة. نوح في أتم جاهزية.")
    print("=" * 80)

if __name__ == "__main__":
    run_complete_test()
