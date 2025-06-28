# KNIME Workflow Runner Script
# Executes KNIME in batch mode with a specified workflow file
# Usage: .\run_knime_workflow.ps1 -WorkflowFile "C:\path\to\workflow.zip"

param(
    [Parameter(Mandatory=$true, HelpMessage="Path to the KNIME workflow file (.zip or .knwf)")]
    [ValidateScript({
        if (Test-Path $_) {
            $true
        } else {
            throw "Workflow file not found: $_"
        }
    })]
    [string]$WorkflowFile,
    
    [Parameter(Mandatory=$false, HelpMessage="Path to KNIME executable (auto-detected if not specified)")]
    [string]$KnimePath,
    
    [Parameter(Mandatory=$false, HelpMessage="Additional KNIME arguments")]
    [string]$AdditionalArgs = "",
    
    [Parameter(Mandatory=$false, HelpMessage="Skip confirmation prompt")]
    [switch]$Force
)

# Function to find KNIME executable
function Find-KnimeExecutable {
    Write-Host "Searching for KNIME executable..." -ForegroundColor Yellow
    
    # Check current directory first (handles PowerShell security)
    if (Test-Path ".\knime.exe") {
        Write-Host "✓ Found KNIME in current directory" -ForegroundColor Green
        return ".\knime.exe"
    }
    
    # Check if knime is in PATH
    try {
        $knimeCmd = Get-Command "knime.exe" -ErrorAction Stop
        Write-Host "✓ Found KNIME in PATH: $($knimeCmd.Source)" -ForegroundColor Green
        return "knime.exe"
    }
    catch {
        Write-Host "  KNIME not found in PATH" -ForegroundColor Gray
    }
    
    # Check common installation paths
    $commonPaths = @(
        "${env:ProgramFiles}\KNIME\knime.exe",
        "${env:ProgramFiles(x86)}\KNIME\knime.exe",
        "${env:LOCALAPPDATA}\Programs\KNIME\knime.exe",
        "${env:USERPROFILE}\KNIME\knime.exe"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            Write-Host "✓ Found KNIME at: $path" -ForegroundColor Green
            return $path
        }
    }
    
    # Wildcard search for versioned installations
    $searchPaths = @(
        "${env:ProgramFiles}\KNIME*\knime.exe",
        "${env:ProgramFiles(x86)}\KNIME*\knime.exe",
        "${env:LOCALAPPDATA}\Programs\KNIME*\knime.exe"
    )
    
    foreach ($searchPath in $searchPaths) {
        $found = Get-ChildItem -Path $searchPath -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) {
            Write-Host "✓ Found KNIME at: $($found.FullName)" -ForegroundColor Green
            return $found.FullName
        }
    }
    
    return $null
}

# Function to validate workflow file
function Test-WorkflowFile {
    param([string]$FilePath)
    
    if (-not (Test-Path $FilePath)) {
        throw "Workflow file not found: $FilePath"
    }
    
    $extension = [System.IO.Path]::GetExtension($FilePath).ToLower()
    if ($extension -notin @('.zip', '.knwf')) {
        Write-Warning "Workflow file should typically be .zip or .knwf format. Found: $extension"
    }
    
    return $true
}

