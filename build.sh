#!/bin/bash
# Script de build para Vercel
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput

