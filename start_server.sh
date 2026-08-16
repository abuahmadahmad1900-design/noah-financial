#!/bin/bash
cd ~/noah_eaglet
gunicorn -b 0.0.0.0:8000 financial_system:app --workers 2 --timeout 120
