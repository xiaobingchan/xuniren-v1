@echo off
ping -n 2 127.0.0.1
cd /d D:\UE\huangsheng-v2-hengping-ue51-a2f-py\camera\
python yolov8-person.py
pause