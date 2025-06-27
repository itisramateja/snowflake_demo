# Simple KNIME Batch Runner
# Basic script to run KNIME with the specified parameters

param(
    [Parameter(Mandatory=$false)]
    [string]$KnimePath = "knime.exe"
)

# Function to find KNIME executable
function Find-KnimeExecutable {
    param([string]$Path)
    
    # If a full path is provided, check if it exists
    if ($Path -ne "knime.exe" -and (Test-Path $Path)) {
        return $Path
    }
    
    # Check current directory first (PowerShell security requires .\ prefix)
    if (Test-Path ".\knime.exe") {
        return ".\knime.exe"
    }
    
    # Try to find knime.exe in PATH
    try {
        $knimeInPath = Get-Command "knime.exe" -ErrorAction SilentlyContinue
        if ($knimeInPath) {
            return $knimeInPath.Source
        }
    }
    catch {
        # Continue to search in common paths
    }
    
    # Try common installation paths
    $commonPaths = @(
        "C:\Program Files\KNIME\knime.exe",
        "C:\Program Files (x86)\KNIME\knime.exe",
        "${env:ProgramFiles}\KNIME\knime.exe",
        "${env:ProgramFiles(x86)}\KNIME\knime.exe"
    )
    
    foreach ($commonPath in $commonPaths) {
        if (Test-Path $commonPath) {
            return $commonPath
        }
    }
    
    return $null
}

Write-Host "Simple KNIME Batch Runner" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

# Find KNIME executable
$knimeExecutable = Find-KnimeExecutable -Path $KnimePath
if (-not $knimeExecutable) {
    Write-Host "KNIME executable not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Solutions:" -ForegroundColor Yellow
    Write-Host "1. Install KNIME from: https://www.knime.com/downloads" -ForegroundColor White
    Write-Host "2. Specify the full path:" -ForegroundColor White
    Write-Host "   .\run_knime_simple.ps1 -KnimePath 'C:\Program Files\KNIME\knime.exe'" -ForegroundColor Cyan
    Write-Host "3. Add KNIME to your PATH environment variable" -ForegroundColor White
    exit 1
}

Write-Host "Using KNIME at: $knimeExecutable" -ForegroundColor Green
Write-Host "Running KNIME in batch mode..." -ForegroundColor Green

# Basic KNIME command with the specified parameters
$knimeArgs = @(
    "-consoleLog",
    "-noexit", 
    "-nosplash",
    "-application",
    "org.knime.product.KNIME_BATCH_APPLICATION"
)

try {
    & $knimeExecutable $knimeArgs
    Write-Host "KNIME execution completed." -ForegroundColor Green
}
catch {
    Write-Error "Failed to execute KNIME: $($_.Exception.Message)"
    Write-Host "Error details: $($_.Exception)" -ForegroundColor Red
}