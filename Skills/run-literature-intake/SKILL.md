---
name: run-literature-intake
description: Process new scientific papers from the fixed Literature Intake folder through PDF conversion, bibliographic renaming, duplicate checking, autonomous subject classification, relocation, verification, and a concise intake report. Use when the user asks to run or process the literature intake. Do not use for maintenance of an arbitrary mother folder.
---

Resolve `<repository-root>` to this checkout. Read `Py-tools/project_config.json` there for `<literature-root>`; relative paths are relative to `Py-tools`. Use a separate local working directory for plans and caches. If this skill is installed elsewhere, retain the checkout path in the student project context.


# Run Literature Intake

Process everything eligible in the fixed intake folder and file it into the existing literature collection.

## Fixed locations

- Literature root: `<literature-root>`
- Intake mother folder: `.literature-intake`
- Temporary figures: `.literature-intake\temp_figs`
- Workflow resources: `<working-directory>`

Do not interpret a different folder as the intake unless the user explicitly overrides the location.

## Required sequence

1. Read and apply `$pdf-to-markdown` to `.literature-intake`.
   - Search recursively for PDFs, excluding `markdown`, `temp_figs`, and files beginning `REPEATED_`.
   - Ignore PDFs longer than 30 pages.
   - Preserve existing usable Markdown.
   - Use local AnyDoc first; retry failed or empty conversions with local Docling/RapidOCR from the activated conda environment.
2. Read and apply `$rename-literature-papers` to `.literature-intake`.
   - Rename every complete eligible pair to `YEAR_FirstAuthor_FinalAuthor_JOURNAL_six-to-eight-word-title-phrase`.
   - Give repeated bibliographic records or target stems `_v2`, `_v3`, and later suffixes; never discard a duplicate merely because it is repeated.
   - Treat an already compliant matching pair as complete.
3. Check each renamed paper against the existing collection outside `.literature-intake` using title, DOI, bibliographic identity, and, when useful, file hash or text evidence.
4. Read the title, abstract, keywords, and enough paper content to select the best existing subject mother folder and subfolder. Prefer the most specific established destination. Make the decision autonomously unless two materially different destinations remain equally plausible or no suitable folder exists.
5. Before moving, check destination collisions. If the same bibliographic stem already exists, preserve both records by assigning the incoming pair the next available `_vN` suffix.
6. Move the PDF into the selected existing subject folder or subfolder. Move its Markdown partner into the destination mother folder's single flat `markdown` folder. Create only that required `markdown` folder if the destination mother does not yet have one; do not create new subject categories.
7. Verify the PDF and Markdown exist at their destinations with identical stems before processing the next paper.

## Invariants

- Do not alter PDF or Markdown contents during renaming or relocation.
- Do not overwrite any file.
- Do not create, remove, rename, or reorganize subject folders.
- Do not place Markdown beside a nested PDF; keep it in the destination mother's flat `markdown` folder.
- Leave ignored books, explicitly `REPEATED_` files, unpaired files, and genuinely ambiguous papers in intake and report them.
- Keep rename plans, DOI caches, and other working files under your working directory, never in the literature collection.
- Figure extraction is not part of routine intake. Leave `temp_figs` unchanged unless the user separately invokes `$extract-paper-figures`.

## Final report

Provide one table with:

- full title
- final bibliographic filename
- approximately 100-word abstract summary
- duplicate-check result
- destination mother folder (the exact top-level subject folder name)
- destination PDF subfolder (the full relative subfolder path beneath that mother folder; write `Mother-folder root` if filed directly in it)
- final PDF destination as a clickable absolute file link
- final Markdown destination as a clickable absolute file link
- uncertainty or action required

Show these as explicit table columns so the filing location is readable without opening a link. Report actual verified destinations after filing, not proposed locations. For papers left in intake, identify `.literature-intake` as the current mother folder, give their current subfolder and available file links, and state why they were not filed. The Markdown destination remains the mother's flat `markdown` folder even when the PDF is filed in a subject subfolder.

Then report conversion totals split by AnyDoc and Docling/RapidOCR, existing Markdown skips, long-document skips, conversion or rename failures, unpaired or ambiguous files, and confirmation that the existing folder structure was preserved.
