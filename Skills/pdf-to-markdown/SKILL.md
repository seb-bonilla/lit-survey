---
name: pdf-to-markdown
description: Convert eligible PDFs of 30 pages or fewer in one top-level literature mother folder, including PDFs in nested folders, into a flat Markdown collection for LLM reading. Use AnyDoc for ordinary PDFs and local Docling with RapidOCR only for PDFs requiring OCR. Ignore documents longer than 30 pages. Do not use for paper summarisation or bibliographic renaming.
---

Resolve `<repository-root>` to this checkout. Read `Py-tools/project_config.json` there for `<literature-root>`; relative paths are relative to `Py-tools`. Use a separate local working directory for plans and caches. Resolve `<publication-root>` from the user only for publication tasks. If this skill is installed elsewhere, retain the checkout path in the student project context.


# PDF to Markdown

Accept one input: the mother folder, which must be an immediate child of the
configured literature project root.

From the repository root, run the converter with your configured Python environment:

```powershell
python Py-tools/convert_pdfs.py --folder "<subject folder>"
```

The converter searches the mother folder recursively but writes every result
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
discovery. Conversion is local and never enables
hosted OCR. If AnyDoc raises `NeedsOcrError`, the script retries that PDF with
Docling and RapidOCR. Docling model assets belong under the local
`Py-tools/docling-models`, never in the user profile cache
or the OneDrive literature folder. Report AnyDoc and OCR-fallback successes
separately, along with existing-file skips, long-document skips, and failed
counts.
