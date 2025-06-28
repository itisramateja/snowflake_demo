# Simple KNIME Workflow Runner
# Usage: .\run_knime_workflow_simple.ps1 "C:\path\to\workflow.zip"

param(
    [Parameter(Mandatory=$true, Position=0, HelpMessage="Path to the KNIME workflow file")]
    [string]$WorkflowFile
)

# Validate workflow file exists
if (-not (Test-Path $WorkflowFile)) {
    Write-Host "❌ Error: Workflow file not found: $WorkflowFile" -ForegroundColor Red
    exit 1
}

# Find KNIME executable
$knimePath = $null

# Check current directory first (PowerShell security)
if (Test-Path ".\knime.exe") {
    $knimePath = ".\knime.exe"
    Write-Host "Using KNIME from current directory" -ForegroundColor Green
}
# Check PATH
elseif (Get-Command "knime.exe" -ErrorAction SilentlyContinue) {
    $knimePath = "knime.exe"
    Write-Host "Using KNIME from PATH" -ForegroundColor Green
}
# Check common locations
else {
    $commonPaths = @(
        "${env:ProgramFiles}\KNIME\knime.exe",
        "${env:LOCALAPPDATA}\Programs\KNIME\knime.exe"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            $knimePath = $path
            Write-Host "Found KNIME at: $path" -ForegroundColor Green
            break
        }
    }
}

if (-not $knimePath) {
    Write-Host "❌ KNIME not found! Please ensure KNIME is installed and accessible." -ForegroundColor Red
    exit 1
}

# Get absolute path for workflow
$workflowPath = Resolve-Path $WorkflowFile

# Build and execute command
Write-Host "Executing workflow: $([System.IO.Path]::GetFileName($workflowPath))" -ForegroundColor Cyan
Write-Host "Started at: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray

$arguments = "-reset -nosave -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflowFile=`"$workflowPath`""

Write-Host "Command: $knimePath $arguments" -ForegroundColor Yellow
Write-Host ""

# Execute KNIME
try {
    & $knimePath -reset -nosave -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflowFile="$workflowPath"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Workflow completed successfully!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "❌ Workflow failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    }
    
    exit $LASTEXITCODE
} catch {
    Write-Host "❌ Error executing KNIME: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}