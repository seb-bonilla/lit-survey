---
name: meeting-summary
description: Scan a meetings folder for unsummarized meeting transcripts and create copy-ready plain-text executive summaries with an email draft, discussion summary, and action points with owners.
metadata:
  short-description: Summarize meeting transcripts into email-ready text files
---

# Meeting Summary

Use this skill when the user asks to run a meeting-summary workflow on a folder of transcript files.

## Outcome

For each transcript text file that does not already have a matching summary, create a sibling file named `<original_stem>_executive_summary.txt`.

The output must contain these sections in this order:

EMAIL DRAFT
EXECUTIVE SUMMARY
MAIN DISCUSSION SUMMARY
MAIN ACTION POINTS

## Workflow

1. Identify the meetings folder from the user request, current project, or available workspace context. If no folder is specified, use the current project folder and inspect it before asking a question.
2. Scan for transcript files, normally `.txt` files. Skip files whose names end in `_executive_summary.txt`, API-key files, caches, and other obvious generated files.
3. Process only transcripts without a matching `_executive_summary.txt` output. Do not overwrite existing summaries unless the user explicitly asks to regenerate them.
4. Read the complete transcript. For long files, use a reliable chunking or large-context approach and preserve enough context for a final cross-check.
5. Produce the four required sections. The email draft comes first and must be directly copyable into an email.
6. Save the output beside the source transcript using UTF-8 plain text.
7. Verify that the output exists, the sections are in the required order, and no unsummarized transcripts remain.

## Accuracy rules

- Distinguish agreed decisions from proposals, questions, hypotheses, literature findings, examples, and personal opinions.
- Do not invent attendees, decisions, deadlines, quantities, technical details, or action owners.
- Record an owner only when the transcript clearly assigns or accepts the action. Otherwise write `Owner: Not specified`.
- Preserve terminology used in the transcript. Do not silently rename materials, devices, processes, or abbreviations.
- If statements conflict, use the later or clearly agreed conclusion only when supported by the transcript; otherwise describe the issue as unresolved.
- Preserve important numbers and units, but do not turn approximate or illustrative values into firm decisions.

## Plain-text format

- Use ordinary text suitable for copying into an email or text file.
- Do not use Markdown, LaTeX, HTML, asterisks, dollar signs, backticks, or decorative rules.
- Use numbered items or lines beginning with `- ` for lists.
- Use ASCII punctuation where practical to avoid encoding corruption.

## LLM/API route

Prefer the project's configured local script or available LLM/API integration. If an API key is available, keep it outside prompts and source-controlled files. If no API route is available, summarize directly with the current Codex model. Do not invent or expose credentials.

## Completion response

Report the created files as clickable absolute paths and state whether any unsummarized transcripts remain. If a file is unavailable because of a lock, sync, or permission problem, report the exact file and stop rather than silently skipping it.
