<#
Local helper to build a Windows executable using PyInstaller.
Run this on Windows PowerShell (as admin if you need to install choco packages).
#>

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
if (Test-Path requirements.txt) { pip install -r requirements.txt }
pip install pyinstaller

# Build single-file exe
pyinstaller --noconfirm --onefile --name CooperRiverDealFinder.exe app.py

Write-Host "Built: dist\CooperRiverDealFinder.exe"
