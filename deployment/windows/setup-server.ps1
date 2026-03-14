# Strict mode and error handling
Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

Write-Output "======================================"
Write-Output "    NexConnect Server Setup (Windows) "
Write-Output "======================================"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

try {
    # 1. Install Chocolatey if missing
    if (-not (Get-Command "choco" -ErrorAction SilentlyContinue)) {
        Write-Output "[*] Installing Chocolatey..."
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        Write-Output "[+] Chocolatey installed. Please restart your shell to apply paths, then run this script again."
        exit 0
    }

    # 2. Install dependencies via Chocolatey
    Write-Output "[*] Installing system dependencies (Node, Python, Nginx, NSSM, Git, PostgreSQL)..."
    choco install nodejs python nginx nssm git postgresql -y

    Write-Output "================================================================"
    Write-Output "[+] Base software installed successfully."
    Write-Output "[!] IMPORTANT MANUAL STEPS:"
    Write-Output "  1. Restart this PowerShell (Administrator) window to refresh your PATH."
    Write-Output "  2. Nginx is likely installed at C:\tools\nginx"
    Write-Output "  3. To set up your database, open pgAdmin or use psql to create the 'nexconnect_db' database and 'nexconnect_admin' user."
    Write-Output "  4. Follow DEPLOYMENT_WINDOWS.md for the next steps."
    Write-Output "================================================================"
    
    exit 0
}
catch {
    Write-Warning "Error during setup: $_"
    exit 1
}
