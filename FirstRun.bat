@echo off


:start
cls

set python_ver=39



cd \
cd \python%python_ver%\Scripts\

cmd /k "D:\Code\DBMS-Event-Management-System & pip install -r requirements.txt"
cmd /k "D:\Code\DBMS-Event-Management-System & python app.py"
pause
exit