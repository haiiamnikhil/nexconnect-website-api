# Strict mode and error handling
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Output "======================================"
Write-Output "  NexConnect Windows Service Install  "
Write-Output "======================================"

# Expected directories based on the two-repo structure
$ApiDir = "C:\Users\Administrator\nexconnect-api"
$VenvDir = Join-Path $ApiDir "backend\venv"
$UvicornExe = Join-Path $VenvDir "Scripts\uvicorn.exe"
$NginxExe = "C:\tools\nginx\nginx.exe"
$NginxDir = "C:\tools\nginx"

try {
    Write-Output "[*] Checking paths..."
    if (-not (Test-Path $ApiDir)) {
        throw "API directory not found at $ApiDir"
    }
    if (-not (Test-Path $UvicornExe)) {
        throw "Uvicorn not found at $UvicornExe. Did you set up the venv?"
    }
    if (-not (Test-Path $NginxExe)) {
        throw "Nginx not found at $NginxExe."
    }

    Write-Output "[*] Installing FastAPI Service (NexConnect-FastAPI)..."
    # Remove if exists
    if ((Get-Service "NexConnect-FastAPI" -ErrorAction SilentlyContinue)) {
        nssm remove "NexConnect-FastAPI" confirm
    }
    
    nssm install "NexConnect-FastAPI" $UvicornExe
    nssm set "NexConnect-FastAPI" AppDirectory $ApiDir
    nssm set "NexConnect-FastAPI" AppParameters "backend.main:app --host 127.0.0.1 --port 8000 --workers 4"
    nssm set "NexConnect-FastAPI" Description "NexConnect FastAPI Backend"
    nssm set "NexConnect-FastAPI" Start SERVICE_AUTO_START

    # Load the .env variables into the service environment
    $EnvPath = Join-Path $ApiDir "backend\.env"
    if ((Test-Path $EnvPath)) {
        $EnvContent = Get-Content $EnvPath
        # Format as null-separated string for NSSM
        $EnvString = ($EnvContent -join "`0") + "`0`0"
        nssm set "NexConnect-FastAPI" AppEnvironmentExtra $EnvString
    }

    Write-Output "[*] Installing Nginx Service (NexConnect-Nginx)..."
    if ((Get-Service "NexConnect-Nginx" -ErrorAction SilentlyContinue)) {
        nssm remove "NexConnect-Nginx" confirm
    }

    nssm install "NexConnect-Nginx" $NginxExe
    nssm set "NexConnect-Nginx" AppDirectory $NginxDir
    nssm set "NexConnect-Nginx" Description "NexConnect Nginx Web Server"
    nssm set "NexConnect-Nginx" Start SERVICE_AUTO_START

    Write-Output "[*] Starting Services..."
    Start-Service "NexConnect-FastAPI"
    Start-Service "NexConnect-Nginx"

    Write-Output "[+] Services installed and started successfully!"
    exit 0
}
catch {
    Write-Warning "Failed to install services: $_"
    exit 1
}
