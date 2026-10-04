---
name: in-depth-paper-summary
description: Read a selected scientific paper using its Markdown text and PDF, present its abstract and a 200-word synthesis of the discussion and conclusions, and display complete figures with all panels together and embedded captions directly in Codex chat. Use for In-Depth Paper Summary requests; standalone figure extraction uses extract-paper-figures.
---

Resolve `<repository-root>` to this checkout. Read `Py-tools/project_config.json` there for `<literature-root>`; relative paths are relative to `Py-tools`. Use a separate local working directory for plans and caches. Resolve `<publication-root>` from the user only for publication tasks. If this skill is installed elsewhere, retain the checkout path in the student project context.


# In-Depth Paper Summary

Deliver a readable paper overview directly in chat. Default to one selected paper, its original abstract, a separate 200-word discussion-and-conclusions summary, and an inline gallery of all extracted figure images. The 200-word limit applies only to the synthesis, not the abstract or figure labels. Follow explicit user changes to length or scope.

## Sources

- Literature root: `<literature-root>`
- Figure skill: `../extract-paper-figures/SKILL.md`
- Temporary figure root: `<literature-root>/.literature-intake/temp_figs`

Resolve an exact path, title, or bibliographic stem to one paper. Use the paper already selected in the conversation when clear; ask for a selection only if none is available or multiple matches remain. Do not process the whole library or run intake.

Find the matching Markdown by stem, including a subject folder's `markdown` collection, and confirm title/authors against the PDF. Read the abstract, discussion, and conclusions in full, and enough results, methods, and captions to interpret the claims. If the paper has no separate discussion or conclusion heading, locate the equivalent passages. Check suspect OCR, numbers, symbols, or truncated passages against the PDF. If Markdown is missing, extract text from the selected PDF for this task; do not trigger batch conversion. If necessary passages are unreadable, explain what is missing rather than inventing a complete summary.

## Abstract and synthesis

Present the original abstract faithfully, repairing only extraction artefacts and retaining scientific notation. Clearly label it as the paper's abstract and cite the local source. If the paper has no abstract, say so; do not present an invented abstract as original. Respect applicable quotation constraints if only an external source is available.

Write a separate synthesis of exactly 200 words by default, counted as whitespace-separated words, excluding its label and source links. Verify the count before delivery. Use plain, precise scientific prose covering the central interpretation, main evidence, authors' conclusions, and material limitations or unresolved questions. Prioritise what the paper establishes and how far its conclusions extend; avoid generic background, unsupported mechanisms, and exaggerated implications. Distinguish the authors' interpretation from demonstrated results. Preserve quantities and units when they are important. Do not claim that absence of discussion proves absence of a limitation.

## Figures

Read and follow the figure skill for extraction, reuse, storage, verification, and replacement. Resolve its helper relative to that skill's directory, not the current working directory. Reuse existing outputs for the exact selected paper; regeneration requires the user's explicit request. Do not alter the paper or its source Markdown.

Enumerate actual generated image files in that paper's temporary folder. Show one complete image per numbered figure in numeric order, with all panels together and the caption included where available. Do not display legacy panel crops. Include graphical abstracts or other extracted images if present. Do not silently omit files or substitute a contact sheet for the originals. Flag extraction warnings or missing expected figures; describe these as all extracted images, not all paper figures unless coverage is verified.

Render each image in the final answer with Markdown image syntax and its absolute filesystem path, for example `![Figure 1](/absolute/path/to/Figure_01.jpeg)`. Use forward slashes and angle brackets around paths containing spaces. Display all images together in one uninterrupted gallery after the summary, using only short figure or panel labels. Keep captions inside the figure images where available; do not repeat them or insert explanatory prose between images unless requested. Retain caption files on disk for interpretation. Before delivery, compare the gallery against the complete-figure inventory; exclude legacy panel crops and duplicate crops of the same figure, and disclose coverage gaps. If the gallery exceeds message limits, deliver clearly numbered continuation messages until all images are displayed. A folder link alone is insufficient.

## Chat delivery

Start with the paper title and its citation details (journal, year, volume, pages or article number, and DOI when available), retaining clickable local PDF and Markdown links. Show only the first author and last author from the published author order, with their full names and clearly labelled roles. For each, show all affiliations attached to that author in the paper, matching the author superscripts to the affiliation entries; include the institution, department or laboratory, and location as supplied. Use affiliations at publication, not current affiliations. Do not list the intervening authors or substitute corresponding authors for the first and last authors. If both authors share an affiliation, it may be written once and explicitly marked as shared. For a single-author paper, show the author once. Verify names and affiliation mappings against the PDF when the Markdown is ambiguous; do not invent expanded names or missing affiliations, and state briefly when the source does not supply them. Follow with the abstract, the 200-word synthesis, and the image gallery. Keep extraction counts and any limitations brief. Deliver directly in chat; do not create a separate summary document unless requested. If one component is unavailable, still deliver the supported components and identify the gap.

