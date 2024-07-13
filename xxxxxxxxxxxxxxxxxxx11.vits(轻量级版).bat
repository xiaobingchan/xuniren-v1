@echo off
ping -n 2 127.0.0.1
cd /d D:\nova_vits\Bert-VITS2\
D:\nova_vits\vits\python.exe  server_fastapi.py
pause

