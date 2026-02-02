# -------- CONFIG --------
$ProjectPath = 'C:\Users\VarunThapar\Downloads\ai-digest'
$VenvPython  = "$ProjectPath\.venv\Scripts\python.exe"

# -------- ENV --------
Set-Location $ProjectPath
$env:PYTHONPATH = 'src'

# -------- RUN PIPELINE --------
& $VenvPython src\cli\run.py
