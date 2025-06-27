# Test script to demonstrate current directory detection
# This script shows how the KNIME scripts handle the current directory scenario

Write-Host "Current Directory KNIME Detection Test" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Current location: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""

# Test if knime.exe exists in current directory
if (Test-Path ".\knime.exe") {
    Write-Host "✓ knime.exe found in current directory" -ForegroundColor Green
    Write-Host "  PowerShell requires: .\knime.exe (with .\ prefix)" -ForegroundColor Cyan
    Write-Host ""
    
    # Test the command recognition
    Write-Host "Testing command recognition:" -ForegroundColor Yellow
    
    # This will fail due to PowerShell security
    Write-Host "1. Testing 'knime.exe' (will fail):" -ForegroundColor White
    try {
        $result = Get-Command "knime.exe" -ErrorAction Stop
        Write-Host "   ✓ Success: $($result.Source)" -ForegroundColor Green
    }
    catch {
        Write-Host "   ✗ Failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # This should work
    Write-Host "2. Testing '.\knime.exe' (should work):" -ForegroundColor White
    try {
        $result = Get-Command ".\knime.exe" -ErrorAction Stop
        Write-Host "   ✓ Success: $($result.Source)" -ForegroundColor Green
    }
    catch {
        Write-Host "   ✗ Failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "Recommendation: Use our KNIME scripts which automatically handle this!" -ForegroundColor Yellow
    Write-Host ".\run_knime.ps1" -ForegroundColor Cyan
    
} else {
    Write-Host "✗ knime.exe not found in current directory" -ForegroundColor Red
    Write-Host "  This test is only relevant when run from a KNIME installation directory" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "For comprehensive KNIME detection, run: .\find_knime.ps1" -ForegroundColor Cyan