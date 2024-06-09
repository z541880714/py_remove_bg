set pyroot=.venv\Scripts
set pyth=.venv\Scripts\python.exe
set pip=.venv\Scripts\pip.exe

set pyname=clean_bg_arg

%pyth% -m pip install --upgrade pip

%pip% install -r requirements.txt

%pip% install --upgrade pyinstaller

%pyroot%\pyinstaller %pyname%.py

if not exist dist\%pyname%\assets md dist%pyname%\assets
xcopy assets dist\%pyname%\assets /e/i/y

pause