"""
نوح — التصميم الموحد للجداول الفاخرة
يطبق على كل أنظمة الإمبراطورية
"""

UNIFIED_TABLE_CSS = '''
<style>
    /* الجدول الإمبراطوري الموحد */
    .noah-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin-top: 30px;
        border-radius: 30px;
        overflow: hidden;
        background: linear-gradient(145deg, rgba(15,15,45,0.95), rgba(5,5,20,0.98));
        box-shadow: 
            0 30px 80px rgba(0,0,0,0.8),
            0 0 60px rgba(255,215,0,0.15),
            inset 0 0 40px rgba(255,215,0,0.03);
        border: 1px solid rgba(255,215,0,0.3);
        backdrop-filter: blur(20px);
    }

    .noah-table thead th {
        background: linear-gradient(145deg, #FFD700, #FF8C00, #FFD700);
        background-size: 300% 300%;
        animation: noah-header-shift 4s ease infinite;
        color: #000;
        padding: 22px;
        font-size: 1.2rem;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        text-shadow: 0 1px 3px rgba(255,255,255,0.5);
        border-bottom: 3px solid #FFD700;
    }

    @keyframes noah-header-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .noah-table tbody td {
        padding: 18px 15px;
        text-align: center;
        color: #e0e0e0;
        font-size: 1.05rem;
        border-bottom: 1px solid rgba(255,215,0,0.08);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
    }

    .noah-table tbody tr:nth-child(odd) td {
        background: rgba(255,255,255,0.03);
    }

    .noah-table tbody tr:nth-child(even) td {
        background: rgba(0,200,255,0.03);
    }

    .noah-table tbody tr:hover td {
        background: linear-gradient(90deg, rgba(255,215,0,0.15), rgba(255,140,0,0.15));
        color: #FFD700;
        transform: scale(1.02);
        text-shadow: 0 0 10px rgba(255,215,0,0.5);
        border-bottom-color: #FFD700;
    }

    .noah-table tbody tr:hover td::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
        animation: noah-shine 1s infinite;
    }

    @keyframes noah-shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
</style>
'''

def apply_unified_table():
    """دالة مساعدة لتطبيق التصميم الموحد."""
    return UNIFIED_TABLE_CSS
