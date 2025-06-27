@echo off
REM KNIME Batch Application Runner (Batch File Version)
REM This batch file runs KNIME with the specified parameters

echo Running KNIME in batch mode...

REM Set default KNIME path (modify as needed)
set KNIME_PATH=knime.exe

REM Check if custom path is provided as argument
if not "%1"=="" set KNIME_PATH=%1

REM Execute KNIME with the specified parameters
"%KNIME_PATH%" -consoleLog -noexit -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION

if %ERRORLEVEL% neq 0 (
    echo Error: Failed to execute KNIME
    echo Make sure KNIME is installed and the path is correct
    echo Usage: run_knime.bat [path_to_knime.exe]
    pause
) else (
    echo KNIME execution completed successfully
)