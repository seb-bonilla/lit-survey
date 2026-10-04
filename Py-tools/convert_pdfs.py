"""Recursively convert PDFs in a configured library or any selected folder to Markdown."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
SCRIPTS_ROOT = SCRIPT_PATH.parent
PROJECT_CONFIG = SCRIPTS_ROOT / "project_config.json"
OUTPUT_DIRECTORY_NAME = "markdown"
DOCLING_MODELS_DIR = SCRIPTS_ROOT / "docling-models"
MAX_PAGES = 30


def load_project_root() -> Path:
    try:
        config = json.loads(PROJECT_CONFIG.read_text(encoding="utf-8"))
        configured_root = Path(config["literature_root"]).expanduser()
        project_root = (configured_root if configured_root.is_absolute() else PROJECT_CONFIG.parent / configured_root).resolve()
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            f"Could not read literature_root from {PROJECT_CONFIG}"
        ) from exc
    if not project_root.is_dir():
        raise RuntimeError(f"Configured literature root does not exist: {project_root}")
    return project_root


def native_path(path: Path) -> str:
    """Return a Windows extended path when needed for long filenames."""
    value = str(path.resolve())
    if os.name == "nt" and not value.startswith("\\\\?\\"):
        return "\\\\?\\" + value
    return value


def configure_console() -> None:
    """Allow scientific filenames with Unicode characters on Windows."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


EXCLUDED_DIRECTORIES = {"markdown", "temp_figs", "docling-models", ".git", ".venv", "__pycache__"}


def top_level_folders(root: Path) -> list[Path]:
    return sorted(
        (path for path in root.iterdir() if path.is_dir()
         and not path.name.startswith(".")
         and path.name.casefold() not in EXCLUDED_DIRECTORIES),
        key=lambda path: path.name.casefold(),
    )


def resolve_selected_folder(folder_name: str) -> Path:
    if folder_name.casefold() == "root":
        return load_project_root()
    selected = Path(folder_name).expanduser()
    # Explicit paths never require configuration. Bare names select library subjects.
    explicit_path = (selected.is_absolute() or folder_name in {".", ".."}
                     or "/" in folder_name or "\\" in folder_name
                     or folder_name.startswith("~"))
    candidate = selected.resolve() if explicit_path else (load_project_root() / selected).resolve()
    if not candidate.is_dir():
        raise ValueError(f"Folder does not exist: {candidate}")
    return candidate


def pdf_files_in(folder: Path) -> list[Path]:
    # Prune derived output at every level, including when selecting the library root.
    pdf_files: list[Path] = []
    for directory, child_dirs, filenames in os.walk(native_path(folder), followlinks=False):
        child_dirs[:] = [name for name in child_dirs
                         if name.casefold() not in EXCLUDED_DIRECTORIES]
        for filename in filenames:
            if Path(filename).suffix.casefold() != ".pdf" or filename.casefold().startswith("repeated_"):
                continue
            value = os.path.join(directory, filename)
            if value.startswith("\\\\?\\"):
                value = value[4:]
            pdf_files.append(Path(value))
    return sorted(pdf_files, key=lambda path: str(path.relative_to(folder)).casefold())


def output_jobs(folder: Path, pdf_files: list[Path]) -> list[tuple[Path, Path]]:
    output_dir = folder / OUTPUT_DIRECTORY_NAME
    by_stem: dict[str, list[Path]] = defaultdict(list)
    for pdf_file in pdf_files:
        by_stem[pdf_file.stem.casefold()].append(pdf_file)

    jobs: list[tuple[Path, Path]] = []
    for pdf_file in pdf_files:
        if len(by_stem[pdf_file.stem.casefold()]) == 1:
            output_name = f"{pdf_file.stem}.md"
        else:
            relative_parent = pdf_file.parent.relative_to(folder)
            prefix = "__".join(relative_parent.parts) if relative_parent.parts else "root"
            output_name = f"{prefix}__{pdf_file.stem}.md"
        jobs.append((pdf_file, output_dir / output_name))

    target_counts = Counter(output.name.casefold() for _, output in jobs)
    collisions = sorted(name for name, count in target_counts.items() if count > 1)
    if collisions:
        raise ValueError(
            "flattened output names are still ambiguous: " + ", ".join(collisions)
        )
    return jobs


def pdf_page_count(pdf_file: Path) -> int:
    """Return a PDF's page count without extracting or altering its contents."""
    import pypdfium2

    document = pypdfium2.PdfDocument(native_path(pdf_file))
    try:
        return len(document)
    finally:
        document.close()


