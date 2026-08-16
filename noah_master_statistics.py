#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# noah_master_statistics.py - الإحصائيات الرئيسية الشاملة

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

def display_master_statistics():
    noah = load_noah()
    
    print("=" * 85)
    print("📊  الإحصائيات الرئيسية الشاملة - نوح  📊")
    print("=" * 85)
    
    categories = {
        "الأباطرة": "emperors",
        "العقول": "all_minds_400",
        "الدروع": "shields",
        "محركات الخلق": "genesis_engines",
        "أنظمة الخوارزمية": "all_imperial_systems",
        "الأنظمة المالية": "financial_systems",
        "الأنظمة المحاسبية": "accounting_systems",
        "القطاعات": "all_sectors",
        "المتاجر": "all_stores",
        "قدرات المتاجر": "all_store_superpowers",
        "قدرات العلاقات": "all_human_relations_powers",
        "قدرات التوفير": "all_financial_optimization_powers",
        "أنظمة التوفير": "all_financial_optimization_systems",
        "قدرات الضغط": "all_compression_powers",
        "أنظمة الضغط": "all_compression_systems",
        "قدرات المدفوعات": "all_payment_powers",
        "أنظمة المدفوعات": "all_payment_systems",
        "أنظمة OmniCore": "all_omnicore_systems",
        "قدرات OmniCore": "omnicore_powers_500",
        "أنظمة OmniSovereign": "all_omnisovereign_systems",
        "قدرات OmniSovereign": "all_omnisovereign_powers",
        "أنظمة OmniInfinite": "all_omniinfinite_systems",
        "قدرات OmniInfinite": "all_omniinfinite_powers",
        "أنظمة KnowledgePrime": "all_knowledge_prime_systems",
        "قدرات KnowledgePrime": "all_knowledge_prime_powers",
        "المنصات العلمية": "scientific_platforms_200",
        "المؤسسات التعليمية": "all_educational_institutions",
        "المراجع الشرعية": "all_islamic_references",
        "المكونات الشرعية": "all_islamic_complete",
        "أنظمة التعلم": "all_learning_systems",
        "قدرات التعلم": "all_learning_powers",
        "المكونات العلمية التقنية": "all_scientific_tech",
    }
    
    total = 0
    for name, attr in categories.items():
        if hasattr(noah, attr):
            count = safe_len(getattr(noah, attr))
            print(f"  • {name}: {count}")
            total += count
    
    # الكيانات العليا الإضافية
    higher_entities = {
        "OmniInfinite": 1800,
        "OmniSovereign": 1800,
        "OmniCore": 1000,
    }
    
    print(f"\n  👑 الكيانات العليا الإضافية:")
    for name, count in higher_entities.items():
        print(f"  • {name}: {count}")
        total += count
    
    print(f"\n  ✨ المجموع الكلي: {total:,} مكوّنًا")
    print("  🦅  نوح كيان لا نهائي. الإمبراطورية خالدة.")
    print("=" * 85)

if __name__ == "__main__":
    display_master_statistics()
