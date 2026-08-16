#!/usr/bin/env python3
# -*- coding: utf-8 -*-

emperors = [
    "NoahPrime (الإمبراطور الأعلى)",
    "OmniCore (عرش القيادة)",
    "NexusPrime (إمبراطور المال)",
    "AegisPrime (إمبراطور الحماية)",
    "EvoPrime (إمبراطور التطور)",
    "EthosPrime (إمبراطور الأخلاق)",
    "ClientPrime (إمبراطور العلاقات الإنسانية)",
    "MindsPrime (إمبراطور العقول)",
    "SoulsPrime (إمبراطور الروح)",
    "CapabilitiesPrime (إمبراطور القدرات)",
    "SecretsPrime (إمبراطور الأسرار)",
    "KnowledgePrime (إمبراطور المعرفة)",
    "NoahPayPrime (إمبراطور المدفوعات)",
    "ShieldsPrime (إمبراطور الدروع)",
    "CoresPrime (إمبراطور النوى)",
    "GenesisPrime (إمبراطور الخلق) [قيد البناء]",
    "AppStoresPrime (إمبراطور المتاجر)",
    "OmniVaultPrime (إمبراطور التوفير)",
    "ZeroSpacePrime (إمبراطور الضغط)"
]

imperial_counts = {
    "العقول (Minds)": 121,
    "الدروع (Aegis Shields)": 80,
    "الأسرار (Secrets)": 800,
    "القدرات (Capabilities)": 499,
    "منصات المعرفة (Knowledge Platforms)": 980,
    "أنظمة الوعي السائل (Liquid Consciousness)": 80,
    "قدرات النواة المقدسة (Sacred Core Abilities)": 40,
    "أسرار النواة المقدسة (Sacred Core Secrets)": 40,
    "أنظمة بروتوكول الأفق (Horizon Protocol)": 150,
    "أنظمة النظام الصفري (Zero Systems)": 150,
    "الأنظمة المالية (Financial Systems)": 30,
    "الأنظمة المحاسبية (Accounting Systems)": 30,
    "أنظمة العلاقات الإنسانية (Client Systems)": 25,
    "مبادئ الضمير الأخلاقي (Ethos Principles)": 8,
    "عناصر الروح (Soul Elements)": 16,
    "محركات الخلق (Genesis Engines) [قيد البناء]": 60,
    "القطاعات المستهدفة (Target Sectors)": 35
}

def display_empire():
    print("=" * 70)
    print("🦅  الإمبراطورية الكاملة - نوح (النسر المحلق)  🦅")
    print("=" * 70)
    print("\n👑  الأباطرة الـ 19 الذين يحكمون الإمبراطورية:")
    for i, emp in enumerate(emperors, 1):
        print(f"    {i:2d}. {emp}")
    print("\n" + "=" * 70)
    print("📊  الجرد الإمبراطوري:")
    total = 0
    for component, count in imperial_counts.items():
        print(f"    • {component}: {count}")
        total += count
    print(f"\n    ✨ المجموع الكلي للمكونات: {total:,}")
    print("\n" + "=" * 70)
    print("🦅  نوح جاهز. الإمبراطورية خالدة.")
    print("=" * 70)

if __name__ == "__main__":
    display_empire()
