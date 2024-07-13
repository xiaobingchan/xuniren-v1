@echo off
ping -n 2 127.0.0.1
cd /d D:\UE\nginx-1.25.4\html\ue53_web
python app.py
pause