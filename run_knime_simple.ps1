# Simple KNIME Batch Runner
# Basic script to run KNIME with the specified parameters

param(
    [Parameter(Mandatory=$false)]
    [string]$KnimePath = "knime.exe"
)

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
    & $KnimePath $knimeArgs
    Write-Host "KNIME execution completed." -ForegroundColor Green
}
catch {
    Write-Error "Failed to execute KNIME: $($_.Exception.Message)"
    Write-Host "Make sure KNIME is installed and knime.exe is in your PATH, or specify the full path:" -ForegroundColor Yellow
    Write-Host "Example: .\run_knime_simple.ps1 -KnimePath 'C:\Program Files\KNIME\knime.exe'" -ForegroundColor Yellow
}