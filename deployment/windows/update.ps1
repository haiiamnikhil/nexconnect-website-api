# Strict mode and error handling
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Output "======================================"
Write-Output "    NexConnect Update Script          "
Write-Output "======================================"

$ApiDir = "C:\Users\Administrator\nexconnect-api"
$UiDir = "C:\Users\Administrator\nexconnect-ui"
$NginxHtmlDir = "C:\tools\nginx\html\nexconnect"

try {
    Write-Output "[*] Pulling latest API (backend)..."
    Set-Location $ApiDir
    git pull origin main

    Write-Output "[*] Pulling latest UI (frontend)..."
    Set-Location $UiDir
    git pull origin main

    Write-Output "[*] Updating backend dependencies..."
    Set-Location $ApiDir
    $PipExe = Join-Path $ApiDir "backend\venv\Scripts\pip.exe"
    $ReqPath = Join-Path $ApiDir "backend\requirements.txt"
    & $PipExe install -r $ReqPath

    Write-Output "[*] Building Angular frontend..."
    Set-Location $UiDir
    npm ci
    npm run build -- --configuration production

    Write-Output "[*] Deploying frontend to Nginx..."
    if (-not (Test-Path $NginxHtmlDir)) {
        New-Item -ItemType Directory -Force -Path $NginxHtmlDir | Out-Null
    }
    
    $SourceDist = Join-Path $UiDir "dist\frontend\browser"
    # Remove old files
    Remove-Item -Recurse -Force (Join-Path $NginxHtmlDir "*") -ErrorAction SilentlyContinue
    # Copy new files
    Copy-Item -Recurse -Force (Join-Path $SourceDist "*") $NginxHtmlDir

    Write-Output "[*] Restarting services..."
    Restart-Service "NexConnect-FastAPI"
    Restart-Service "NexConnect-Nginx"

    Write-Output "[+] Update complete!"
    exit 0
}
catch {
    Write-Warning "Update failed: $_"
    exit 1
}
