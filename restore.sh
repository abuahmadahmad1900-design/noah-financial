#!/bin/bash
echo "🦅 بدء استعادة الإمبراطورية..."
cd ~/noah_eaglet
latest_backup=$(ls -t noah_backup_*.tar.gz 2>/dev/null | head -1)
if [ -z "$latest_backup" ]; then
    echo "❌ لا توجد نسخة احتياطية."
    exit 1
fi
echo "📦 النسخة: $latest_backup"
tar -xzf "$latest_backup"
echo "✅ تمت الاستعادة بنجاح."
echo "🚀 شغّل: python ~/noah_eaglet/noah_final.py"
