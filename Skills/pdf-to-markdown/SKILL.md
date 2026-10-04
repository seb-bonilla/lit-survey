---
name: pdf-to-markdown
description: Convert eligible PDFs of 30 pages or fewer in a selected library root, subject folder, or explicit folder path, including nested PDFs, into a flat Markdown collection for LLM reading. Use local AnyDoc first and Docling/RapidOCR only if AnyDoc fails or returns empty text, in the activated conda environment. Ignore documents longer than 30 pages. Do not use for paper summarisation or bibliographic renaming.
---

Resolve `<repository-root>` to this checkout. Read `Py-tools/project_config.json` there for `<literature-root>`; relative paths are relative to `Py-tools`. Use a separate local working directory for plans and caches. If this skill is installed elsewhere, retain the checkout path in the student project context.


# PDF to Markdown

Select `root` for the configured library, a subject name, or an absolute/explicit relative folder path. Explicit paths do not require project_config.json.

From the repository root, activate the conda environment described in Py-tools/README.md and run:

```powershell
python Py-tools/convert_pdfs.py --folder "<subject folder>"
```

The converter searches the selected folder recursively but writes every result
into its single `markdown/` directory. It does not reproduce nested folders.
PDFs longer than 30 pages are treated as books and ignored. Report them as
long-document skips; do not convert, rename, move, or delete them, and do not
remove Markdown that may already exist for them.
Unique PDF stems become `<stem>.md`. When several PDFs have the same stem, it
prefixes each output with its relative parent path, for example
`InO__paper.md` and `SnO__paper.md`, so flattening never overwrites a result.

Existing Markdown files are skipped unless the user explicitly asks to
regenerate them; then add `--overwrite`. Files whose names begin with
`REPEATED_` are deliberately retained intake duplicates and are excluded from
discovery. Conversion uses local AnyDoc without OCR first. Retry only failed or empty conversions using local Docling/RapidOCR; never enable hosted OCR. Models are needed only for that fallback; download them as described in `Py-tools/README.md`. Models belong in `Py-tools/docling-models`. Report AnyDoc and Docling/RapidOCR successes separately, existing-file skips, long-document skips, and failures.

