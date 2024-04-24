
set rootDir=../test/pptx

pip install --upgrade pip
pip install -r %rootDir%\requirements.txt

python %rootDir%/ppt.py

pause