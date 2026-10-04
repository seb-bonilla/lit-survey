# Python tools

## Set up with Anaconda

Open **Anaconda Prompt**, change to the repository folder, and create the conda environment:

```bat
cd /d "C:\path\to\lit-survey"
conda env create -f Py-tools/environment.yml
conda activate literature-survey
python -m pip check
```

The environment uses Python 3.12. Conda installs Python and the figure-extraction dependencies from conda-forge, then automatically runs pip **inside that same environment** to install Docling and its RapidOCR dependencies. There is no separate virtual environment or additional pip command to run for the setup above.

This mixed setup is needed on Windows because Docling depends on `docling-parse`, which is not available as a Windows conda-forge package. Do not add Docling to the conda dependency list; it belongs in the YAML file's `pip` section.

For an existing environment, update it with:

```bat
conda env update -n literature-survey -f Py-tools/environment.yml
conda activate literature-survey
```

If you prefer to install manually, activate your Python 3.12 conda environment first, then run these commands in order:

```bat
conda install -c conda-forge pip pypdfium2 pymupdf pillow
python -m pip install "docling[rapidocr]>=2.126,<3"
python -m pip check
```

Activate `literature-survey` each time you open a new prompt. All Python commands below use that active environment. To run from a script without activation, use `conda run -n literature-survey python ...`.

## Configure your library

Set `literature_root` in `Py-tools/project_config.json` to your paper library. Relative paths are resolved from `Py-tools`; the default `../literature` means a `literature` folder in the repository root. Create subject folders inside your library. Keep private papers and outputs out of the public repository.

## Download conversion models once

**Docling** is the Python library that converts PDFs. It uses downloaded models to recognise page layout, tables, and text in images. **Docker is not required**: the tools run directly in your conda environment.

After creating the environment, run the following in **Anaconda Prompt**. Start in the repository root: the folder containing `Py-tools` and `Skills`, not inside `Py-tools`.

```bat
cd /d "C:\path\to\lit-survey"
conda activate literature-survey
python -m docling.cli.tools models download layout tableformer rapidocr --rapidocr-backend-lang "onnxruntime:en" --output-dir Py-tools/docling-models
```

Replace the example path with your repository's location. The command runs Docling's download utility using Python from the active conda environment. It saves the layout, table, and English OCR models in `Py-tools/docling-models` beneath the current folder. Wait for the command to finish successfully before converting papers. You normally need to do this only once per computer; repeat it if the models are removed or a dependency update requires new models.

The download needs internet access and may take several minutes. Subsequent conversion uses the saved models locally with remote services disabled. It does not upload papers or require an OpenAI API key. Figure extraction does not need these models.

### Windows PowerShell alternative

Use **Anaconda PowerShell Prompt**, or a Windows PowerShell session where `conda activate` already works. After creating the environment, run:

```powershell
Set-Location "C:\path\to\lit-survey"
conda activate literature-survey
python -m docling.cli.tools models download layout tableformer rapidocr --rapidocr-backend-lang "onnxruntime:en" --output-dir Py-tools/docling-models
```

If ordinary PowerShell does not recognise conda, use Anaconda Prompt instead. The Python download command is identical in both shells; only the command for changing folders differs.

Alternatively, from that same repository folder and activated PowerShell environment, run `./Py-tools/setup_conversion.ps1`. This helper checks the environment and downloads the same models. It does not create another environment or install packages. If PowerShell blocks the helper script, use the Python command above.

## PDF to Markdown

```bat
python Py-tools/convert_pdfs.py --list-folders
python Py-tools/convert_pdfs.py --folder "My subject" --dry-run
python Py-tools/convert_pdfs.py --folder "My subject"
```

The converter searches the selected immediate child folder recursively and writes a flat `markdown` folder there. Repeated stems receive folder prefixes. Existing Markdown is preserved unless `--overwrite` is requested. PDFs longer than 30 pages and `REPEATED_` files are skipped; these limits do not define your research scope.

Inspect the output against the original PDF, especially equations, symbols, tables, and reading order. Existing conversions are retained even if created with a different converter.

## Extract complete figures

```bat
python Py-tools/extract_figures.py --pdf "path/to/paper.pdf"
python Py-tools/extract_figures.py --pdf "path/to/paper.pdf" --output-root "path/to/figures"
```

The default output is `<literature-root>/.literature-intake/temp_figs/<paper-stem>/Figure_01/`, containing a complete JPEG and `caption.txt`. An explicit output root works without library configuration. Existing output is preserved; `--replace` deletes and regenerates only that paper's output folder, so use it deliberately.

Crops are heuristic. Inspect panels, axes, legends, captions, and warnings against the PDF. These tools do not digitise plots or populate Excel.

Package documentation: [Docling installation](https://docling-project.github.io/docling/getting_started/installation/) and [Docling model-download CLI](https://docling-project.github.io/docling/reference/cli/).
