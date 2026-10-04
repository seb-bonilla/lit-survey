# Starting and maintaining your literature survey

Build a literature survey that helps you answer a research question, compare evidence, and identify what to investigate next. Keep the original papers, a structured Excel database, and your developing conclusions connected so that every important claim can be checked and updated.

This guide adapts the [Project 1 manual](https://github.com/seb-bonilla/literature-site/blob/main/manual.md) and the supplied Project 1 and Project 2 contexts and skills. The supplied `izro_literature.xlsx` and `izro_literature_v2.xlsx` workbooks are motivating examples: its materials-science properties illustrate the structure, but your own database should use fields appropriate to your question.

## 1. Define what you need to learn

Write your main research question in one or two sentences. Add subquestions and identify the observations that would help answer them. Agree on an initial scope: topics, methods, date range, and reasons for including or excluding papers.

For example, a survey of zirconium-doped indium oxide could ask how deposition and annealing affect electrical and optical properties. Useful fields might include composition, thickness, processing conditions, mobility, carrier concentration, and measurement method. Another topic will need different fields.

Start with a small batch of important papers. Test the database structure before extracting a large collection.

## 2. Search, collect, and prioritise

Search your institution's literature databases and publisher sources using topic names, abbreviations, synonyms, properties, methods, and applications. Include reviews, foundational work, recent studies, and results that challenge an emerging conclusion. Follow both references and later citing papers.

Keep a dated search log with the source, exact query, filters, useful results, and inclusion decisions. Keep a reading queue with priority, full-text availability, reading status, and next action. Deduplicate by DOI and title. A saved PDF does not mean its evidence has been checked.

Store original PDFs locally and use a reference manager if it helps manage citations. Triage papers by reading the title, abstract, figures, tables, and conclusions, then inspect methods and relevant results. Spend detailed extraction time on papers that address your questions.

## 3. Make Excel your working database

Use the example workbook to understand the division of responsibilities. Preserve an existing workbook's headers, units, identifiers, and formatting rather than imposing a new layout.

| Sheet | What belongs here | Row rule |
| --- | --- | --- |
| `Papers` | Bibliography, DOI, local source paths, relevance, reading status, and next action | One publication per row |
| `Reported Data` | Measurements, sample identity, processing and measurement conditions, units, uncertainty, and source location | One distinct observation or condition per row |
| `Notes` | Concise findings, authors' explanations, limitations, contradictions, and open questions | Follow the established paper-level layout |
| `Main` (optional) | Your developing synthesis and, in the website example, narrative and figure placement | Follow the example's narrative structure |

Use stable Paper IDs and reuse them exactly across sheets. The extraction skills commonly use `FirstAuthor_Year`, with suffixes where needed; retain your workbook's existing convention. Observation IDs such as `O1`, `O2`, and `O3` must remain unique across `Reported Data`.

Put one numeric quantity in each numeric cell. Define units in headers or dedicated fields and document conversions. Leave unreported values blank; zero means a reported zero. Record at least the Paper ID, page or figure/table/panel, sample or condition, and evidence type for each important observation.

Distinguish author-reported numbers, digitised graphical estimates, calculated quantities, and interpretations. Calculations need valid inputs, a documented formula, and units. Do not carry physical relationships from the IZrO example into another topic without checking their applicability.

## Choose the tools that fit your library

Project 1 provides a small student workflow: PDF conversion, paired renaming, figure extraction, calibrated digitisation, and extraction into Excel. Project 2 provides a more developed subject-organised library workflow. Combine its library management with Project 1's database work; Project 2 does not supply the Excel extraction or digitisation skills.

| Need | Skill or helper | Source |
| --- | --- | --- |
| Process and file incoming papers | `run-literature-intake` | Project 2 |
| Convert a subject folder, with local OCR when needed | `pdf-to-markdown` | Project 2 |
| Give PDF/Markdown pairs bibliographic names | `rename-literature-papers` | Both projects; conventions differ |
| Extract complete figures from a selected paper | `extract-paper-figures` | Project 2 |
| Read a selected paper with a synthesis and figure gallery | `in-depth-paper-summary` | Project 2 |
| Create or update a survey of selected subject folders | `make-literature-survey` | Project 2 |
| Digitise selected plots with calibration and source checks | `digitize-figure-data` | Project 1 |
| Add or enrich a paper in Excel | `extract-paper-info` | Project 1 |
| Revise scientific prose consistently | `sebastian-writing-style` | Project 2 |

Use a simple layout when beginning: `literature/` for PDFs, its `markdown/` and `figures/` subfolders for derived sources, `data/literature.xlsx` for the database, and `records/` for searches and reading actions. Project 1's helper commands use that layout once the helpers and dependencies are supplied:

```powershell
python convert_pdfs.py --folder literature
python extract_figures.py --folder literature --pdf 2024_Smith
```

For a larger existing collection, Project 2 uses top-level subject folders (called mother folders), nested PDF categories, and one flat `markdown/` directory per mother. Its `.literature-intake` folder receives new papers; operational helpers, plans, and caches live in a separate local scripts folder. Configure the library and scripts paths before use. Its packaged skills retain source-computer paths, and changing configuration alone does not repair every reference. Follow its migration instructions and test one paper before batch processing.

Project 2 intake converts, renames, checks duplicates, and files pairs into existing categories. It preserves repeated files and does not create new subject categories automatically. Its conversion and naming workflows skip documents longer than 30 pages and deliberately retained `REPEATED_` files; report those gaps and read relevant long documents separately. Those limits are implementation choices, not literature inclusion criteria.

Choose one naming convention for your project. Project 1 uses a short two-to-four-word title phrase; Project 2 uses six-to-eight words and `_v2`, `_v3` suffixes for collisions. Both require verified publication metadata and preserve paired files. Database deduplication remains separate: preserving two source files does not justify inserting the same publication twice into `Papers`.

Routine intake does not automatically extract figures, summarise papers, update Excel, or write folder surveys. Request those stages when useful. A folder survey describes the available local collection; it does not establish that the global literature is current or exhaustively covered.

## 4. Process one paper from source to verified record

The following tools are available in the source projects. This guidance file does not install or bundle them. Check the scripts and skills supplied with your chosen project before running commands: the original website and portable starter use different library paths and converter options.

| Stage | Tool | What you must inspect |
| --- | --- | --- |
| Convert PDF text to Markdown | `convert_pdfs.py` | Tables, symbols, equations, and reading order against the PDF; scanned papers may need OCR |
| Rename paired files | `rename-literature-papers` skill | Bibliographic metadata, matching PDF/Markdown names, and the rename log |
| Extract figures and captions | `extract_figures.py` | Complete axes, legends, captions, and panels against the original figure |
| Recover useful plotted values | `digitize-figure-data` skill with WebPlotDigitizer | Axis calibration, linear/log scales, series identity, units, and graphical precision |
| Populate Excel | `extract-paper-info` skill | Duplicate handling, source locations, values, conditions, IDs, and formatting |

Rename before extracting figures so that source paths remain consistent. Prefer reported tables or downloadable numerical data to digitising the same evidence. Digitise only quantitative plots that contribute to your questions; retain the CSV and calibration note beside the image.

Once the project skills are installed, example requests are:

```text
$rename-literature-papers rename matching PDF and Markdown pairs in [library path].

$digitize-figure-data digitize [figure image path] and cross-check against [paper Markdown path].

$extract-paper-info add [paper Markdown path] to [workbook path], preserving its existing schema and using [CSV path] where relevant.
```

Make a recoverable workbook backup before editing. Check DOI and Paper ID before insertion; enrich an existing record rather than creating a duplicate. Paper extraction should update `Papers`, `Reported Data`, and `Notes`; changing `Main` is a separate synthesis task.

Read the methods, results, and limitations yourself. Compare the saved entries with the original PDF before marking them verified. Converted text and AI-generated summaries are aids to reading; the original source supports the scientific claim.

## 5. Turn records into understanding

Keep three levels explicit: what was measured, how the authors explain it, and what you conclude after comparing studies. Write short, source-linked notes that can be revised independently. Where the example uses knowledge-nugget columns, use concise standalone findings, preferably fewer than 30 words each.

Compare observations only after checking definitions, units, sample preparation, and measurement conditions. Use filters and reproducible plots to answer specific questions. Investigate outliers and disagreements in the source papers before drawing conclusions or averaging results.

Record missing evidence and conflicting explanations. Update your synthesis with supporting and contradicting Paper IDs. Let these gaps determine the next searches.

## 6. Maintain a regular cycle

Choose a manageable cadence, such as a weekly session:

1. Repeat useful searches and follow citations; record the date and coverage.
2. Deduplicate new papers and update the reading queue.
3. Read and extract the most relevant papers.
4. Check new entries and correct earlier mistakes, recording what changed and why.
5. Revisit notes, comparisons, contradictions, and open questions.
6. Save a dated database backup and commit meaningful changes to workflow files.

Keep private workbooks and licensed PDFs in backed-up storage. Git only preserves files that are tracked: an ignored workbook needs its own backup and transfer plan. When moving computers, transfer the private sources and database separately and recreate the Python environment from dependency files.

The initial intensive survey can finish when repeated searches mostly return known work and the remaining gaps become specific. Record a research map: key papers, comparable observations, supported conclusions, unresolved disagreements, and the next experiments or searches. Continue maintaining it as the project develops. Describe your actual search coverage; do not call an informal survey exhaustive or systematic.

## 7. Share a website when it becomes useful

The [literature-site example](https://github.com/seb-bonilla/literature-site/) adds Python-generated figures, searchable CSV tables, MkDocs, and GitHub Pages. Excel remains the editable source; website files are regenerated outputs. Website publication is optional for establishing and maintaining the database.

Before sharing, check values and provenance, figure labels, links, and generated tables. Review the exported content as well as the workbook: excluding the workbook from Git does not keep its exported data private. Publish only material intended for sharing, and keep licensed source PDFs outside the public repository.

## A paper is ready to use when

- Its bibliography is verified and duplicate records have been checked.
- Important observations include units, conditions, and retrievable evidence locations.
- Digitised and calculated values are labelled with their provenance.
- Notes separate reported findings, author interpretation, and your synthesis.
- Unresolved checks and next actions are recorded.
- The saved workbook reopens correctly and you have checked the entries against the source.

For the complete source workflow, consult the [Project 1 manual](https://github.com/seb-bonilla/literature-site/blob/main/manual.md) and [project context](https://github.com/seb-bonilla/literature-site/blob/main/PROJECT_CONTEXT.md). The manual describes both general survey practice and a specific website implementation; adapt its fields and tools to your own research.

