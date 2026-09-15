@echo off
setlocal
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
pyinstaller --clean virtual_fly_brain_puppy.spec
echo Build complete: dist\VirtualFlyBrainPuppy\VirtualFlyBrainPuppy.exe
