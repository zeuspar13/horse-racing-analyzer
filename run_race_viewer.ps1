#!/usr/bin/env pwsh

# Set execution policy
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# Set error action preference
$ErrorActionPreference = "Continue"

# Import Windows Forms
Add-Type -AssemblyName System.Windows.Forms

# Define script path
$scriptPath = Join-Path $PSScriptRoot "scripts\race_viewer.ps1"

# Run the script
try {
    & $scriptPath
} catch {
    Write-Host "Error running script: $_" -ForegroundColor Red
    exit 1
}
