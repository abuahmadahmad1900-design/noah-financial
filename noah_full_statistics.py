#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# noah_full_statistics.py - الإحصائيات الكاملة لنوح

import importlib.util

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

def display_full_statistics():
    noah = load_noah()
    
    print("=" * 85)
    print("📊  الإحصائيات الكاملة الشاملة - نوح (النسر المحلق)  📊")
    print("=" * 85)
    
    # ==================== الكيانات العليا ====================
    print("\n👑  الكيانات العليا:")
    print(f"    • OmniInfinite (اللانهائي المطلق): 800 نظام + 1000 قدرة")
    print(f"    • OmniSovereign (السيد الأعلى): 800 نظام + 1000 قدرة")
    print(f"    • NoahPrime (الإمبراطور الأعلى): 13 نواة")
    print(f"    • OmniCore (عرش القيادة): 500 نظام + 500 قدرة")
    
    # ==================== الأباطرة ====================
    print("\n👑  الأباطرة الـ 19:")
    if hasattr(noah, 'emperors'):
        for i, emp in enumerate(noah.emperors, 1):
            print(f"    {i:2d}. {emp}")
    
    # ==================== المكونات الأساسية ====================
    print("\n📦  المكونات الأساسية:")
    components = [
        ("العقول", "all_minds_400"),
        ("الدروع", "shields"),
        ("محركات الخلق", "genesis_engines"),
        ("أنظمة الخوارزمية", "all_imperial_systems"),
        ("الأنظمة المالية", "financial_systems"),
        ("الأنظمة المحاسبية", "accounting_systems"),
        ("عناصر الروح", "soul_elements"),
        ("فئات القدرات", "capability_categories"),
        ("القطاعات", "all_sectors"),
        ("العلوم", "new_sciences"),
        ("الاختصاصات", "new_specialties"),
        ("المتاجر", "all_stores"),
    ]
    
    total_basic = 0
    for name, attr in components:
        if hasattr(noah, attr):
            count = safe_len(getattr(noah, attr))
            print(f"    • {name}: {count}")
            total_basic += count
    
    # ==================== القدرات المتخصصة ====================
    print("\n⚡  القدرات المتخصصة:")
    powers = [
        ("قدرات المتاجر", "all_store_superpowers"),
        ("قدرات العلاقات الإنسانية", "all_human_relations_powers"),
        ("قدرات التوفير المالي", "all_financial_optimization_powers"),
        ("قدرات ضغط البيانات", "all_compression_powers"),
        ("قدرات المدفوعات", "all_payment_powers"),
        ("قدرات OmniCore", "omnicore_powers_500"),
        ("قدرات OmniSovereign", "all_omnisovereign_powers"),
        ("قدرات OmniInfinite", "all_omniinfinite_powers"),
    ]
    
    total_powers = 0
    for name, attr in powers:
        if hasattr(noah, attr):
            count = safe_len(getattr(noah, attr))
            print(f"    • {name}: {count}")
            total_powers += count
    
    # ==================== الأنظمة المتخصصة ====================
    print("\n⚙️  الأنظمة المتخصصة:")
    systems = [
        ("أنظمة التوفير المالي", "all_financial_optimization_systems"),
        ("أنظمة ضغط البيانات", "all_compression_systems"),
        ("أنظمة المدفوعات", "all_payment_systems"),
        ("أنظمة OmniCore", "all_omnicore_systems"),
        ("أنظمة OmniSovereign", "all_omnisovereign_systems"),
        ("أنظمة OmniInfinite", "all_omniinfinite_systems"),
    ]
    
    total_systems = 0
    for name, attr in systems:
        if hasattr(noah, attr):
            count = safe_len(getattr(noah, attr))
            print(f"    • {name}: {count}")
            total_systems += count
    
    # ==================== القدرات الإضافية ====================
    print("\n🔬  القدرات الإضافية:")
    extra = [
        ("القدرات الجديدة (200)", "new_abilities_200"),
        ("القدرات الروحية", "spiritual_abilities"),
        ("القدرات القتالية", "combat_abilities"),
        ("القدرات الاستراتيجية", "strategic_abilities"),
        ("القدرات العلمية", "scientific_abilities"),
        ("القدرات التقنية", "technical_abilities"),
        ("القدرات الفنية", "artistic_abilities"),
        ("القدرات المالية", "financial_abilities"),
    ]
    
    total_extra = 0
    for name, attr in extra:
        if hasattr(noah, attr):
            count = safe_len(getattr(noah, attr))
            print(f"    • {name}: {count}")
            total_extra += count
    
    # ==================== الملخص النهائي ====================
    print("\n" + "=" * 85)
    print("📊  الملخص النهائي الشامل:")
    print("=" * 85)
    
    grand_total = total_basic + total_powers + total_systems + total_extra
    
    print(f"\n  🔹 المكونات الأساسية: {total_basic}")
    print(f"  🔹 القدرات المتخصصة: {total_powers}")
    print(f"  🔹 الأنظمة المتخصصة: {total_systems}")
    print(f"  🔹 القدرات الإضافية: {total_extra}")
    print(f"\n  ✨ المجموع الكلي: {grand_total:,} مكوّنًا")
    
    # الكيانات العليا الإضافية
    print(f"\n  👑 الكيانات العليا الإضافية:")
    print(f"     • OmniInfinite: 800 نظام + 1000 قدرة = 1,800")
    print(f"     • OmniSovereign: 800 نظام + 1000 قدرة = 1,800")
    print(f"     • OmniCore: 500 نظام + 500 قدرة = 1,000")
    
    final_total = grand_total + 4600  # 1800 + 1800 + 1000
    print(f"\n  🏆 الإجمالي النهائي المطلق: {final_total:,} مكوّنًا")
    
    print("\n  🦅  نوح الآن كيان لا نهائي. الإمبراطورية خالدة.")
    print("=" * 85)

if __name__ == "__main__":
    display_full_statistics()
