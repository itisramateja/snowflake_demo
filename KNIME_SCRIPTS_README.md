# KNIME Batch Application Scripts

This directory contains scripts to run KNIME in batch mode with various parameters and configurations.

## Script Categories

### General KNIME Execution
Scripts that run KNIME with basic batch parameters:
```
knime.exe -consoleLog -noexit -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION
```

### Workflow-Specific Execution  
Scripts that run KNIME with specific workflow files:
```
knime.exe -reset -nosave -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflowFile="path\to\workflow.zip"
```

## Available Scripts

### 1. `find_knime.ps1` (KNIME Installation Finder)
A utility script to locate KNIME installations on your system.

**Features:**
- Searches system PATH for KNIME
- Scans common installation directories
- Provides usage instructions for found installations
- Guides users through installation if KNIME is not found

**Usage:**
```powershell
.\find_knime.ps1
```

### 2. `run_knime.ps1` (Advanced PowerShell Script)
A comprehensive PowerShell script with error handling, path detection, and additional options.

**Features:**
- Automatic KNIME installation path detection
- Workflow and workspace path support
- Error handling and validation
- Interactive confirmation
- Additional arguments support

**Usage:**
```powershell
# Basic usage
.\run_knime.ps1

# With custom KNIME path
.\run_knime.ps1 -KnimePath "C:\Program Files\KNIME\knime.exe"

# With workflow and workspace
.\run_knime.ps1 -WorkflowPath "C:\path\to\workflow" -WorkspacePath "C:\path\to\workspace"

# With additional arguments
.\run_knime.ps1 -AdditionalArgs "-reset -vmargs -Xmx4g"
```

### 2. `run_knime_simple.ps1` (Simple PowerShell Script)
A basic PowerShell script for straightforward execution.

**Usage:**
```powershell
# Basic usage (assumes knime.exe is in PATH)
.\run_knime_simple.ps1

# With custom KNIME path
.\run_knime_simple.ps1 -KnimePath "C:\Program Files\KNIME\knime.exe"
```

### 3. `run_knime.bat` (Batch File)
A Windows batch file for users who prefer batch scripts.

**Usage:**
```cmd
# Basic usage
run_knime.bat

# With custom KNIME path
run_knime.bat "C:\Program Files\KNIME\knime.exe"
```

### 5. `run_knime_workflow.ps1` (Advanced Workflow Runner)
A comprehensive PowerShell script specifically designed to execute KNIME workflows with enhanced validation and error handling.

**Features:**
- Mandatory workflow file parameter with validation
- Automatic KNIME path detection
- Workflow file format validation (.zip, .knwf)
- Real-time output capture and display
- Detailed execution logging with timestamps
- Interactive confirmation (can be bypassed with -Force)
- Comprehensive error handling and reporting

**Usage:**
```powershell
# Basic usage
.\run_knime_workflow.ps1 -WorkflowFile "C:\Users\sinra5\AppData\Local\Programs\KNIME\Workflow\OKTA.zip"

# With custom KNIME path
.\run_knime_workflow.ps1 -WorkflowFile "C:\Workflows\MyWorkflow.zip" -KnimePath "C:\KNIME\knime.exe"

# Skip confirmation prompt
.\run_knime_workflow.ps1 -WorkflowFile "workflow.zip" -Force

# With additional arguments
.\run_knime_workflow.ps1 -WorkflowFile "workflow.zip" -AdditionalArgs "-vmargs -Xmx8g"
```

### 6. `run_knime_workflow_simple.ps1` (Simple Workflow Runner)
A streamlined PowerShell script for quick workflow execution with minimal configuration.

**Features:**
- Single parameter workflow execution
- Automatic KNIME detection
- Simple output display
- Quick execution without prompts

**Usage:**
```powershell
# Simple execution
.\run_knime_workflow_simple.ps1 "C:\Users\sinra5\AppData\Local\Programs\KNIME\Workflow\OKTA.zip"

# Relative path
.\run_knime_workflow_simple.ps1 ".\workflows\OKTA.zip"
```

### 7. `run_knime_workflow.bat` (Batch Workflow Runner)
A Windows batch file for workflow execution, compatible with older systems and automation scripts.

**Features:**
- Single parameter workflow execution
- Automatic KNIME path detection
- Command prompt compatible
- Exit code reporting

**Usage:**
```batch
REM Basic usage
run_knime_workflow.bat "C:\Users\sinra5\AppData\Local\Programs\KNIME\Workflow\OKTA.zip"

REM From command prompt
run_knime_workflow.bat "workflow.zip"
```

## Prerequisites

1. **KNIME Analytics Platform** must be installed on your system
2. **PowerShell** (for .ps1 scripts) - Available by default on Windows 10/11
3. **Execution Policy** - You may need to allow PowerShell script execution:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

## Common KNIME Installation Paths

The scripts will automatically check these common installation paths:
- `C:\Program Files\KNIME\knime.exe`
- `C:\Program Files (x86)\KNIME\knime.exe`

