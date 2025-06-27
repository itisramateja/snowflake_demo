# KNIME Batch Application Runner
# This script runs KNIME in batch mode with console logging enabled

param(
    [Parameter(Mandatory=$false)]
    [string]$KnimePath = "knime.exe",
    
    [Parameter(Mandatory=$false)]
    [string]$WorkflowPath = "",
    
    [Parameter(Mandatory=$false)]
    [string]$WorkspacePath = "",
    
    [Parameter(Mandatory=$false)]
    [string]$AdditionalArgs = ""
)

# Function to check if KNIME executable exists
function Test-KnimeExecutable {
    param([string]$Path)
    
    # If a full path is provided, check if it exists
    if ($Path -ne "knime.exe" -and (Test-Path $Path)) {
        return $true
    }
    
    # Try to find knime.exe in PATH first
    try {
        $knimeInPath = Get-Command "knime.exe" -ErrorAction SilentlyContinue
        if ($knimeInPath) {
            Write-Host "Found KNIME in PATH: $($knimeInPath.Source)" -ForegroundColor Green
            return $knimeInPath.Source
        }
    }
    catch {
        # Continue to search in common paths
    }
    
    # Try to find knime.exe in common installation paths
    $commonPaths = @(
        "C:\Program Files\KNIME\knime.exe",
        "C:\Program Files (x86)\KNIME\knime.exe",
        "${env:ProgramFiles}\KNIME\knime.exe",
        "${env:ProgramFiles(x86)}\KNIME\knime.exe",
        "C:\KNIME\knime.exe",
        "${env:LOCALAPPDATA}\KNIME\knime.exe"
    )
    
    # Also search for KNIME Analytics Platform directories
    $knimeSearchPaths = @(
        "C:\Program Files\KNIME*\knime.exe",
        "C:\Program Files (x86)\KNIME*\knime.exe",
        "${env:ProgramFiles}\KNIME*\knime.exe",
        "${env:ProgramFiles(x86)}\KNIME*\knime.exe"
    )
    
    # Search common paths first
    foreach ($commonPath in $commonPaths) {
        if (Test-Path $commonPath) {
            Write-Host "Found KNIME at: $commonPath" -ForegroundColor Green
            return $commonPath
        }
    }
    
    # Search with wildcards for versioned installations
    foreach ($searchPath in $knimeSearchPaths) {
        $foundPaths = Get-ChildItem -Path (Split-Path $searchPath) -Filter (Split-Path $searchPath -Leaf) -ErrorAction SilentlyContinue
        if ($foundPaths) {
            $knimePath = $foundPaths[0].FullName
            if (Test-Path $knimePath) {
                Write-Host "Found KNIME at: $knimePath" -ForegroundColor Green
                return $knimePath
            }
        }
    }
    
    return $false
}

# Function to build KNIME command arguments
function Build-KnimeCommand {
    param(
        [string]$ExecutablePath,
        [string]$WorkflowPath,
        [string]$WorkspacePath,
        [string]$AdditionalArgs
    )
    
    $baseArgs = @(
        "-consoleLog",
        "-noexit",
        "-nosplash",
        "-application",
        "org.knime.product.KNIME_BATCH_APPLICATION"
    )
    
    $allArgs = $baseArgs
    
    # Add workflow path if provided
    if ($WorkflowPath -ne "") {
        if (Test-Path $WorkflowPath) {
            $allArgs += "-workflowFile"
            $allArgs += "`"$WorkflowPath`""
        } else {
            Write-Warning "Workflow path does not exist: $WorkflowPath"
        }
    }
    
    # Add workspace path if provided
    if ($WorkspacePath -ne "") {
        if (Test-Path $WorkspacePath) {
            $allArgs += "-data"
            $allArgs += "`"$WorkspacePath`""
        } else {
            Write-Warning "Workspace path does not exist: $WorkspacePath"
        }
    }
    
    # Add any additional arguments
    if ($AdditionalArgs -ne "") {
        $allArgs += $AdditionalArgs.Split(' ')
    }
    
    return $allArgs
}

# Main execution
Write-Host "KNIME Batch Application Runner" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

# Check if KNIME executable exists
$knimeExe = Test-KnimeExecutable -Path $KnimePath
if ($knimeExe -eq $false) {
    Write-Host "KNIME executable not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common solutions:" -ForegroundColor Yellow
    Write-Host "1. Install KNIME Analytics Platform from: https://www.knime.com/downloads" -ForegroundColor White
    Write-Host "2. If KNIME is installed, provide the full path to knime.exe:" -ForegroundColor White
    Write-Host "   .\run_knime.ps1 -KnimePath 'C:\Program Files\KNIME\knime.exe'" -ForegroundColor Cyan
    Write-Host "3. Add KNIME to your system PATH environment variable" -ForegroundColor White
    Write-Host ""
    Write-Host "Common KNIME installation locations to check:" -ForegroundColor Yellow
    Write-Host "- C:\Program Files\KNIME\knime.exe" -ForegroundColor White
    Write-Host "- C:\Program Files (x86)\KNIME\knime.exe" -ForegroundColor White
    Write-Host "- C:\Program Files\KNIME Analytics Platform*\knime.exe" -ForegroundColor White
    Write-Host ""
    Write-Host "To find KNIME on your system, try:" -ForegroundColor Yellow
    Write-Host "Get-ChildItem -Path 'C:\Program Files*' -Recurse -Name 'knime.exe' -ErrorAction SilentlyContinue" -ForegroundColor Cyan
    exit 1
} elseif ($knimeExe -ne $true) {
    $KnimePath = $knimeExe
}

# Build the command arguments
$commandArgs = Build-KnimeCommand -ExecutablePath $KnimePath -WorkflowPath $WorkflowPath -WorkspacePath $WorkspacePath -AdditionalArgs $AdditionalArgs

# Display the command that will be executed
Write-Host "Executing KNIME with the following command:" -ForegroundColor Green
Write-Host "$KnimePath $($commandArgs -join ' ')" -ForegroundColor White

# Confirm execution
$confirmation = Read-Host "Do you want to proceed? (Y/N)"
if ($confirmation -eq 'Y' -or $confirmation -eq 'y' -or $confirmation -eq 'Yes' -or $confirmation -eq 'yes') {
    try {
        # Execute KNIME
        Write-Host "Starting KNIME..." -ForegroundColor Green
        & $KnimePath $commandArgs
        
        Write-Host "KNIME execution completed." -ForegroundColor Green
    }
    catch {
        Write-Error "Error executing KNIME: $($_.Exception.Message)"
        exit 1
    }
} else {
    Write-Host "Execution cancelled by user." -ForegroundColor Yellow
}