def print_folder_inventory(root: Path) -> None:
    files = pdf_files_in(root)
    direct = [path for path in files if path.parent == root]
    print(f"Root: {root}")
    print(f"  root: {len(direct)} direct PDF(s), {len(files)} recursive PDF(s)")
    for path in direct:
        print(f"    {path.name}")
    print("Subject folders:")
    for folder in top_level_folders(root):
        print(f"  {folder.name}: {len(pdf_files_in(folder))} recursive PDF(s)")
    print("Counts exclude generated folders and REPEATED_ files; page limits are checked during conversion.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Recursively convert PDFs in a selected folder into "
            "one flat Markdown directory."
        )
    )
    parser.add_argument(
        "--folder",
        metavar="NAME_OR_PATH",
        help="root, a configured subject name, or any absolute/explicit relative folder path",
    )
    parser.add_argument(
        "--list-folders",
        action="store_true",
        help="list the configured root (or --folder path), direct PDFs, and subject folder counts",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would be converted without writing files",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="replace Markdown files that already exist",
    )
    parser.add_argument(
        "--skip-rel",
        action="append",
        default=[],
        metavar="PATH",
        help=(
            "skip one PDF path relative to the selected mother folder; may be "
            "repeated for a file whose conversion was already attempted and failed"
        ),
    )
    return parser


def load_anydoc():
    try:
        import anydoc
    except ImportError as exc:
        raise RuntimeError(
            "AnyDoc is not installed. Activate literature-survey and run "
            "python -m pip install firecrawl-anydoc==0.2.4"
        ) from exc
    return anydoc


def load_docling_converter():
    """Build a local PDF converter with RapidOCR and project-scoped models."""
    if not DOCLING_MODELS_DIR.is_dir():
        raise RuntimeError(
            "Docling models are missing. Run the model-download step described "
            f"in {SCRIPTS_ROOT / 'README.md'}."
        )

    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

    try:
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import (
            PdfPipelineOptions,
            RapidOcrOptions,
        )
        from docling.document_converter import DocumentConverter, PdfFormatOption
    except ImportError as exc:
        raise RuntimeError(
            "Docling with RapidOCR is not installed. Create and activate the "
            "conda environment described in Py-tools/README.md."
        ) from exc

    pipeline_options = PdfPipelineOptions(
        artifacts_path=DOCLING_MODELS_DIR,
        do_ocr=True,
        enable_remote_services=False,
        ocr_options=RapidOcrOptions(
            backend="onnxruntime",
            lang=["en"],
        ),
    )
    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )


def convert_with_docling(converter, pdf_file: Path) -> str:
    result = converter.convert(source=Path(native_path(pdf_file)))
    markdown = result.document.export_to_markdown()
    if not markdown.strip():
        raise RuntimeError("Docling returned empty Markdown")
    return markdown


def write_markdown_atomic(output_file: Path, markdown: str) -> None:
    output = native_path(output_file)
    temporary = output + ".tmp"
    with open(temporary, "w", encoding="utf-8") as handle:
        handle.write(markdown)
    os.replace(temporary, output)


