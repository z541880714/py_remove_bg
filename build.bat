set pip=C:\Users\lionel\anaconda3\envs\py_remove_bg\Scripts\pip.exe
set pyinstaller=C:\Users\lionel\anaconda3\envs\py_remove_bg\Scripts\pyinstaller.exe

set pyname=clean_bg_arg
set qrname=qrcodeGenerator

%pip% -m pip install --upgrade pip
%pip% install -r requirements.txt
%pip% install --upgrade pyinstaller
%pyinstaller% %pyname%.py -y

if not exist dist\%pyname%\assets md dist\%pyname%\assets
xcopy assets dist\%pyname%\assets /e/i/y

%pyinstaller% %qrname%.py -y
xcopy dist\%qrname% dist\%pyname%  /s/e/i/y

rd /s /q dist\%qrname%\


7z a out\py_remove.7z dist\%pyname%

pause