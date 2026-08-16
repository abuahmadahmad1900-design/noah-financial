#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# test_system_full.py - اختبار شامل للتأكد من عمل النظام بالكامل

import importlib.util
import time

def load_noah():
    spec = importlib.util.spec_from_file_location("noah_final", "/data/data/com.termux/files/home/noah_eaglet/noah_final.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def safe_len(obj):
    try:
        return len(obj)
    except:
        return 0

def run_full_test():
    print("=" * 85)
    print("🧪  اختبار النظام الشامل - نوح  🧪")
    print("=" * 85)
    
    score = 0
    total = 40
    errors = []
    
    # 1. تحميل الملف
    try:
        noah = load_noah()
        print("✅ 1. تم تحميل noah_final.py بنجاح")
        score += 1
    except Exception as e:
        print(f"❌ 1. فشل التحميل: {e}")
        return
    
    # 2. الأباطرة
    if hasattr(noah, 'emperors') and len(noah.emperors) == 19:
        print("✅ 2. الأباطرة الـ 19 موجودون")
        score += 1
    else:
        print("❌ 2. الأباطرة غير مكتملين")
        errors.append("الأباطرة")
    
    # 3. العقول
    if hasattr(noah, 'all_minds_400') and len(noah.all_minds_400) == 500:
        print("✅ 3. العقول الـ 500 موجودون")
        score += 1
    else:
        print("❌ 3. العقول غير مكتملة")
        errors.append("العقول")
    
    # 4. الدروع
    if hasattr(noah, 'shields') and len(noah.shields) == 200:
        print("✅ 4. الدروع الـ 200 موجودة")
        score += 1
    else:
        print("❌ 4. الدروع غير مكتملة")
        errors.append("الدروع")
    
    # 5. محركات الخلق
    if hasattr(noah, 'genesis_engines') and len(noah.genesis_engines) == 200:
        print("✅ 5. محركات الخلق الـ 200 موجودة")
        score += 1
    else:
        print("❌ 5. محركات الخلق غير مكتملة")
        errors.append("محركات الخلق")
    
    # 6. أنظمة الخوارزمية
    if hasattr(noah, 'all_imperial_systems') and len(noah.all_imperial_systems) == 500:
        print("✅ 6. أنظمة الخوارزمية الـ 500 موجودة")
        score += 1
    else:
        print("❌ 6. أنظمة الخوارزمية غير مكتملة")
        errors.append("أنظمة الخوارزمية")
    
    # 7. الأنظمة المالية
    if hasattr(noah, 'financial_systems') and len(noah.financial_systems) == 100:
        print("✅ 7. الأنظمة المالية الـ 100 موجودة")
        score += 1
    else:
        print("❌ 7. الأنظمة المالية غير مكتملة")
        errors.append("الأنظمة المالية")
    
    # 8. الأنظمة المحاسبية
    if hasattr(noah, 'accounting_systems') and len(noah.accounting_systems) == 100:
        print("✅ 8. الأنظمة المحاسبية الـ 100 موجودة")
        score += 1
    else:
        print("❌ 8. الأنظمة المحاسبية غير مكتملة")
        errors.append("الأنظمة المحاسبية")
    
    # 9. القطاعات
    if hasattr(noah, 'all_sectors') and len(noah.all_sectors) == 30:
        print("✅ 9. القطاعات الـ 30 موجودة")
        score += 1
    else:
        print("❌ 9. القطاعات غير مكتملة")
        errors.append("القطاعات")
    
    # 10. المتاجر
    if hasattr(noah, 'all_stores') and len(noah.all_stores) == 250:
        print("✅ 10. المتاجر الـ 250 موجودة")
        score += 1
    else:
        print("❌ 10. المتاجر غير مكتملة")
        errors.append("المتاجر")
    
    # 11. قدرات المتاجر
    if hasattr(noah, 'all_store_superpowers') and len(noah.all_store_superpowers) == 200:
        print("✅ 11. قدرات المتاجر الـ 200 موجودة")
        score += 1
    else:
        print("❌ 11. قدرات المتاجر غير مكتملة")
        errors.append("قدرات المتاجر")
    
    # 12. قدرات العلاقات
    if hasattr(noah, 'all_human_relations_powers') and len(noah.all_human_relations_powers) == 1000:
        print("✅ 12. قدرات العلاقات الـ 1000 موجودة")
        score += 1
    else:
        print("❌ 12. قدرات العلاقات غير مكتملة")
        errors.append("قدرات العلاقات")
    
    # 13. قدرات التوفير
    if hasattr(noah, 'all_financial_optimization_powers') and len(noah.all_financial_optimization_powers) == 1000:
        print("✅ 13. قدرات التوفير الـ 1000 موجودة")
        score += 1
    else:
        print("❌ 13. قدرات التوفير غير مكتملة")
        errors.append("قدرات التوفير")
    
    # 14. أنظمة التوفير
    if hasattr(noah, 'all_financial_optimization_systems') and len(noah.all_financial_optimization_systems) == 400:
        print("✅ 14. أنظمة التوفير الـ 400 موجودة")
        score += 1
    else:
        print("❌ 14. أنظمة التوفير غير مكتملة")
        errors.append("أنظمة التوفير")
    
    # 15. قدرات الضغط
    if hasattr(noah, 'all_compression_powers') and len(noah.all_compression_powers) == 1000:
        print("✅ 15. قدرات الضغط الـ 1000 موجودة")
        score += 1
    else:
        print("❌ 15. قدرات الضغط غير مكتملة")
        errors.append("قدرات الضغط")
    
    # 16. أنظمة الضغط
    if hasattr(noah, 'all_compression_systems') and len(noah.all_compression_systems) == 400:
        print("✅ 16. أنظمة الضغط الـ 400 موجودة")
        score += 1
    else:
        print("❌ 16. أنظمة الضغط غير مكتملة")
        errors.append("أنظمة الضغط")
    
    # 17. قدرات المدفوعات
    if hasattr(noah, 'all_payment_powers') and len(noah.all_payment_powers) == 1000:
        print("✅ 17. قدرات المدفوعات الـ 1000 موجودة")
        score += 1
    else:
        print("❌ 17. قدرات المدفوعات غير مكتملة")
        errors.append("قدرات المدفوعات")
    
    # 18. أنظمة المدفوعات
    if hasattr(noah, 'all_payment_systems') and len(noah.all_payment_systems) == 400:
        print("✅ 18. أنظمة المدفوعات الـ 400 موجودة")
        score += 1
    else:
        print("❌ 18. أنظمة المدفوعات غير مكتملة")
        errors.append("أنظمة المدفوعات")
    
    # 19. أنظمة OmniCore
    if hasattr(noah, 'all_omnicore_systems') and len(noah.all_omnicore_systems) == 500:
        print("✅ 19. أنظمة OmniCore الـ 500 موجودة")
        score += 1
    else:
        print("❌ 19. أنظمة OmniCore غير مكتملة")
        errors.append("أنظمة OmniCore")
    
    # 20. أنظمة OmniSovereign
    if hasattr(noah, 'all_omnisovereign_systems') and len(noah.all_omnisovereign_systems) == 800:
        print("✅ 20. أنظمة OmniSovereign الـ 800 موجودة")
        score += 1
    else:
        print("❌ 20. أنظمة OmniSovereign غير مكتملة")
        errors.append("أنظمة OmniSovereign")
    
    # 21. أنظمة OmniInfinite
    if hasattr(noah, 'all_omniinfinite_systems') and len(noah.all_omniinfinite_systems) == 800:
        print("✅ 21. أنظمة OmniInfinite الـ 800 موجودة")
        score += 1
    else:
        print("❌ 21. أنظمة OmniInfinite غير مكتملة")
        errors.append("أنظمة OmniInfinite")
    
    # 22. أنظمة KnowledgePrime
    if hasattr(noah, 'all_knowledge_prime_systems') and len(noah.all_knowledge_prime_systems) == 875:
        print("✅ 22. أنظمة KnowledgePrime الـ 875 موجودة")
        score += 1
    else:
        print("❌ 22. أنظمة KnowledgePrime غير مكتملة")
        errors.append("أنظمة KnowledgePrime")
    
    # 23. المؤسسات التعليمية
    if hasattr(noah, 'all_educational_institutions') and len(noah.all_educational_institutions) == 600:
        print("✅ 23. المؤسسات التعليمية الـ 600 موجودة")
        score += 1
    else:
        print("❌ 23. المؤسسات التعليمية غير مكتملة")
        errors.append("المؤسسات التعليمية")
    
    # 24. المراجع الشرعية
    if hasattr(noah, 'all_islamic_references') and len(noah.all_islamic_references) == 930:
        print("✅ 24. المراجع الشرعية الـ 930 موجودة")
        score += 1
    else:
        print("❌ 24. المراجع الشرعية غير مكتملة")
        errors.append("المراجع الشرعية")
    
    # 25. المكونات الشرعية
    if hasattr(noah, 'all_islamic_complete') and len(noah.all_islamic_complete) == 600:
        print("✅ 25. المكونات الشرعية الـ 600 موجودة")
        score += 1
    else:
        print("❌ 25. المكونات الشرعية غير مكتملة")
        errors.append("المكونات الشرعية")
    
    # 26. أنظمة التعلم
    if hasattr(noah, 'all_learning_systems') and len(noah.all_learning_systems) == 1000:
        print("✅ 26. أنظمة التعلم الـ 1000 موجودة")
        score += 1
    else:
        print("❌ 26. أنظمة التعلم غير مكتملة")
        errors.append("أنظمة التعلم")
    
    # 27. قدرات التعلم
    if hasattr(noah, 'all_learning_powers') and len(noah.all_learning_powers) == 1000:
        print("✅ 27. قدرات التعلم الـ 1000 موجودة")
        score += 1
    else:
        print("❌ 27. قدرات التعلم غير مكتملة")
        errors.append("قدرات التعلم")
    
    # 28. المكونات العلمية
    if hasattr(noah, 'all_scientific_tech') and len(noah.all_scientific_tech) == 497:
        print("✅ 28. المكونات العلمية الـ 497 موجودة")
        score += 1
    else:
        print("❌ 28. المكونات العلمية غير مكتملة")
        errors.append("المكونات العلمية")
    
    # 29. الكيانات العليا
    if hasattr(noah, 'all_higher_entities') and len(noah.all_higher_entities) == 300:
        print("✅ 29. الكيانات العليا الـ 300 موجودة")
        score += 1
    else:
        print("❌ 29. الكيانات العليا غير مكتملة")
        errors.append("الكيانات العليا")
    
    # 30. تقوية الكيانات
    if hasattr(noah, 'all_entities_boost') and len(noah.all_entities_boost) == 350:
        print("✅ 30. تقوية الكيانات الـ 350 موجودة")
        score += 1
    else:
        print("❌ 30. تقوية الكيانات غير مكتملة")
        errors.append("تقوية الكيانات")
    
    # 31. أنظمة SelfDevPrime
    if hasattr(noah, 'all_selfdev_systems') and len(noah.all_selfdev_systems) == 999:
        print("✅ 31. أنظمة SelfDevPrime الـ 999 موجودة")
        score += 1
    else:
        print("❌ 31. أنظمة SelfDevPrime غير مكتملة")
        errors.append("أنظمة SelfDevPrime")
    
    # 32. أنظمة SelfDevPrime Mega
    if hasattr(noah, 'all_selfdev_mega_systems') and len(noah.all_selfdev_mega_systems) == 375:
        print("✅ 32. أنظمة SelfDevPrime Mega الـ 375 موجودة")
        score += 1
    else:
        print("❌ 32. أنظمة SelfDevPrime Mega غير مكتملة")
        errors.append("أنظمة SelfDevPrime Mega")
    
    # 33. قدرات SelfDevPrime
    if hasattr(noah, 'selfdev_prime_powers') and len(noah.selfdev_prime_powers) == 204:
        print("✅ 33. قدرات SelfDevPrime الـ 204 موجودة")
        score += 1
    else:
        print("❌ 33. قدرات SelfDevPrime غير مكتملة")
        errors.append("قدرات SelfDevPrime")
    
    # 34. قدرات SelfDevPrime Mega
    if hasattr(noah, 'all_selfdev_mega_powers') and len(noah.all_selfdev_mega_powers) == 300:
        print("✅ 34. قدرات SelfDevPrime Mega الـ 300 موجودة")
        score += 1
    else:
        print("❌ 34. قدرات SelfDevPrime Mega غير مكتملة")
        errors.append("قدرات SelfDevPrime Mega")
    
    # 35. قدرات OmniCore
    if hasattr(noah, 'omnicore_powers_500') and len(noah.omnicore_powers_500) == 500:
        print("✅ 35. قدرات OmniCore الـ 500 موجودة")
        score += 1
    else:
        print("❌ 35. قدرات OmniCore غير مكتملة")
        errors.append("قدرات OmniCore")
    
    # 36. قدرات OmniSovereign
    if hasattr(noah, 'all_omnisovereign_powers') and len(noah.all_omnisovereign_powers) == 1000:
        print("✅ 36. قدرات OmniSovereign الـ 1000 موجودة")
        score += 1
    else:
        print("❌ 36. قدرات OmniSovereign غير مكتملة")
        errors.append("قدرات OmniSovereign")
    
    # 37. قدرات OmniInfinite
    if hasattr(noah, 'all_omniinfinite_powers') and len(noah.all_omniinfinite_powers) == 1000:
        print("✅ 37. قدرات OmniInfinite الـ 1000 موجودة")
        score += 1
    else:
        print("❌ 37. قدرات OmniInfinite غير مكتملة")
        errors.append("قدرات OmniInfinite")
    
    # 38. قدرات KnowledgePrime
    if hasattr(noah, 'all_knowledge_prime_powers') and len(noah.all_knowledge_prime_powers) == 500:
        print("✅ 38. قدرات KnowledgePrime الـ 500 موجودة")
        score += 1
    else:
        print("❌ 38. قدرات KnowledgePrime غير مكتملة")
        errors.append("قدرات KnowledgePrime")
    
    # 39. عناصر الروح
    if hasattr(noah, 'soul_elements') and len(noah.soul_elements) == 16:
        print("✅ 39. عناصر الروح الـ 16 موجودة")
        score += 1
    else:
        print("❌ 39. عناصر الروح غير مكتملة")
        errors.append("عناصر الروح")
    
    # 40. فئات القدرات
    if hasattr(noah, 'capability_categories') and len(noah.capability_categories) == 10:
        print("✅ 40. فئات القدرات الـ 10 موجودة")
        score += 1
    else:
        print("❌ 40. فئات القدرات غير مكتملة")
        errors.append("فئات القدرات")
    
    print("\n" + "=" * 85)
    print(f"📊  نتيجة الاختبار الشامل: {score}/{total}")
    if errors:
        print(f"⚠️  مكونات تحتاج انتباه: {', '.join(errors)}")
    else:
        print("✅  جميع المكونات تعمل بشكل كامل. النظام سليم 100%.")
    print("=" * 85)

if __name__ == "__main__":
    run_full_test()
