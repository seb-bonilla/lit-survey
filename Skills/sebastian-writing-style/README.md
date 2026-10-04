# Sebastian's Writing Style skill

This folder is a portable Codex skill for drafting and revising scientific documents in Sebastian's writing style. The skill contains no absolute file paths, external dependencies or computer-specific settings.

## What to copy

Copy the complete `sebastian-writing-style` folder. Keep its internal structure unchanged:

```text
sebastian-writing-style/
|-- SKILL.md
|-- README.md
|-- agents/
|   `-- openai.yaml
`-- references/
    `-- style-guide.md
```

The source PDFs and the reviewer skill used to derive the style are not required when using this skill.

## Install on Windows

1. Find the Codex skills directory. It is normally:

   ```text
   C:\Users\YOUR-USER-NAME\.codex\skills
   ```

   If the `CODEX_HOME` environment variable is set, use its `skills` subfolder instead.

2. Copy the complete folder into that directory. The result should be:

   ```text
   C:\Users\YOUR-USER-NAME\.codex\skills\sebastian-writing-style\SKILL.md
   ```

3. Restart Codex, or start a new Codex session, so that the skill catalogue is refreshed.

## Install on macOS or Linux

1. Copy the complete folder to:

   ```text
   ~/.codex/skills/sebastian-writing-style
   ```

   If `CODEX_HOME` is set, use `$CODEX_HOME/skills/sebastian-writing-style` instead.

2. Restart Codex, or start a new session.

## Install in another Codex instance

Transfer the folder by OneDrive, a USB drive, a private repository or another file-transfer method. On the destination computer, place it in that Codex installation's skills directory using the instructions above. Always copy the folder itself, not only `SKILL.md`, because the detailed style guide is stored in `references/style-guide.md`.

If the destination is managed by an organisation, local skill installation may be restricted. In that case, ask the Codex administrator where personal skills should be installed.

## Invoke the skill

Call it explicitly in a prompt:

```text
Use $sebastian-writing-style to revise the following introduction.
```

Other examples:

```text
Use $sebastian-writing-style to draft an abstract from these results.
```

```text
Use $sebastian-writing-style to make this proposal section more direct while preserving every target and citation.
```

```text
Use $sebastian-writing-style to rewrite this discussion for a materials-science audience. Do not change the scientific conclusions.
```

Codex may also select the skill automatically when a request explicitly asks for Sebastian's writing style.

## Updating the skill

Edit the master copy of this folder, then replace the complete installed folder on each computer. Keep the folder name and the `name` field in `SKILL.md` as `sebastian-writing-style`; this preserves the invocation `$sebastian-writing-style`.

When replacing an older version, close active Codex sessions first or restart them afterwards to ensure that cached skill instructions are refreshed.

## Relationship to the reviewer skill

This skill writes and revises prose. The separate `scientific-writing-review` skill diagnoses problems and produces reviewer comments without silently rewriting a student's work. Keep both installed if you want both behaviours:

- use `$sebastian-writing-style` to draft or revise text;
- use `$scientific-writing-review` to review a student's document and provide teaching comments.

