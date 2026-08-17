import requests
import time
from datetime import datetime

SERVICES = [
    ("💼 المالي", "https://noah-finance.onrender.com"),
    ("🏥 الطبي", "https://noah-financial-4.onrender.com"),
    ("🏢 ERP", "https://noah-erp.onrender.com"),
    ("🦅 المنصة", "https://noah-empire-portal.onrender.com"),
]

def monitor_loop():
    while True:
        print(f"=== مراقبة {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        for name, url in SERVICES:
            try:
                r = requests.get(url, timeout=60)
                status = "✅" if r.status_code == 200 else "⚠️"
            except:
                status = "❌"
            print(f"{status} {name}")
        print("=" * 40)
        time.sleep(300)  # كل 5 دقائق

if __name__ == "__main__":
    monitor_loop()
