$ErrorActionPreference = "Stop"
$ScriptsDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$ModelDirectory = Join-Path $ScriptsDirectory "docling-models"

if (-not $env:CONDA_PREFIX) {
    throw "Activate your conda environment first: conda activate literature-survey"
}
$PythonExecutable = (Get-Command python -ErrorAction Stop).Source
& $PythonExecutable -c "import os, sys; from pathlib import Path; assert Path(sys.prefix).resolve() == Path(os.environ['CONDA_PREFIX']).resolve(), 'Python does not belong to the activated conda environment'; import docling, rapidocr, onnxruntime"
if ($LASTEXITCODE -ne 0) {
    throw "Check the active environment and install dependencies using Py-tools/environment.yml."
}

& $PythonExecutable -m docling.cli.tools models download layout tableformer rapidocr `
    --rapidocr-backend-lang "onnxruntime:en" `
    --output-dir $ModelDirectory
if ($LASTEXITCODE -ne 0) {
    throw "Could not download local conversion models (exit code $LASTEXITCODE)."
}
Write-Output "Local conversion models are ready. Environment: $env:CONDA_DEFAULT_ENV"
