---
name: rename-literature-papers
description: Inspect extracted scientific-paper Markdown and rename matching PDF and Markdown pairs with consistent bibliographic filenames while preserving the literature folder structure. Use for literature-library cleanup, publisher-download filenames, DOI-style filenames, or requests to rename papers by year, authors, journal, and title phrase. Do not use for PDF conversion or paper summarisation.
---

Resolve `<repository-root>` to this checkout. Read `Py-tools/project_config.json` there for `<literature-root>`; relative paths are relative to `Py-tools`. Use a separate local working directory for plans and caches. If this skill is installed elsewhere, retain the checkout path in the student project context.


# Rename Literature Papers

Use Codex's model access to interpret the Markdown directly. Do not call the OpenAI API and do not require an API key.

## Input and pairing

Accept one mother folder that is an immediate child of the configured
configured literature root.

- Discover PDFs recursively below the mother folder, excluding its `markdown/`
  directory.
- Exclude files whose names begin with `REPEATED_`; these are deliberately
  retained intake duplicates and must not be renamed or paired.
- Ignore every PDF longer than 30 pages. Do not rename it or its Markdown, even
  when a Markdown file already exists from an earlier run.
- Read Markdown only from the mother folder's single flat `markdown/` directory.
- Reconstruct each expected Markdown filename with the same rule used by the
  PDF-to-Markdown skill: a unique PDF stem maps to `<stem>.md`; duplicate stems
  map to `<relative-parent-parts-joined-by-__>__<stem>.md`, using `root` for the
  mother folder itself.
- Rename only complete, unambiguous PDF/Markdown pairs. Report and skip an
  unpaired or ambiguous file.
- Keep every PDF in its existing parent directory and keep every Markdown file
  in the existing flat `markdown/` directory. Never create, remove, or move
  literature directories.

## Naming rule

Build one ASCII-safe stem in this form:

`YEAR_FirstAuthor_FinalAuthor_JOURNAL_Short-title-phrase`

Apply these constraints:

- Use the year of the formal journal citation, not submission or acceptance year.
- Use the surnames of the first and final authors in the paper's author list.
- Preserve compound surnames as one token, for example `DeWolf` or `MoralesMasis`.
- Use a recognisable journal or conference acronym containing at most 9 letters or digits.
- Use a meaningful six-to-eight-word phrase drawn from the paper title. Keep
  enough technical detail to distinguish related papers; omit filler words when
  possible.
- Use underscores between bibliographic fields and hyphens within the title phrase.
- Remove accents and filesystem-unsafe punctuation.
- Give the PDF and Markdown partner exactly the same stem.
- When two or more complete pairs resolve to the same bibliographic stem, keep
  the first pair at the base stem and append `_v2`, `_v3`, and so on to later
  copies. Apply the same versioned stem to both members of each pair. Do not
  skip a repeated paper merely because it shares a DOI or target stem.
- Treat a versioned duplicate as compliant when its stem follows the complete
  convention followed by `_v2` or a later numeric version.

Example:
`2019_Aydin_DeWolf_ADVFNMAT_Hydrogenated-indium-zinc-oxide-tandem-electrodes.pdf`

## Workflow

1. Inventory all recursive PDFs, record documents longer than 30 pages as
   ignored books, and reconstruct flattened Markdown partners only for PDFs of
   30 pages or fewer before making changes.
2. Read each Markdown file and locate the title, formal publication year,
   ordered author list, and journal name. Search throughout the file when the
   opening text is disordered.
3. If local evidence is insufficient, inspect the PDF title page and then an
   official publisher or DOI page. Never invent unsupported bibliographic facts.
4. Build every target stem in memory. Check for duplicate targets, existing
   destinations, Windows-reserved characters, and paths that would exceed safe
   Windows lengths. Assign `_v2`, `_v3`, and later numeric suffixes to repeated
   bibliographic records or other identical target stems. A filename that only
   resembles the convention is not complete: unless it exactly matches the
   required fields and title-word count (plus an optional duplicate suffix),
   rename it from the verified bibliographic evidence.
5. Apply the validated mappings directly using literal file paths. Recheck both
   destinations before each pair. Rename the PDF within its present directory
   and its Markdown partner within `markdown/`. If the second rename fails,
   restore the PDF's original name and report the failure. Never overwrite an
   existing file. Keep the old-to-new mapping available for recovery until all
   pairs have been verified; no separate Python helper is required.
6. Verify that all renamed pairs share a stem, that every PDF stayed in its
   original parent directory, and that no directory was added, removed, or
   renamed. Report completed, skipped, and failed counts.

Never create a rename log or other bookkeeping file in the literature folder.
Never overwrite an existing file, alter paper contents, or change the folder
structure.
