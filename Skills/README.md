# Skills

Each folder contains `SKILL.md` and any required scripts, references, and agent metadata. Keep the complete folder when installing a skill.

This directory is a distribution catalogue. To use skills in Codex, copy the desired complete folders into your student project's `.agents/skills/` directory or your configured personal skills directory. Merely keeping them in `Skills` does not install them. Keep this repository checkout available: PDF conversion and figure extraction use its `Py-tools` scripts. Record its absolute location and your library location in the student project context.

Create and activate the `literature-survey` conda environment using [the Python tools setup](../Py-tools/README.md), then configure `Py-tools/project_config.json`. Start with one paper. Source files, reading outputs, and private workbooks belong to the student's collection, not this public catalogue.

## Literature workflow

- `pdf-to-markdown`: local Docling conversion with OCR when needed.
- `rename-literature-papers`: verified bibliographic naming of PDF/Markdown pairs.
- `run-literature-intake`: conversion, naming, duplicate checks, and filing into existing subject folders.
- `extract-paper-figures`: complete figures and captions for a selected paper.
- `in-depth-paper-summary`: a selected paper's synthesis and figure gallery.
- `make-literature-survey`: evidence-based surveys of selected subject folders.

Example after installation:

```text
$pdf-to-markdown convert the subject folder "My subject" using [repository path].
$in-depth-paper-summary read [paper path].
$make-literature-survey update the survey for "My subject".
```

Skills assist reading and library maintenance. These skills do not provide Excel extraction or calibrated plot digitisation; verify scientific claims against the original papers.