def convert_folder(
    folder: Path,
    *,
    dry_run: bool,
    overwrite: bool,
    skip_relative: list[str] | None = None,
) -> int:
    pdf_files = pdf_files_in(folder)
    output_dir = folder / OUTPUT_DIRECTORY_NAME

    if not pdf_files:
        print(f"No PDFs found in: {folder}")
        return 0

    try:
        all_jobs = output_jobs(folder, pdf_files)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    jobs: list[tuple[Path, Path]] = []
    skipped = 0
    skipped_long: list[tuple[str, int]] = []
    page_count_failures: list[tuple[str, str]] = []
    requested_skips: list[tuple[str, str]] = []
    skip_keys = {
        str(Path(value)).replace("/", "\\").casefold()
        for value in (skip_relative or [])
    }
    for pdf_file, output_file in all_jobs:
        source = str(pdf_file.relative_to(folder))
        if source.replace("/", "\\").casefold() in skip_keys:
            reason = "previous conversion attempt did not complete"
            requested_skips.append((source, reason))
            print(f"SKIP requested after failure: {source}")
            continue
        try:
            pages = pdf_page_count(pdf_file)
        except Exception as exc:
            page_count_failures.append(
                (source, f"{type(exc).__name__}: {exc}")
            )
            print(f"FAILED page count: {source}: {type(exc).__name__}: {exc}")
            continue
        if pages > MAX_PAGES:
            skipped_long.append((source, pages))
            print(f"SKIP long document ({pages} pages): {source}")
            continue
        if os.path.isfile(native_path(output_file)) and not overwrite:
            print(f"SKIP existing: {output_file.name}")
            skipped += 1
            continue
        jobs.append((pdf_file, output_file))

    top_level_count = sum(pdf.parent == folder for pdf in pdf_files)
    duplicate_pdf_count = sum(
        count for count in Counter(pdf.stem.casefold() for pdf in pdf_files).values() if count > 1
    )
    print(f"Selected folder: {folder}")
    print(
        f"Found: {len(pdf_files)} PDF(s) "
        f"({top_level_count} top-level, {len(pdf_files) - top_level_count} nested)"
    )
    print(f"Output: {output_dir}")
    if duplicate_pdf_count:
        print(f"Disambiguated: {duplicate_pdf_count} PDF(s) with duplicate stems")

    if dry_run:
        for pdf_file, output_file in jobs:
            source = pdf_file.relative_to(folder)
            print(f"WOULD CONVERT: {source} -> {output_file.name}")
        print(
            f"Dry run complete: {len(jobs)} to convert, {skipped} existing skipped, "
            f"{len(skipped_long)} long documents ignored, "
            f"{len(page_count_failures)} page-count failures"
        )
        return 0

    if not jobs:
        print(
            f"Nothing to do: 0 converted, {skipped} existing skipped, "
            f"{len(skipped_long)} long documents ignored, "
            f"{len(page_count_failures)} page-count failures"
        )
        return 1 if page_count_failures else 0

    try:
        anydoc = load_anydoc()
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    output_dir.mkdir(exist_ok=True)

    converted_anydoc = 0
    converted_ocr = 0
    docling_converter = None
    docling_load_error = None
    failures: list[tuple[str, str]] = list(page_count_failures) + requested_skips
    for pdf_file, output_file in jobs:
        source = str(pdf_file.relative_to(folder))
        engine = "AnyDoc"
        try:
            # No hosted OCR options: AnyDoc reads text locally without ML models.
            markdown = anydoc.to_markdown(native_path(pdf_file))
            if not isinstance(markdown, str) or not markdown.strip():
                raise RuntimeError("AnyDoc returned empty or invalid Markdown")
        except Exception as anydoc_exc:
            print(f"FALLBACK Docling/RapidOCR: {source}: {type(anydoc_exc).__name__}: {anydoc_exc}")
            try:
                # Load expensive models only once, and only after a failed AnyDoc attempt.
                if docling_load_error is not None:
                    raise RuntimeError(docling_load_error)
                if docling_converter is None:
                    try:
                        docling_converter = load_docling_converter()
                    except Exception as exc:
                        docling_load_error = f"{type(exc).__name__}: {exc}"
                        raise
                markdown = convert_with_docling(docling_converter, pdf_file)
                engine = "Docling/RapidOCR"
            except Exception as ocr_exc:
                reason = (f"AnyDoc: {type(anydoc_exc).__name__}: {anydoc_exc}; "
                          f"Docling/RapidOCR: {type(ocr_exc).__name__}: {ocr_exc}")
                failures.append((source, reason))
                print(f"FAILED: {source}: {reason}")
                continue

        try:
            write_markdown_atomic(output_file, markdown)
        except Exception as exc:
            # A disk error must not trigger another expensive conversion.
            reason = f"Save failed: {type(exc).__name__}: {exc}"
            failures.append((source, reason))
            print(f"FAILED: {source}: {reason}")
            continue
        if engine == "AnyDoc":
            converted_anydoc += 1
        else:
            converted_ocr += 1
        print(f"OK {engine}: {source} -> {output_file.name}")

    print(
        f"Complete: {converted_anydoc} via AnyDoc, {converted_ocr} via Docling/RapidOCR, "
        f"{skipped} existing skipped, "
        f"{len(skipped_long)} long documents ignored, {len(failures)} failed"
    )
    if failures:
        print("Files needing attention:")
        for filename, reason in failures:
            print(f"  {filename}: {reason}")
        return 1
    return 0


def main() -> int:
    configure_console()
    args = build_parser().parse_args()
    if not args.folder and not args.list_folders:
        build_parser().error("provide --folder NAME_OR_PATH or --list-folders")
    try:
        folder = resolve_selected_folder(args.folder) if args.folder else load_project_root()
    except (ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    if args.list_folders:
        print_folder_inventory(folder)
        return 0

    return convert_folder(
        folder,
        dry_run=args.dry_run,
        overwrite=args.overwrite,
        skip_relative=args.skip_rel,
    )


if __name__ == "__main__":
    raise SystemExit(main())
