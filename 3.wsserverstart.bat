@echo off
ping -n 3 127.0.0.1
cd /d D:\xuniren-v1\WSServer
node SampleWSServer.js
pause