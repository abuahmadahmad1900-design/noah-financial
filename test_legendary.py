#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# test_legendary.py - الاختبار الأسطوري النهائي (نسخة كاملة)

import importlib.util
import random

def load_noah():
    spec = importlib.util.spec_from_file_location("noah_final", "/data/data/com.termux/files/home/noah_eaglet/noah_final.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class LegendaryTest:
    def __init__(self):
        self.noah = None
        self.score = 0
        self.total = 600
        self.results = {}
    
    def load(self):
        try:
            self.noah = load_noah()
            return True
        except:
            return False
    
    def check(self, name, condition, points=20):
        if condition:
            self.results[name] = points
            self.score += points
            return True
        self.results[name] = 0
        return False
    
    def run_all(self):
        print("=" * 80)
        print("🧪  الاختبار الأسطوري النهائي - نوح (النسر المحلق)  🧪")
        print("=" * 80)
        print("\n🔛 بدء الاختبار الشامل...\n")
        
        if not self.load():
            print("❌ فشل تحميل noah_final.py")
            return
        
        # 30 فئة × 20 نقطة = 600 نقطة
        tests = [
            ("الأباطرة الـ 19", hasattr(self.noah, 'emperors') and len(self.noah.emperors) == 19),
            ("العقول الـ 500", hasattr(self.noah, 'all_minds_400') and len(self.noah.all_minds_400) == 500),
            ("الدروع الـ 200", hasattr(self.noah, 'shields') and len(self.noah.shields) == 200),
            ("محركات الخلق الـ 200", hasattr(self.noah, 'genesis_engines') and len(self.noah.genesis_engines) == 200),
            ("أنظمة الخوارزمية الـ 500", hasattr(self.noah, 'all_imperial_systems') and len(self.noah.all_imperial_systems) == 500),
            ("الأنظمة المالية الـ 100", hasattr(self.noah, 'financial_systems') and len(self.noah.financial_systems) == 100),
            ("الأنظمة المحاسبية الـ 100", hasattr(self.noah, 'accounting_systems') and len(self.noah.accounting_systems) == 100),
            ("عناصر الروح الـ 16", hasattr(self.noah, 'soul_elements') and len(self.noah.soul_elements) == 16),
            ("فئات القدرات الـ 10", hasattr(self.noah, 'capability_categories') and len(self.noah.capability_categories) == 10),
            ("القطاعات الـ 30", hasattr(self.noah, 'all_sectors') and len(self.noah.all_sectors) == 30),
            ("العلوم الـ 100", hasattr(self.noah, 'new_sciences') and len(self.noah.new_sciences) == 100),
            ("الاختصاصات الـ 100", hasattr(self.noah, 'new_specialties') and len(self.noah.new_specialties) == 100),
            ("المتاجر الـ 250", hasattr(self.noah, 'all_stores') and len(self.noah.all_stores) == 250),
            ("قدرات المتاجر الـ 200", hasattr(self.noah, 'all_store_superpowers') and len(self.noah.all_store_superpowers) == 200),
            ("العلاقات الإنسانية الـ 1000", hasattr(self.noah, 'all_human_relations_powers') and len(self.noah.all_human_relations_powers) == 1000),
            ("التوفير المالي الـ 1000", hasattr(self.noah, 'all_financial_optimization_powers') and len(self.noah.all_financial_optimization_powers) == 1000),
            ("أنظمة التوفير الـ 400", hasattr(self.noah, 'all_financial_optimization_systems') and len(self.noah.all_financial_optimization_systems) == 400),
            ("ضغط البيانات الـ 1000", hasattr(self.noah, 'all_compression_powers') and len(self.noah.all_compression_powers) == 1000),
            ("أنظمة الضغط الـ 400", hasattr(self.noah, 'all_compression_systems') and len(self.noah.all_compression_systems) == 400),
            ("المدفوعات الـ 1000", hasattr(self.noah, 'all_payment_powers') and len(self.noah.all_payment_powers) == 1000),
            ("أنظمة المدفوعات الـ 400", hasattr(self.noah, 'all_payment_systems') and len(self.noah.all_payment_systems) == 400),
            ("التكامل الشامل", hasattr(self.noah, 'emperors') and hasattr(self.noah, 'all_minds_400') and hasattr(self.noah, 'shields')),
            ("المرونة", hasattr(self.noah, 'genesis_engines') and len(self.noah.genesis_engines) > 0),
            ("الشمولية", hasattr(self.noah, 'all_sectors') and len(self.noah.all_sectors) > 20),
            ("العمق", hasattr(self.noah, 'all_human_relations_powers') and len(self.noah.all_human_relations_powers) > 900),
            ("الترابط", hasattr(self.noah, 'all_stores') and hasattr(self.noah, 'all_payment_systems')),
            ("التنوع", hasattr(self.noah, 'new_sciences') and hasattr(self.noah, 'new_specialties')),
            ("الاكتمال", hasattr(self.noah, 'soul_elements') and hasattr(self.noah, 'capability_categories')),
            ("القوة", hasattr(self.noah, 'all_compression_systems') and len(self.noah.all_compression_systems) > 300),
            ("الذكاء", hasattr(self.noah, 'all_store_superpowers') and len(self.noah.all_store_superpowers) > 150),
        ]
        
        for name, condition in tests:
            if self.check(name, condition):
                print(f"✅ {name}")
            else:
                print(f"❌ {name}")
        
        print("\n" + "=" * 80)
        print("📊  النتيجة النهائية للاختبار الأسطوري:")
        print("=" * 80)
        for key, val in self.results.items():
            if val > 0:
                print(f"    • {key}: {val} نقطة")
        print(f"\n    🏆 المجموع: {self.score}/{self.total}")
        
        percentage = (self.score / self.total) * 100
        print(f"    📈 النسبة: {percentage:.1f}%")
        
        if percentage == 100:
            print("\n    🦅  نوح أسطوري! كامل بلا نقصان!")
        elif percentage >= 90:
            print("\n    🦅  نوح أسطوري! لا يُقهر ولا يُوصف!")
        elif percentage >= 70:
            print("\n    🦅  نوح قوي جدًا!")
        else:
            print("\n    ⚠️  نوح يحتاج إلى تقوية.")
        
        print("=" * 80)

if __name__ == "__main__":
    test = LegendaryTest()
    test.run_all()
