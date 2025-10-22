# setup_msstore_venv.ps1
# Create a venv using the Microsoft Store Python (if available) and install requirements

$projectRoot = Split-Path -Path $MyInvocation.MyCommand.Path -Parent
Set-Location -LiteralPath $projectRoot

# Try to find python from WindowsApps (Store)
$pythonCandidates = & where.exe python 2>$null | ForEach-Object { $_.Trim() }
$storePython = $null
foreach ($p in $pythonCandidates) {
    if ($p -match 'WindowsApps' -or $p -match 'PythonSoftwareFoundation') {
        $storePython = $p
        break
    }
}

if (-not $storePython) {
    Write-Output "Could not automatically find Microsoft Store Python. Please run 'where.exe python' and pass the full path to python.exe to 'python -m venv .venv-msstore'"
    exit 1
}

Write-Output "Using python: $storePython"

# Create venv
& $storePython -m venv .venv-msstore
Write-Output "Created .venv-msstore"

# Upgrade pip and install requirements
.\.venv-msstore\Scripts\python.exe -m pip install --upgrade pip
.\.venv-msstore\Scripts\python.exe -m pip install -r .\requirements.txt

Write-Output "Setup complete. Activate with: . .\.venv-msstore\Scripts\Activate.ps1"