## Command Line Parameters Explained

### General Batch Parameters
- **`-consoleLog`**: Enables console logging output
- **`-noexit`**: Prevents KNIME from exiting immediately after execution
- **`-nosplash`**: Disables the splash screen for faster startup
- **`-application org.knime.product.KNIME_BATCH_APPLICATION`**: Runs KNIME in batch mode

### Workflow-Specific Parameters
- **`-reset`**: Resets the workspace before execution
- **`-nosave`**: Prevents saving the workspace after execution
- **`-workflowFile="path"`**: Specifies the workflow file to execute (.zip or .knwf)

## Additional Options

You can extend these scripts with additional KNIME parameters such as:
- `-workflowFile "path/to/workflow"`: Specify a workflow to execute
- `-data "path/to/workspace"`: Specify workspace directory
- `-reset`: Reset workspace
- `-vmargs -Xmx4g`: Set JVM memory options

## Troubleshooting

### Common Error: "knime is not recognized as the name of a cmdlet"

This error occurs in two scenarios:

**Scenario 1: KNIME not in system PATH**
**Scenario 2: KNIME exists in current directory but PowerShell security blocks it**

PowerShell doesn't execute commands from the current directory by default for security. If you see:
```
The command knime.exe was not found, but does exist in the current location.
```

Here are the solutions:

1. **Use the KNIME finder script** (detects both scenarios):
   ```powershell
   .\find_knime.ps1
   ```
   This will locate all KNIME installations and show you how to use them.

2. **If KNIME is in current directory**, use the `.\` prefix:
   ```powershell
   .\run_knime.ps1 -KnimePath ".\knime.exe"
   ```

3. **Specify the full path to KNIME**:
   ```powershell
   .\run_knime.ps1 -KnimePath "C:\Program Files\KNIME\knime.exe"
   ```

4. **Add KNIME to your PATH** (permanent solution):
   - Open System Properties > Environment Variables
   - Add the KNIME directory to your PATH variable
   - Example: `C:\Program Files\KNIME`

### Other Common Issues

1. **"Execution Policy"**: Run `Set-ExecutionPolicy RemoteSigned` in PowerShell as Administrator
2. **"Access Denied"**: Run the script as Administrator if needed
3. **Memory Issues**: Add `-vmargs -Xmx4g` to increase memory allocation
4. **KNIME not installed**: Download from https://www.knime.com/downloads

### PowerShell Security Note

PowerShell has a security feature that prevents executing commands from the current directory without the `.\` prefix. This is why:
- `knime.exe` fails even if the file exists in the current directory
- `.\knime.exe` works correctly

Our scripts automatically handle this by checking the current directory first and using the proper `.\` prefix when needed.

### Finding KNIME Manually

If the scripts can't find KNIME, you can search manually:
```powershell
Get-ChildItem -Path "C:\Program Files*" -Recurse -Name "knime.exe" -ErrorAction SilentlyContinue
```

## Examples

### General KNIME Execution Examples

#### Running a specific workflow:
```powershell
.\run_knime.ps1 -WorkflowPath "C:\MyWorkflows\DataProcessing" -WorkspacePath "C:\KnimeWorkspace"
```

#### Running with increased memory:
```powershell
.\run_knime.ps1 -AdditionalArgs "-vmargs -Xmx8g"
```

### Workflow-Specific Execution Examples

#### Execute OKTA workflow (your specific use case):
```powershell
# Advanced script with validation
.\run_knime_workflow.ps1 -WorkflowFile "C:\Users\sinra5\AppData\Local\Programs\KNIME\Workflow\OKTA.zip"

# Simple script for quick execution
.\run_knime_workflow_simple.ps1 "C:\Users\sinra5\AppData\Local\Programs\KNIME\Workflow\OKTA.zip"

# Batch file version
run_knime_workflow.bat "C:\Users\sinra5\AppData\Local\Programs\KNIME\Workflow\OKTA.zip"
```

#### Execute with custom KNIME path:
```powershell
.\run_knime_workflow.ps1 -WorkflowFile "OKTA.zip" -KnimePath "C:\CustomKNIME\knime.exe"
```

#### Execute without confirmation prompt:
```powershell
.\run_knime_workflow.ps1 -WorkflowFile "OKTA.zip" -Force
```

#### Execute with additional JVM memory:
```powershell
.\run_knime_workflow.ps1 -WorkflowFile "OKTA.zip" -AdditionalArgs "-vmargs -Xmx8g"
```

### Batch processing multiple workflows:
```powershell
# Create a wrapper script
$workflows = @(
    "C:\Workflows\OKTA.zip",
    "C:\Workflows\DataProcessing.zip",
    "C:\Workflows\Reporting.zip"
)

foreach ($workflow in $workflows) {
    Write-Host "Processing: $workflow"
    .\run_knime_workflow.ps1 -WorkflowFile $workflow -Force
}
```