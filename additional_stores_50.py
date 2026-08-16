#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# additional_stores_50.py - 50 متجرًا جديدًا

additional_stores_50 = [
    # ===== متاجر تطبيقات عالمية (10) =====
    "Aptoide", "APKMirror", "APKPure", "F-Droid", "Uptodown",
    "GetJar", "SlideME", "Mobogenie", "9Apps", "AppBrain",

    # ===== متاجر شركات كبرى (10) =====
    "Xiaomi GetApps", "Oppo App Market", "Vivo App Store", "OnePlus Store",
    "Realme App Market", "Lenovo App Store", "ZTE App Store", "LG SmartWorld",
    "Sony Select", "Panasonic App Store",

    # ===== متاجر إقليمية (10) =====
    "Baidu Mobile Assistant", "Tencent MyApp", "360 Mobile Assistant",
    "Wandoujia", "Yandex Store", "Mail.ru Store", "Naver App Store",
    "Kakao App Store", "Line App Store", "Rakuten App Store",

    # ===== متاجر متخصصة (10) =====
    "Meta Quest Store", "Steam Store", "Epic Games Store", "GOG Store",
    "Itch.io Store", "Roblox Store", "Minecraft Marketplace",
    "Unity Asset Store", "Unreal Marketplace", "Sketchfab Store",

    # ===== متاجر بديلة ومستقلة (10) =====
    "AppGallery Lite", "Aurora Store", "OpenStore", "AppCenter",
    "Snap Store", "Flatpak Store", "Flathub Store", "Homebrew Store",
    "Chocolatey Store", "Winget Store"
]

def display_additional_stores():
    print("=" * 80)
    print(f"🏪  قائمة الـ {len(additional_stores_50)} متجرًا الجديد (لنصل إلى 60)  🏪")
    print("=" * 80)
    for i, store in enumerate(additional_stores_50, 1):
        print(f"    {i:2d}. {store}")
    print("\n" + "=" * 80)
    print(f"✨  إجمالي المتاجر الإضافية: {len(additional_stores_50)}")
    print("=" * 80)

if __name__ == "__main__":
    display_additional_stores()
