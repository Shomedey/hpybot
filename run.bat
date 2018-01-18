@ECHO OFF

goto start

:start
cls
if not exist installedrequirements.txt (
	echo Installing requirements from requirements.txt
	python -m pip install -r requirements.txt
	echo - >installedrequirements.txt
)
python start.py
ping -n 2 127.0.0.1 >nul
goto start