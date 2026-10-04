---
name: extract-paper-figures
description: Extract complete figures with all panels together and captions included in the figure image from a selected scientific PDF. Use when the user asks to see, inspect, or extract figures from a particular literature paper. Store every output only in the literature root temporary-figures folder; do not run automatically for all intake papers.
---

Resolve `<repository-root>` to this checkout. Read `Py-tools/project_config.json` there for `<literature-root>`; relative paths are relative to `Py-tools`. Use a separate local working directory for plans and caches. If this skill is installed elsewhere, retain the checkout path in the student project context.


# Extract Paper Figures

Use this skill only for papers the user selects. Figure extraction is an optional follow-up to the intake workflow, not an automatic intake step.

## Fixed locations

- Literature root: `<literature-root>`
- Temporary output root: `<literature-root>/temp_figs`
- Helper: `<repository-root>/Py-tools/extract_figures.py`
- Python: `Python from the activated literature-survey conda environment`

Never place extracted figures in a subject mother folder or its `markdown` folder.

## Workflow

1. Resolve the requested paper to exactly one PDF under the literature root. Accept an exact path, bibliographic stem, or unambiguous title. Ignore PDFs already inside `temp_figs`.
2. Find the matching Markdown by stem when it exists. Use it to confirm figure numbering and captions when the PDF extraction is ambiguous.
3. Run `python Py-tools/extract_figures.py --pdf <absolute-pdf-path>` from the repository root.
4. Inspect the reported warnings and a sample of the JPEGs. Keep all panels together in one image per numbered figure. Include the original caption in the same crop when possible. Check for clipped panels or captions, body-text false matches and repeated captions. When a caption continues elsewhere, assemble the continuation into the same image or report the limitation. Never invent missing caption text.
5. Report the output folder, complete-figure count, caption coverage, and any figures or captions that need manual attention.

## Output layout

Use the paper's exact current stem:

```text
temp_figs\
  <paper-stem>\
    Figure_01\
      Figure_01.jpeg
      caption.txt
```

The complete figure JPEG is mandatory and should contain the caption below the full figure. Do not create separate panel images. Keep caption.txt for interpretation and recovery. Do not create manifests or bookkeeping files.

## Safety and replacement

- Do not overwrite an existing paper output. If it exists, report it and reuse it.
- Use `--replace` only after the user explicitly asks to regenerate that paper's figures.
- Delete a selected paper's temporary figure folder, or clear `temp_figs`, only on an explicit user request. Resolve and verify the exact path remains beneath the fixed temporary output root before deletion.
- Do not alter the source PDF or any Markdown.

## Display in chat

Display one complete image per numbered figure in numeric order with absolute Markdown image paths. Reuse existing complete figures without showing legacy panel crops. Do not regenerate old outputs unless requested. Flag old images without embedded captions, extraction gaps or incomplete crops. Keep labels short; caption text belongs inside the image and in caption.txt, not repeated between images.
