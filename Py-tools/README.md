# Python tools

Run these commands from the repository root. Use Python 3.12 and a fresh environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r Py-tools/requirements-conversion.txt
python -m pip install -r Py-tools/requirements-figures.txt
```

Set `literature_root` in `project_config.json` to your paper library. Relative paths are resolved from `Py-tools`; the default `../literature` means a `literature` folder in the repository root. Create subject folders inside your library. Do not commit private papers or generated outputs.

## PDF to Markdown

```powershell
python Py-tools/convert_pdfs.py --list-folders
python Py-tools/convert_pdfs.py --folder "My subject" --dry-run
python Py-tools/convert_pdfs.py --folder "My subject"
```

Searches the selected immediate child folder recursively and writes a flat `markdown` folder there. Repeated stems get folder prefixes. Existing Markdown is preserved unless `--overwrite` is requested. PDFs longer than 30 pages and `REPEATED_` files are skipped; these limits do not define your research scope.

Ordinary conversion uses local AnyDoc. OCR fallback uses local Docling/RapidOCR. Before OCR, download the models:

```powershell
python -m docling.cli.tools models download layout tableformer rapidocr --rapidocr-backend-lang "onnxruntime:en" --output-dir Py-tools/docling-models
```

Windows users can instead run `Py-tools/setup_conversion.ps1` to create a tool-local environment, install conversion dependencies, and download the models. Use its `.venv/Scripts/python.exe` for conversion afterwards. Model downloads need internet access; paper conversion is local. No OpenAI API key is needed.

## Extract complete figures

```powershell
python Py-tools/extract_figures.py --pdf "path/to/paper.pdf"
python Py-tools/extract_figures.py --pdf "path/to/paper.pdf" --output-root "path/to/figures"
```

The default output is `<literature-root>/.literature-intake/temp_figs/<paper-stem>/Figure_01/`, with a complete JPEG and `caption.txt`. An explicit output root works without library configuration. Existing output is preserved; `--replace` deletes and regenerates only that paper's output folder, so use it only deliberately.

Crops are heuristic. Inspect panels, axes, legends, captions, and warnings against the PDF. These tools do not digitise plots or populate Excel.
