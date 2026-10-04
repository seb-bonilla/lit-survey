# Starting and maintaining your literature survey

Use your literature survey to answer a research question, compare evidence, and identify what to investigate next. Keep the original papers, an Excel database, and your developing conclusions connected so that important claims can be checked and updated.

## 1. Start with a question

Write your main research question in one or two sentences. Add a few subquestions and decide which measurements, methods, or findings would help answer them. Set an initial scope and clear reasons for including or excluding papers.

Begin with a small batch of important papers. Use them to test your database structure before collecting large amounts of data.

## 2. Find and organise papers

Search using topic names, synonyms, methods, properties, and applications. Include reviews, foundational papers, recent studies, and contradictory results. Follow references and papers that cite useful studies.

Keep two simple records:

- A search log: date, search source, query, filters, and useful results.
- A reading queue: paper, priority, reading status, and next action.

Save original PDFs and use a reference manager if helpful. Check DOI and title to avoid duplicate records. Read the abstract, figures, tables, and conclusions first, then decide which papers deserve detailed reading.

## 3. Build your Excel database

Use separate sheets for different kinds of information:

| Sheet | Purpose |
| --- | --- |
| `Papers` | One row per publication: citation, DOI, source file, relevance, and reading status |
| `Reported Data` | One row per distinct observation or experimental condition: values, units, methods, conditions, and source location |
| `Notes` | Concise paper-level findings, interpretations, limitations, and open questions |
| `Main` (optional) | Your synthesis across papers: supported conclusions, disagreements, and research gaps |

The IZrO example workbook illustrates this structure. Adapt the property columns to your own topic.

Give each paper a stable Paper ID and reuse it across sheets. Give each observation a unique ID. Put one number in each numeric cell, define the units, and leave unreported values blank. A blank is different from a reported zero.

Record the source page, figure, table, or panel for important observations. Keep sample preparation and measurement conditions with the values. Label digitised estimates and calculated quantities clearly; document conversions and calculations.

## 4. Read and extract one paper at a time

A practical sequence is:

1. Convert the PDF to Markdown if this helps you read or extract its content. Check tables, symbols, and equations against the PDF. Scanned papers may need OCR.
2. Give the PDF and Markdown matching, consistent names based on verified citation details.
3. Read the methods, relevant results, figures, and limitations.
4. Extract useful observations into Excel, keeping units, conditions, and source locations.
5. Write concise notes that distinguish reported findings from the authors' explanations and your own interpretation.
6. Check the saved entries against the original paper before marking them verified.

Prefer author-reported numbers or downloadable data. When useful values appear only in a graph, digitise the plot with calibrated axes and retain the CSV, series labels, units, and calibration notes. Use precision appropriate to the image.

## 5. Use tools to help

Python helpers and Codex skills can assist with repetitive work. Use the tools you have installed and check their setup instructions before processing a large library.

| Task | Relevant skill |
| --- | --- |
| Convert PDFs to readable text | `pdf-to-markdown` |
| Rename matching PDF and Markdown files | `rename-literature-papers` |
| Check and file incoming papers | `run-literature-intake` |
| Extract figures and captions | `extract-paper-figures` |
| Read a paper with a summary and figure gallery | `in-depth-paper-summary` |
| Digitise quantitative plots | `digitize-figure-data` |
| Add or update paper records in Excel | `extract-paper-info` |
| Draft or update a survey of selected folders | `make-literature-survey` |

For example, once the relevant skill is installed:

```text
$extract-paper-info add [paper path] to [workbook path], preserving its existing structure and recording evidence locations.
```

Back up the workbook before editing. Update existing paper records rather than inserting duplicates. AI-assisted extraction still needs your verification against the source.

## 6. Compare and maintain

Compare results only after checking units, definitions, methods, and conditions. Use filters and plots to answer specific questions. Investigate unusual points and disagreements before drawing conclusions.

Set aside regular time to:

- Search for new papers and update the reading queue.
- Extract and verify the most relevant evidence.
- Correct earlier entries and record why they changed.
- Revise notes, comparisons, and research gaps.
- Save a dated database backup and record meaningful workflow changes in Git.

Keep private databases and licensed PDFs in backed-up storage. Git does not back up files excluded from the repository. Share only material intended for public use.

The initial survey has reached a useful stopping point when you can explain the main findings, the strength of their evidence, the unresolved questions, and what to investigate next. Continue updating that understanding throughout your research.
