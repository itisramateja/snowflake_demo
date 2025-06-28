@echo off
REM KNIME Workflow Runner Batch Script
REM Usage: run_knime_workflow.bat "C:\path\to\workflow.zip"

setlocal enabledelayedexpansion

if "%~1"=="" (
    echo Error: Please provide a workflow file path
    echo Usage: %~nx0 "C:\path\to\workflow.zip"
    exit /b 1
)

set "WORKFLOW_FILE=%~1"

REM Check if workflow file exists
if not exist "%WORKFLOW_FILE%" (
    echo Error: Workflow file not found: %WORKFLOW_FILE%
    exit /b 1
)

REM Find KNIME executable
set "KNIME_EXE="

REM Check current directory first
if exist "knime.exe" (
    set "KNIME_EXE=knime.exe"
    echo Using KNIME from current directory
    goto :found_knime
)

REM Check common installation paths
set "SEARCH_PATHS=%ProgramFiles%\KNIME\knime.exe"
set "SEARCH_PATHS=%SEARCH_PATHS%;%ProgramFiles(x86)%\KNIME\knime.exe"
set "SEARCH_PATHS=%SEARCH_PATHS%;%LOCALAPPDATA%\Programs\KNIME\knime.exe"

for %%P in ("%SEARCH_PATHS:;=" "%") do (
    if exist %%P (
        set "KNIME_EXE=%%P"
        echo Found KNIME at: %%P
        goto :found_knime
    )
)

REM Try to find KNIME in PATH
knime.exe --version >nul 2>&1
if !errorlevel! equ 0 (
    set "KNIME_EXE=knime.exe"
    echo Using KNIME from PATH
    goto :found_knime
)

echo Error: KNIME executable not found!
echo Please ensure KNIME is installed and accessible.
exit /b 1

:found_knime
echo.
echo Executing workflow: %~nx1
echo Started at: %time%
echo.

REM Execute KNIME with the specified parameters
"%KNIME_EXE%" -reset -nosave -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflowFile="%WORKFLOW_FILE%"

set "EXIT_CODE=%errorlevel%"

echo.
if %EXIT_CODE% equ 0 (
    echo Workflow completed successfully!
) else (
    echo Workflow failed with exit code: %EXIT_CODE%
)

echo Completed at: %time%
exit /b %EXIT_CODE%