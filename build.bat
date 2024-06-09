set pyname=clean_bg_arg
set qrname=qrcodeGenerator

pip -m pip install --upgrade pip
pip install -r requirements.txt
pip install --upgrade pyinstaller
pyinstaller %pyname%.py

if not exist dist\%pyname%\assets md dist%pyname%\assets
xcopy assets dist\%pyname%\assets /e/i/y

pyinstaller %qrname%.py
xcopy dist\%qrname% dist\%pyname%  /s/e/i/y

pause