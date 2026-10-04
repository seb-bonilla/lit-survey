---
name: make-literature-survey
description: Create or update concise, scope-complete literature-survey.md files for selected mother folders in the configured literature root, using Sebastian's writing style and sections for their subfolders. Use for folder-level surveys, not individual-paper summaries or routine intake.
---

Resolve `<repository-root>` to this checkout. Read `Py-tools/project_config.json` there for `<literature-root>`; relative paths are relative to `Py-tools`. Use a separate local working directory for plans and caches. Resolve `<publication-root>` from the user only for publication tasks. If this skill is installed elsewhere, retain the checkout path in the student project context.


# Make Literature Survey

Create one short scientific survey per selected mother folder, comprehensive in scope rather than length.

## Scope and sources

Literature root: `<literature-root>`.
Output: `<mother folder>\literature-survey.md`.
Authoritative skill resources: `<repository-root>/Skills/make-literature-survey`.

Use explicitly selected folders or those clearly established in the conversation. For a survey requested after intake, use the mother folders that received papers. Ask for selection if none is established; do not default to the whole library. Use the selected folders; do not impose a fixed subject list or exclude a subject without the user choosing that scope.

Read and apply `../sebastian-writing-style/SKILL.md` and its referenced style guide.

Inspect the actual PDF folder tree and the mother's flat `markdown` directory. Map paper Markdown to source PDF locations to assign subfolder coverage. Exclude existing surveys and generated summaries from primary paper evidence.

Read every available paper Markdown in the selected mother folder, including papers whose PDFs are nested. Work in batches when needed; an inventory or abstracts alone do not count as reading the corpus. Check PDFs for missing text, extraction errors, ambiguous metadata and quantitative claims. Do not trigger batch conversion or renaming. Read additional local source text where practical, distinguishing books and theses from primary research. Disclose missing Markdown, inaccessible sources and subfolders containing only long documents rather than implying complete coverage.

Latest means latest supported by the local collection; do not imply global currency. External literature searching is additional scope when requested. Narrow DOI or publisher checks may resolve bibliographic uncertainty.

## Survey content

Use the established structure:

1. `# Literature survey: <subject>`.
2. A concise scope and state-of-the-art overview.
3. A section synthesising papers directly in the mother folder, when present.
4. One compact section per existing literature subfolder, including nested subject subfolders. Use actual names or clear relative paths. Exclude technical/output directories such as `markdown` and temporary figures.
5. A short outlook identifying limitations and unresolved research questions.

Prefer one short paragraph per section; add another only when scientific coverage requires it. No fixed total word count: length scales with the number of subjects. Synthesise approaches, classifications, established findings and recent progress rather than listing every paper. Describe sparse or unsupported sections briefly and explicitly.

Identify notable discoveries, quantitative advances and specific claims using verified filename-derived markers such as `[2026_Wang_Hao_NE]`: year, first author, final author, journal. Retain a version or distinguishing title fragment if otherwise ambiguous. Establish bibliographic identity from source text for noncompliant filenames; do not invent citations or rename papers.

Use British scientific English and Sebastian's direct, economical prose. Preserve quantities, units, conditions and caveats. Distinguish measured results from predictions, modelling and authors' interpretations. Avoid unsupported rankings, causal claims and novelty.

## Save and report

Create or update the selected folder's `literature-survey.md`. Read an existing survey first; preserve useful supported synthesis and user-specified additions, reconciling them with the corpus rather than appending disconnected updates.

Change only selected survey files. Preserve PDFs, paper Markdown and the folder structure. Keep temporary indexes and working files under `<working-directory>`, not the literature folders. Figure extraction and intake remain separate workflows; do not automatically run surveys after every intake unless that integration is requested.

Before delivery, check that all intended subject subfolders are represented, cited claims are supported, and coverage gaps are disclosed. Report clickable survey-file links, paper coverage per mother folder and material limitations.