# Main execution
try {
    Write-Host "KNIME Workflow Runner" -ForegroundColor Cyan
    Write-Host "===================" -ForegroundColor Cyan
    Write-Host ""
    
    # Validate workflow file
    Write-Host "Validating workflow file..." -ForegroundColor Yellow
    Test-WorkflowFile -FilePath $WorkflowFile
    $resolvedWorkflowPath = Resolve-Path $WorkflowFile
    Write-Host "✓ Workflow file: $resolvedWorkflowPath" -ForegroundColor Green
    Write-Host ""
    
    # Find KNIME executable
    if (-not $KnimePath) {
        $KnimePath = Find-KnimeExecutable
        if (-not $KnimePath) {
            Write-Host "❌ KNIME executable not found!" -ForegroundColor Red
            Write-Host ""
            Write-Host "Solutions:" -ForegroundColor Yellow
            Write-Host "1. Add KNIME to your system PATH" -ForegroundColor White
            Write-Host "2. Run this script from the KNIME installation directory" -ForegroundColor White
            Write-Host "3. Specify the path manually: -KnimePath 'C:\Path\To\knime.exe'" -ForegroundColor White
            Write-Host "4. Use find_knime.ps1 to locate KNIME installations" -ForegroundColor White
            exit 1
        }
    } else {
        if (-not (Test-Path $KnimePath)) {
            throw "Specified KNIME path not found: $KnimePath"
        }
        Write-Host "✓ Using specified KNIME path: $KnimePath" -ForegroundColor Green
    }
    Write-Host ""
    
    # Build command arguments
    $knimeArgs = @(
        "-reset",
        "-nosave", 
        "-nosplash",
        "-application", "org.knime.product.KNIME_BATCH_APPLICATION",
        "-workflowFile=`"$resolvedWorkflowPath`""
    )
    
    if ($AdditionalArgs) {
        $knimeArgs += $AdditionalArgs.Split(' ')
    }
    
    # Display command to be executed
    Write-Host "Command to execute:" -ForegroundColor Yellow
    Write-Host "$KnimePath $($knimeArgs -join ' ')" -ForegroundColor White
    Write-Host ""
    
    # Confirmation prompt
    if (-not $Force) {
        $confirmation = Read-Host "Do you want to execute this command? (y/N)"
        if ($confirmation -notmatch '^[Yy]') {
            Write-Host "Operation cancelled by user." -ForegroundColor Yellow
            exit 0
        }
        Write-Host ""
    }
    
    # Execute KNIME
    Write-Host "Starting KNIME workflow execution..." -ForegroundColor Green
    Write-Host "Workflow: $([System.IO.Path]::GetFileName($resolvedWorkflowPath))" -ForegroundColor Cyan
    Write-Host "Started at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
    Write-Host ""
    Write-Host "--- KNIME Output ---" -ForegroundColor Magenta
    
    # Start the process and capture output
    $processInfo = New-Object System.Diagnostics.ProcessStartInfo
    $processInfo.FileName = $KnimePath
    $processInfo.Arguments = $knimeArgs -join ' '
    $processInfo.UseShellExecute = $false
    $processInfo.RedirectStandardOutput = $true
    $processInfo.RedirectStandardError = $true
    $processInfo.CreateNoWindow = $false
    
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $processInfo
    
    # Event handlers for output
    $outputBuilder = New-Object System.Text.StringBuilder
    $errorBuilder = New-Object System.Text.StringBuilder
    
    $outputAction = {
        if ($Event.SourceEventArgs.Data) {
            Write-Host $Event.SourceEventArgs.Data
            [void]$outputBuilder.AppendLine($Event.SourceEventArgs.Data)
        }
    }
    
    $errorAction = {
        if ($Event.SourceEventArgs.Data) {
            Write-Host $Event.SourceEventArgs.Data -ForegroundColor Red
            [void]$errorBuilder.AppendLine($Event.SourceEventArgs.Data)
        }
    }
    
    Register-ObjectEvent -InputObject $process -EventName OutputDataReceived -Action $outputAction | Out-Null
    Register-ObjectEvent -InputObject $process -EventName ErrorDataReceived -Action $errorAction | Out-Null
    
    # Start the process
    $process.Start() | Out-Null
    $process.BeginOutputReadLine()
    $process.BeginErrorReadLine()
    
    # Wait for completion
    $process.WaitForExit()
    
    # Clean up events
    Get-EventSubscriber | Unregister-Event
    
    Write-Host ""
    Write-Host "--- End KNIME Output ---" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "Completed at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
    
    # Check exit code
    if ($process.ExitCode -eq 0) {
        Write-Host "✅ KNIME workflow completed successfully!" -ForegroundColor Green
        Write-Host "Exit code: $($process.ExitCode)" -ForegroundColor Green
    } else {
        Write-Host "❌ KNIME workflow failed!" -ForegroundColor Red
        Write-Host "Exit code: $($process.ExitCode)" -ForegroundColor Red
        
        if ($errorBuilder.Length -gt 0) {
            Write-Host ""
            Write-Host "Error details:" -ForegroundColor Yellow
            Write-Host $errorBuilder.ToString() -ForegroundColor Red
        }
    }
    
    exit $process.ExitCode
    
} catch {
    Write-Host ""
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Usage examples:" -ForegroundColor Yellow
    Write-Host "  .\run_knime_workflow.ps1 -WorkflowFile 'C:\Workflows\MyWorkflow.zip'" -ForegroundColor White
    Write-Host "  .\run_knime_workflow.ps1 -WorkflowFile 'workflow.knwf' -Force" -ForegroundColor White
    Write-Host "  .\run_knime_workflow.ps1 -WorkflowFile 'workflow.zip' -KnimePath 'C:\KNIME\knime.exe'" -ForegroundColor White
    exit 1
}