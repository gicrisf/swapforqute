# SwapForQute Installation Script for Windows
# Downloads the latest script from the default branch and sets up the userscript

$ErrorActionPreference = "Stop"

$InstallDir = "$env:APPDATA\qutebrowser\userscripts"
$ScriptName = "sfq.py"
$ScriptUrl = "https://raw.githubusercontent.com/gicrisf/swapforqute/main/$ScriptName"

Write-Host "SwapForQute Installation" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Warning: Python not found in PATH. Qutebrowser requires Python to run userscripts." -ForegroundColor Yellow
    Write-Host ""
}

# Create installation directory
Write-Host "Creating installation directory: $InstallDir"
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

# Download the script
Write-Host "Downloading latest script..."
$OutputPath = Join-Path $InstallDir $ScriptName
try {
    Invoke-WebRequest -Uri $ScriptUrl -OutFile $OutputPath
    Write-Host "Download complete!" -ForegroundColor Green
} catch {
    Write-Host "Error: Failed to download the script." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# Create batch wrapper for Windows
Write-Host "Creating batch wrapper..."
$BatchPath = Join-Path $InstallDir "sfq.bat"
$BatchContent = @"
@echo off
REM SwapForQute batch wrapper for Windows
REM This wrapper allows qutebrowser to execute the Python script on Windows

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Execute the Python script with all arguments passed through
python "%SCRIPT_DIR%sfq.py" %*
"@
Set-Content -Path $BatchPath -Value $BatchContent
Write-Host "Batch wrapper created!" -ForegroundColor Green

Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Script installed to: $OutputPath"
Write-Host "Batch wrapper created: $BatchPath"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Edit the RULES dictionary in $OutputPath to customize URL transformations"
Write-Host "2. Add to your qutebrowser config.py:"
Write-Host ""
Write-Host "   import os"
Write-Host "   sfq_script_path = os.path.join(os.getenv('APPDATA'), 'qutebrowser', 'userscripts', 'sfq.bat')"
Write-Host "   sfq_cmd = `"--userscript {}`".format(sfq_script_path)"
Write-Host "   c.aliases['sfq'] = `"set-cmd-text -s :spawn {} --cmd 'open' -u `".format(sfq_cmd)"
Write-Host "   config.bind('o', ':sfq')"
Write-Host ""
Write-Host "3. Restart qutebrowser and press 'o' to use SwapForQute!"
Write-Host ""
