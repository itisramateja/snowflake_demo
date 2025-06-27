# KNIME Batch Application Scripts

This directory contains scripts to run KNIME in batch mode with the following parameters:
```
knime.exe -consoleLog -noexit -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION
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

- **`-consoleLog`**: Enables console logging output
- **`-noexit`**: Prevents KNIME from exiting immediately after execution
- **`-nosplash`**: Disables the splash screen for faster startup
- **`-application org.knime.product.KNIME_BATCH_APPLICATION`**: Runs KNIME in batch mode

## Additional Options

You can extend these scripts with additional KNIME parameters such as:
- `-workflowFile "path/to/workflow"`: Specify a workflow to execute
- `-data "path/to/workspace"`: Specify workspace directory
- `-reset`: Reset workspace
- `-vmargs -Xmx4g`: Set JVM memory options

## Troubleshooting

### Common Error: "knime is not recognized as the name of a cmdlet"

This error occurs when KNIME is not in your system PATH. Here are the solutions:

1. **Use the KNIME finder script**:
   ```powershell
   .\find_knime.ps1
   ```
   This will locate all KNIME installations and show you how to use them.

2. **Specify the full path to KNIME**:
   ```powershell
   .\run_knime.ps1 -KnimePath "C:\Program Files\KNIME\knime.exe"
   ```

3. **Add KNIME to your PATH** (permanent solution):
   - Open System Properties > Environment Variables
   - Add the KNIME directory to your PATH variable
   - Example: `C:\Program Files\KNIME`

### Other Common Issues

1. **"Execution Policy"**: Run `Set-ExecutionPolicy RemoteSigned` in PowerShell as Administrator
2. **"Access Denied"**: Run the script as Administrator if needed
3. **Memory Issues**: Add `-vmargs -Xmx4g` to increase memory allocation
4. **KNIME not installed**: Download from https://www.knime.com/downloads

### Finding KNIME Manually

If the scripts can't find KNIME, you can search manually:
```powershell
Get-ChildItem -Path "C:\Program Files*" -Recurse -Name "knime.exe" -ErrorAction SilentlyContinue
```

## Examples

### Running a specific workflow:
```powershell
.\run_knime.ps1 -WorkflowPath "C:\MyWorkflows\DataProcessing" -WorkspacePath "C:\KnimeWorkspace"
```

### Running with increased memory:
```powershell
.\run_knime.ps1 -AdditionalArgs "-vmargs -Xmx8g"
```

### Batch processing multiple workflows:
Create a wrapper script that calls the KNIME script multiple times with different workflow paths.