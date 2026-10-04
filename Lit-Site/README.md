# Lit-Site: turn your literature workbook into a website

This optional extension publishes the synthesis written in your Excel workbook's `Main` sheet. Continue collecting and verifying papers with the Python tools and Codex skills first. Excel remains your editable source; this extension reads it without changing it and generates `docs/index.md` for MkDocs.

MkDocs builds the website. Its built-in **Read the Docs theme** gives it a documentation layout. **GitHub Pages** and **Read the Docs** are separate hosting choices: both can build the files stored in your GitHub repository. Viewing a Markdown file on GitHub also works, but embedded interactive HTML figures need the built website.

## 1. Add the site dependencies to your existing environment

Open Anaconda Prompt at your repository root, the folder containing `Py-tools`, `Skills`, and `Lit-Site`:

```bat
cd /d "C:\path\to\lit-survey"
conda activate literature-survey
conda install -c conda-forge mkdocs openpyxl pyyaml
python -m pip check
```

Do not create a second environment or reinstall the PDF conversion stack. MkDocs builds and previews the site; openpyxl reads Excel. The Read the Docs theme is included with MkDocs. Docker, an API key, and a local web server installation are not needed.

If pip check reports a conflict after adding conda packages, resolve it before proceeding; your existing environment also contains pip-installed Docling. The lightweight site requirements file is for the hosted build, which does not install AnyDoc or Docling.

## 2. Prepare the Main sheet

Use the following layout. Keep the first row's B and C cells empty.

| Cell or row | Meaning |
| --- | --- |
| A1 | Page title |
| A populated, B empty, from row 2 | Section heading |
| A and B populated | Subsection heading in A, first paragraph in B |
| B populated, A empty | Another paragraph in the current section or subsection |
| C populated | Optional figure markers such as `Figure 1` or `Figure 1; Figure 2` |

Example:

| A | B | C |
| --- | --- | --- |
| My literature survey | | |
| Research question | | |
| | Explain your question and scope. | |
| Processing methods | Compare the reported methods, citing the supporting papers. | |
| | Describe disagreements and their experimental context. | Figure 1 |
| Open questions | | |
| | Identify the evidence needed next. | |

The generated page uses one title, section headings, and subsection headings. Paragraphs stay in row order, and figures appear after the text in their row. A C-only row places a figure at that position. You may use Markdown in paragraph cells for citations, links, lists, emphasis, and tables. Keep headings to a single line. Add retrievable source links yourself: the exporter does not invent references or resolve Paper IDs.

Use narrative text rather than formulas in A-C. The exporter rejects formulas because it does not calculate Excel or trust stale cached results. `Papers`, `Reported Data`, and `Notes` are left untouched and are not exported by this first version.

## 3. Generate the page

Save your workbook in Excel first. Its path can be anywhere on your computer; site generation does not use `Py-tools/project_config.json`.

```bat
python Lit-Site/build_site.py "C:\path\to\literature.xlsx"
```

This regenerates `Lit-Site/docs/index.md`. Do not edit that generated page to maintain your survey: update `Main` and regenerate. Other documentation pages are not overwritten. Use `--sheet "Other sheet"` if your narrative sheet has a different name.

If column C already has figures and you want to try only the text first:

```bat
python Lit-Site/build_site.py "C:\path\to\literature.xlsx" --skip-figures
```

The page explicitly marks omitted figures. Review those notes before publishing.

## 4. Add figures when useful

Figures are optional. They can be approved images from `temp_figs`, your own comparison plots, or self-contained HTML exported from Plotly. This extension does not digitise plots, run figure generators, or grant permission to reproduce a publisher's image.

Copy `Lit-Site/figures.example.json` to `Lit-Site/figures.json` and replace its sample entry with real file paths and captions. Add one entry for each marker in column C:

```json
{
  "Figure 1": {
    "file": "C:/Research/figures/comparison.png",
    "caption": "Figure 1. Comparison of verified observations, with source references."
  }
}
```

Use forward slashes in JSON paths, or escape each backslash. Relative paths are resolved from the JSON file's folder. Supported files are PNG, JPEG, SVG, WebP, GIF, and HTML. For HTML plots, export a standalone file with its JavaScript included; linked companion files are not copied automatically.

```bat
python Lit-Site/build_site.py "C:\path\to\literature.xlsx" --figures Lit-Site/figures.json
```

Selected assets are copied to `Lit-Site/docs/assets/figures`. Missing mappings or files produce an error rather than silently dropping a figure. Renaming or changing a source file does not update the copied asset until you regenerate. Old unused assets remain: review and remove obsolete exports before publishing, particularly if a figure should no longer be public.

## 5. Preview and build locally

From the repository root in the activated environment:

```bat
python -m mkdocs serve -f Lit-Site/mkdocs.yml
```

Open `http://127.0.0.1:8000/`. Stop the preview with Ctrl+C. Check headings, paragraph order, citations, figures, and links.

To build static HTML:

```bat
python -m mkdocs build --strict -f Lit-Site/mkdocs.yml
```

Output goes into `Lit-Site/site`, which is ignored by Git. You can also append `--build` to the exporter command to generate Markdown and build HTML together. Change `site_name` in `Lit-Site/mkdocs.yml` to your survey's name.

## 6. Publish the reviewed exports

Keep your working workbook private and backed up. Commit the source scripts, configuration, and reviewed files in `Lit-Site/docs`; do not commit the workbook, licensed PDFs, or `Lit-Site/site`. An ignored workbook does not make exported text or figures private. The hosting services read the committed exports, so they never need your workbook or conversion models.

The templates below are inactive until you copy them into your student repository. Choose one host and check its configuration before publishing.

### GitHub Pages

1. Copy `Lit-Site/templates/github-pages.yml` to `.github/workflows/literature-site.yml` at your repository root.
2. Commit your reviewed docs and the workflow, then push your publishing branch.
3. In the GitHub repository, open Settings → Pages and select GitHub Actions as the source.
4. In Actions, select Publish literature site and use Run workflow on the branch containing your exports.

The supplied template runs manually to let you review updates before publishing. It builds only this extension with MkDocs and deploys the static output. Later you can add a push trigger if you want automatic publication. See [GitHub's Pages workflow guide](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

### Read the Docs hosting

1. Copy `Lit-Site/templates/readthedocs.yaml` to `.readthedocs.yaml` at the repository root.
2. Commit that file and your reviewed exports, then push them.
3. Import your GitHub repository into Read the Docs and select the branch you want it to build.
4. Start a build and check its logs and site URL. Read the Docs builds may run automatically on subsequent pushes to configured branches.

The template points to `Lit-Site/mkdocs.yml` and installs only the hosted site requirements. The service uses its own build environment; your local work still uses `literature-survey`. See [the official MkDocs integration guide](https://docs.readthedocs.com/platform/stable/intro/mkdocs.html).

## Maintain the site

Update and verify the workbook → regenerate Markdown and assets → preview → review the Git diff → commit and publish. Local preview does not publish anything. Never rely on a website build to check scientific claims.

For extension checks, run `python -m unittest discover -s Lit-Site/tests -v` in the activated environment.
