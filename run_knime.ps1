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
    
    if (Test-Path $Path) {
        return $true
    }
    
    # Try to find knime.exe in common installation paths
    $commonPaths = @(
        "C:\Program Files\KNIME\knime.exe",
        "C:\Program Files (x86)\KNIME\knime.exe",
        "${env:ProgramFiles}\KNIME\knime.exe",
        "${env:ProgramFiles(x86)}\KNIME\knime.exe"
    )
    
    foreach ($commonPath in $commonPaths) {
        if (Test-Path $commonPath) {
            Write-Host "Found KNIME at: $commonPath" -ForegroundColor Green
            return $commonPath
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
    Write-Error "KNIME executable not found at: $KnimePath"
    Write-Host "Please ensure KNIME is installed and provide the correct path using -KnimePath parameter" -ForegroundColor Yellow
    Write-Host "Example: .\run_knime.ps1 -KnimePath 'C:\Program Files\KNIME\knime.exe'" -ForegroundColor Yellow
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