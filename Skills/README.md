# Skills

Each folder contains `SKILL.md` and any required scripts, references, and agent metadata. Keep the complete folder when installing a skill.

This directory is a distribution catalogue. To use skills in Codex, copy the desired complete folders into your student project's `.agents/skills/` directory or your configured personal skills directory. Merely keeping them in `Skills` does not install them. Keep this repository checkout available: PDF conversion and figure extraction use its `Py-tools` scripts. Record its absolute location and your library location in the student project context.

Configure `Py-tools/project_config.json` and install the relevant dependencies first. Start with one paper. Source files, reading outputs, and private workbooks belong to the student's collection, not this public catalogue.

## Literature workflow

- `pdf-to-markdown`: local text conversion and OCR fallback.
- `rename-literature-papers`: verified bibliographic naming of PDF/Markdown pairs.
- `run-literature-intake`: conversion, naming, duplicate checks, and filing into existing subject folders.
- `extract-paper-figures`: complete figures and captions for a selected paper.
- `in-depth-paper-summary`: a selected paper's synthesis and figure gallery.
- `make-literature-survey`: evidence-based surveys of selected subject folders.
- `sebastian-writing-style`: concise scientific writing with its full style guide.

## Optional supporting skills

- `research-project-brief`: research briefs from notes.
- `meeting-summary`: structured summaries of meeting transcripts.
- `create-publication-linkedin-post`: draft publication posts and figure packs; does not publish automatically. Its carousel helper additionally needs `reportlab`, PyMuPDF, and Pillow.

Example after installation:

```text
$pdf-to-markdown convert the subject folder "My subject" using [repository path].
$in-depth-paper-summary read [paper path].
$make-literature-survey update the survey for "My subject".
```

Skills assist reading and library maintenance. These skills do not provide Excel extraction or calibrated plot digitisation; verify scientific claims against the original papers.
