# Python tools

## Set up with Anaconda

Open **Anaconda Prompt**, change to the repository folder, and create the conda environment:

```bat
cd /d "C:\path\to\lit-survey"
conda env create -f Py-tools/environment.yml
conda activate literature-survey
```

The environment uses Python 3.12 and packages from conda-forge. It includes dependencies for PDF conversion, figure extraction, and the optional publication-carousel helper. No pip installation is needed.

For an existing environment, update it with:

```bat
conda env update -n literature-survey -f Py-tools/environment.yml
conda activate literature-survey
```

To add the packages manually to an existing Python 3.12 conda environment:

```bat
conda install -c conda-forge "docling>=2.126,<3" "rapidocr>=3.9,<4" onnxruntime pypdfium2 pymupdf pillow reportlab
```

Activate `literature-survey` each time you open a new prompt. All Python commands below use that active environment. To run from a script without activation, use `conda run -n literature-survey python ...`.

## Configure your library

Set `literature_root` in `Py-tools/project_config.json` to your paper library. Relative paths are resolved from `Py-tools`; the default `../literature` means a `literature` folder in the repository root. Create subject folders inside your library. Keep private papers and outputs out of the public repository.

## Download conversion models once

Docling converts PDFs locally and uses RapidOCR for image text. Download the layout, table, and English OCR models before conversion:

```bat
python -m docling.cli.tools models download layout tableformer rapidocr --rapidocr-backend-lang "onnxruntime:en" --output-dir Py-tools/docling-models
```

Downloads require internet access. Conversion uses these local models with remote services disabled and does not upload papers or require an OpenAI API key. Figure extraction does not need the models.

Windows PowerShell users can run `Py-tools/setup_conversion.ps1` after activating the conda environment. It checks the environment and downloads the models; it does not create another environment or install packages.

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

## Other Python helpers

After activating the same environment, run the rename-plan or publication-carousel helper in its skill folder with `python <script-path> --help` for options.

Package documentation: [Docling on conda-forge](https://anaconda.org/conda-forge/docling) and [Docling model-download CLI](https://docling-project.github.io/docling/reference/cli/).
