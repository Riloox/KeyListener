@echo off
echo Building KeyListener executables...

echo Building main program...
pyinstaller --onefile --noconsole --icon=icon.ico keylistener.py

echo Building register executable...
pyinstaller --onefile --noconsole --icon=icon.ico register.py

echo Building unregister executable...
pyinstaller --onefile --noconsole --icon=icon.ico unregister.py

echo All executables created in the 'dist' folder.
pause