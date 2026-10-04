$ErrorActionPreference = "Stop"

$ScriptsDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$VirtualEnvironment = Join-Path $ScriptsDirectory ".venv"
$PythonExecutable = Join-Path $VirtualEnvironment "Scripts\python.exe"
$ModelDirectory = Join-Path $ScriptsDirectory "docling-models"


function Invoke-PythonChecked {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$PythonArguments)
    & $PythonExecutable @PythonArguments
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed with exit code $LASTEXITCODE."
    }
}

if (-not (Test-Path -LiteralPath $PythonExecutable)) {
    $SystemPython = (Get-Command python -ErrorAction Stop).Source
    if (-not (Test-Path -LiteralPath $SystemPython)) {
        throw "No usable Python was found. Install Python 3.12 and rerun this setup script."
    }
    & $SystemPython -m venv $VirtualEnvironment
    if ($LASTEXITCODE -ne 0) {
        throw "Could not create the Python environment (exit code $LASTEXITCODE)."
    }
}

Invoke-PythonChecked -m pip install --upgrade pip
Invoke-PythonChecked -m pip install -r (Join-Path $ScriptsDirectory "requirements-conversion.txt")

$RequiredModelDirectories = @(
    "docling-project--docling-layout-heron",
    "docling-project--docling-layout-heron-onnx",
    "docling-project--docling-models",
    "RapidOcr"
)
$ModelsMissing = $false
foreach ($DirectoryName in $RequiredModelDirectories) {
    if (-not (Test-Path -LiteralPath (Join-Path $ModelDirectory $DirectoryName))) {
        $ModelsMissing = $true
    }
}

if ($ModelsMissing) {
    & $PythonExecutable -m docling.cli.tools models download layout tableformer rapidocr `
        --rapidocr-backend-lang "onnxruntime:en" `
        --output-dir $ModelDirectory
    if ($LASTEXITCODE -ne 0) {
        throw "Could not download the local Docling models (exit code $LASTEXITCODE)."
    }
}

Write-Output "PDF conversion environment is ready: $PythonExecutable"

