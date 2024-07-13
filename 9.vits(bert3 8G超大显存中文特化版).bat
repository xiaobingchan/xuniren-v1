@echo off
ping -n 2 127.0.0.1
cd /d D:\Bert-VITS2-Extra\
venv\python.exe server_fastapi.py
pause

