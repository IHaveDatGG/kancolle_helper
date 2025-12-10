@echo off
python\python.exe -m pip install -r requirements.txt
python\python.exe src\update.py
python\python.exe src\main.py
