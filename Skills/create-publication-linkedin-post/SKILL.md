---
name: create-publication-linkedin-post
description: Prepare LinkedIn publication posts in Sebastian Bonilla's voice, with a journal-header cover, complete paper figures, an upload-ready PDF carousel, paper links and evidence-based tagging suggestions. Use for selected publications, not automatic processing of the library or publishing to LinkedIn.
---

Resolve `<repository-root>` to this checkout. Read `Py-tools/project_config.json` there for `<literature-root>`; relative paths are relative to `Py-tools`. Use a separate local working directory for plans and caches. Resolve `<publication-root>` from the user only for publication tasks. If this skill is installed elsewhere, retain the checkout path in the student project context.


# Publication LinkedIn materials

Create a reviewable publication pack for a paper selected by Sebastian. His publication library is `<publication-root>`. Infer a paper from author, journal, year and topic when unambiguous; confirm the actual title, DOI and publication dates from its contents.

## Voice and evidence

Read `$sebastian-writing-style` and its full style guide. Read [references/linkedin-voice.md](references/linkedin-voice.md) for the social genre. This adapts the scientific style to Sebastian's warm public voice; it does not alter the shared writing-style skill.

Read the complete abstract, relevant methods and results, discussion, conclusions, authors, affiliations, contribution statement and acknowledgements. Keep a short claim-to-source record in the publication pack. Distinguish results from interpretations, device performance from implied performance, and new work from prior literature. Do not invent student milestones, personal anecdotes, novelty, author contributions or future impact. Distinguish online-first from issue dates; avoid stale 'just published' language.

Draft one copy-ready post in British English, normally 180–230 words including acknowledgements, organisation names, the paper link and hashtags. Treat this as a guide, not a reason to omit essential scientific qualifications. Sebastian found the 307-word Sharpe trial too long: keep background and methods to one short paragraph, use two or three concise findings, and finish with one bounded takeaway and collaborator thanks. Start with warm recognition of the lead researcher when appropriate. Use short paragraphs and occasional diamond bullets, as in Sebastian's example. Put the DOI link and a small relevant hashtag set at the end. Count words before delivery and trim repetition and secondary details. Save plain text; show the finished post in a social-post writing block in chat.

## Figures and carousel

Use `$extract-paper-figures` on the selected PDF, including one from PublishedPapers: the user's publication workflow explicitly extends its source-library scope. For this workflow, Sebastian explicitly requests all outputs inside PublishedPapers/temp, overriding that skill's fixed Literature Intake output root. Run its helper with `--output-root <publication-pack>/raw-figures`; it creates a paper-stem subfolder containing figures and captions. Reuse existing outputs and respect its replacement/deletion rules. If an earlier extraction exists in Literature Intake, copy it into the pack's raw-figures directory and preserve the original. Keep upload-ready images separate from raw candidates.

Check detected captions against the PDF. The extraction helper can mistake prose such as 'Fig. 2(b) shows' or 'Fig. 9 shows' for captions. Reject those candidates from the upload set, retain the raw outputs, and report the discrepancy. Inspect every accepted full figure for clipping, adjacent prose, missing legends or lost panel labels. Repair incorrect crops from the source page, preserving the raw extraction. Include all main-paper figures; obtain supplementary figures only when requested and clearly state their coverage. Keep complete figures even if optional panel crops are useful. Do not automatically split complicated panel arrangements.

Create a cover by rendering a crop of the actual first-page journal masthead, journal-cover thumbnail, complete title, authors and affiliations. Inspect the crop boundaries rather than guessing or recreating journal branding. Omit the abstract and body prose. Make each subsequent carousel page one complete figure, with white margins and its original labels, legends and axes. Add no explanatory prose to figure pages. Preserve aspect ratios and use a common page size suited to the figures.

Read the PDF skill before producing the carousel. The bundled `scripts/build_carousel.py` takes a selected source PDF, an inspected header rectangle and the accepted figure images in order; it creates uniform upload images and a PDF. It refuses existing output names. Use an explicit crop rectangle in PDF points, and pass Figure 2's validated filename if the raw helper has generated duplicates. Its output never implies crop validation: inspect the cover and every rendered PDF page before delivering.

## Links and tags

Use the printed DOI as the canonical paper link and verify online metadata when accessible. Add publisher, repository or public full-text links only after checking their identity and access. Never invent a shortened link or describe a paper as open access without evidence.

Recommend the lead author first, then major contributors identified in the contribution statement, followed by other co-authors. List every co-author and every collaborating organisation from the paper, including non-university research centres. Separate optional funder/laboratory acknowledgements from author affiliations. Search LinkedIn or official institutional pages for matching people and organisations. Verify identities through affiliation or a contextual tag from an institutional or collaborator post, rather than name alone. If no reliable profile is found, retain the name with 'select manually; profile unverified'. Do not make up handles. Plain text names do not become active LinkedIn mentions: tell the user to select the matching accounts in the composer.

## Save and deliver

Save all generated outputs under `<publication-library>\temp\<year>-<lead-author>-<short-topic>\`: `post.txt`, `publication-notes.md` (bibliography, links, tags with evidence, claim checks, coverage and upload order), `images\` (cover and complete figures), `carousel.pdf`, and `raw-figures\` (original crops and captions). Keep assembly scratch files in a separate `qa\` subfolder within that pack so the images directory contains only upload files. Keep source publications untouched. Revisions use a new version or only overwrite artifacts the user has asked to revise. When asked to relocate an existing pack, move it into temp and update recorded paths.

Deliver the post, a direct carousel link, the tag priorities and an uninterrupted gallery with the cover and complete figures. When using the extraction skill, also satisfy its gallery inventory requirement for raw outputs, clearly labelling rejected automatic crops. Explain concrete coverage gaps. Do not upload or publish merely because a pack has been requested.
