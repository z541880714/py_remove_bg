chcp 65001

set pyroot=C:\Users\lionel\anaconda3\envs\py_remove_bg\Scripts
set pyth=C:\Users\lionel\anaconda3\envs\py_remove_bg\python.exe
set pip=%pyroot%\pip.exe
set pyname=clean_bg_arg


%pyth% -m pip install --upgrade pip

%pip% install -r requirements.txt

%pip% install --upgrade pyinstaller

%pyroot%\pyinstaller %pyname%.py

xcopy res dist\%pyname%\res /e/i
if not exist dist\%pyname%\assets md dist\%pyname%\assets
xcopy assets dist\%pyname%\assets /e/i

pause