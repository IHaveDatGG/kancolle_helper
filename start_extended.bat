@echo off
python\python.exe -m pip install -r requirements.txt
python\python.exe src\update.py
start python\pythonw.exe src\main_extended.py
