# KNIME Installation Finder
# This script helps locate KNIME installations on your system

Write-Host "KNIME Installation Finder" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# Check current directory first
Write-Host "Checking current directory..." -ForegroundColor Yellow
if (Test-Path ".\knime.exe") {
    Write-Host "✓ Found KNIME in current directory: $(Get-Location)\knime.exe" -ForegroundColor Green
    Write-Host "  Use: .\knime.exe (note the .\ prefix required by PowerShell)" -ForegroundColor Cyan
} else {
    Write-Host "✗ KNIME not found in current directory" -ForegroundColor Red
}

Write-Host ""

# Check if knime.exe is in PATH
Write-Host "Checking if KNIME is in system PATH..." -ForegroundColor Yellow
try {
    $knimeInPath = Get-Command "knime.exe" -ErrorAction SilentlyContinue
    if ($knimeInPath) {
        Write-Host "✓ Found KNIME in PATH: $($knimeInPath.Source)" -ForegroundColor Green
    } else {
        Write-Host "✗ KNIME not found in system PATH" -ForegroundColor Red
    }
}
catch {
    Write-Host "✗ KNIME not found in system PATH" -ForegroundColor Red
}

Write-Host ""
Write-Host "Searching common installation directories..." -ForegroundColor Yellow

# Search common installation paths
$searchPaths = @(
    "C:\Program Files",
    "C:\Program Files (x86)",
    "${env:ProgramFiles}",
    "${env:ProgramFiles(x86)}",
    "C:\",
    "${env:LOCALAPPDATA}"
)

$foundInstallations = @()

foreach ($searchPath in $searchPaths) {
    if (Test-Path $searchPath) {
        Write-Host "Searching in: $searchPath" -ForegroundColor Gray
        try {
            $knimeFiles = Get-ChildItem -Path $searchPath -Recurse -Name "knime.exe" -ErrorAction SilentlyContinue | Select-Object -First 10
            foreach ($knimeFile in $knimeFiles) {
                $fullPath = Join-Path $searchPath $knimeFile
                if (Test-Path $fullPath) {
                    $foundInstallations += $fullPath
                    Write-Host "  ✓ Found: $fullPath" -ForegroundColor Green
                }
            }
        }
        catch {
            # Continue searching other paths
        }
    }
}

Write-Host ""
if ($foundInstallations.Count -eq 0) {
    Write-Host "No KNIME installations found on this system." -ForegroundColor Red
    Write-Host ""
    Write-Host "To install KNIME:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://www.knime.com/downloads" -ForegroundColor White
    Write-Host "2. Download KNIME Analytics Platform" -ForegroundColor White
    Write-Host "3. Run the installer and follow the setup wizard" -ForegroundColor White
} else {
    Write-Host "Found $($foundInstallations.Count) KNIME installation(s):" -ForegroundColor Green
    Write-Host ""
    
    for ($i = 0; $i -lt $foundInstallations.Count; $i++) {
        Write-Host "[$($i + 1)] $($foundInstallations[$i])" -ForegroundColor White
    }
    
    Write-Host ""
    Write-Host "To use any of these installations with the KNIME scripts:" -ForegroundColor Yellow
    Write-Host ".\run_knime.ps1 -KnimePath `"$($foundInstallations[0])`"" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or to add KNIME to your PATH:" -ForegroundColor Yellow
    Write-Host "1. Open System Properties > Environment Variables" -ForegroundColor White
    Write-Host "2. Add the KNIME directory to your PATH variable:" -ForegroundColor White
    Write-Host "   $(Split-Path $($foundInstallations[0]))" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Script completed." -ForegroundColor Cyan