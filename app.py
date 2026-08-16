#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
import importlib.util, os

app = Flask(__name__)
BASE = "/data/data/com.termux/files/home/noah_eaglet/"

def load_noah():
    spec = importlib.util.spec_from_file_location("noah_final", BASE + "noah_final.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def load_extra(attr):
    """تحميل متغير من ملف خارجي"""
    extra_files = {
        'all_sectors_50_complete': 'all_sectors_50_complete.py',
    }
    if attr in extra_files:
        path = BASE + extra_files[attr]
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location(attr, path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return getattr(mod, attr, [])
    return []

def safe_len(obj):
    try:
        return len(obj)
    except:
        return 0

MAPPING = [
    ('الأباطرة', 'emperors'),
    ('العقول', 'all_minds_400'),
    ('الدروع', 'shields'),
    ('محركات الخلق', 'genesis_engines'),
    ('أنظمة الخوارزمية', 'all_imperial_systems'),
    ('الأنظمة المالية', 'financial_systems'),
    ('الأنظمة المحاسبية', 'accounting_systems'),
    ('القطاعات', 'all_sectors'),
    ('المتاجر', 'all_stores'),
    ('قدرات المتاجر', 'all_store_superpowers'),
    ('قدرات العلاقات', 'all_human_relations_powers'),
    ('قدرات التوفير', 'all_financial_optimization_powers'),
    ('أنظمة التوفير', 'all_financial_optimization_systems'),
    ('قدرات الضغط', 'all_compression_powers'),
    ('أنظمة الضغط', 'all_compression_systems'),
    ('قدرات المدفوعات', 'all_payment_powers'),
    ('أنظمة المدفوعات', 'all_payment_systems'),
    ('أنظمة OmniCore', 'all_omnicore_systems'),
    ('قدرات OmniCore', 'omnicore_powers_500'),
    ('أنظمة OmniSovereign', 'all_omnisovereign_systems'),
    ('قدرات OmniSovereign', 'all_omnisovereign_powers'),
    ('أنظمة OmniInfinite', 'all_omniinfinite_systems'),
    ('قدرات OmniInfinite', 'all_omniinfinite_powers'),
    ('أنظمة KnowledgePrime', 'all_knowledge_prime_systems'),
    ('قدرات KnowledgePrime', 'all_knowledge_prime_powers'),
    ('المؤسسات التعليمية', 'all_educational_institutions'),
    ('المراجع الشرعية', 'all_islamic_references'),
    ('المكونات الشرعية', 'all_islamic_complete'),
    ('أنظمة التعلم', 'all_learning_systems'),
    ('قدرات التعلم', 'all_learning_powers'),
    ('المكونات العلمية', 'all_scientific_tech'),
    ('الكيانات العليا', 'all_higher_entities'),
    ('تقوية الكيانات', 'all_entities_boost'),
    ('أنظمة SelfDevPrime', 'all_selfdev_systems'),
    ('قدرات SelfDevPrime', 'selfdev_prime_powers'),
    ('أنظمة SelfDevPrime Mega', 'all_selfdev_mega_systems'),
    ('قدرات SelfDevPrime Mega', 'all_selfdev_mega_powers'),
    ('أنظمة TradeOmniPrime', 'all_trade_omni'),
    ('قدرات TradeOmniPrime', 'all_trade_essential'),
    ('المنصات العلمية', 'scientific_platforms_200'),
    ('المنصات الإضافية', 'all_scientific_platforms_extra'),
    ('عناصر الروح', 'soul_elements'),
    ('فئات القدرات', 'capability_categories'),
    ('القطاعات الخمسون الجديدة', 'all_sectors_50_complete'),
    ('القطاعات الأربعة الكبرى', 'all_top_sectors'),
    ('الأنظمة الصحية التفصيلية', 'health_systems_full'),
    ('الأنظمة الفضائية التفصيلية', 'space_systems_full'),
    ('الأنظمة الزراعية التفصيلية', 'agriculture_systems_full'),
    ('الأنظمة الطاقية التفصيلية', 'energy_systems_full'),
    ('الأنظمة الإعلامية التفصيلية', 'media_systems_full'),
]

def get_items(attr):
    if attr == 'all_sectors_50_complete':
        return load_extra(attr)
    if attr == 'all_top_sectors':
        path = BASE + 'all_top_sectors.py'
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location('top', path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return getattr(mod, 'all_top_sectors', [])
        return []
    noah = load_noah()
    if hasattr(noah, attr):
        return getattr(noah, attr)
    return []

@app.route('/')
def index():
    noah = load_noah()
    emperors = list(noah.emperors) if hasattr(noah, 'emperors') else []
    stats = {}
    for label, attr in MAPPING:
        stats[label] = safe_len(get_items(attr))
    total = sum(stats.values())
    stats['الإجمالي'] = total
    stats['total'] = total
    return render_template('index.html', stats=stats, emperors=emperors)

@app.route('/minds')
def minds():
    items = get_items('all_minds_400')
    return render_template('minds.html', minds=items, count=len(items))

@app.route('/browse')
def browse():
    categories = []
    for label, attr in MAPPING:
        categories.append({'label': label, 'attr': attr, 'count': safe_len(get_items(attr))})
    return render_template('browse.html', categories=categories)

@app.route('/all')
def all_items():
    all_data = []
    for label, attr in MAPPING:
        for item in get_items(attr):
            all_data.append((item, label))
    return render_template('all.html', all_data=all_data, count=len(all_data))

@app.route('/api/stats')
def api_stats():
    stats = {}
    for label, attr in MAPPING:
        stats[label] = safe_len(get_items(attr))
    stats['total'] = sum(stats.values())
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
