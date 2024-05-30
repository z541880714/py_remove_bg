set pyroot=.venv\Scripts
set pyth=.venv\Scripts\python.exe
set pip=.venv\Scripts\pip.exe

%pyth% -m pip install --upgrade pip

%pip% install -r requirements.txt

%pip% install --upgrade pyinstaller

%pyroot%\pyinstaller clean_bg.py

xcopy res dist\clean_bg\res /e/i
if not exist dist\clean_bg\assets md dist\clean_bg\assets
xcopy assets dist\clean_bg\assets /e/i

pause