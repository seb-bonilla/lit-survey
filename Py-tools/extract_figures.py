"""Extract caption-associated figures from a scientific PDF as temporary JPEGs."""
from __future__ import annotations
import argparse, json, re, shutil
from pathlib import Path
import pymupdf as fitz
from PIL import Image

CONFIG_PATH = Path(__file__).resolve().parent / "project_config.json"

def default_output_root():
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        configured = Path(config["literature_root"]).expanduser()
        root = (configured if configured.is_absolute() else CONFIG_PATH.parent / configured).resolve()
    except (OSError, KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f"Set literature_root in {CONFIG_PATH}, or pass --output-root") from exc
    if not root.is_dir():
        raise SystemExit(f"Literature root does not exist: {root}; configure it or pass --output-root")
    return root / "temp_figs"

CAPTION_RE = re.compile(r"^\s*(?:fig(?:ure)?\.?|scheme)\s*([A-Z]?\d+)(?:\.(?!\d)|\s+(?=(?-i:[A-Z])|\())", re.I)

def caption_blocks(page):
    found = []
    for block in page.get_text("blocks"):
        text = " ".join(str(block[4]).split())
        if CAPTION_RE.match(text): found.append((text, fitz.Rect(block[:4])))
    return sorted(found, key=lambda item: (item[1].y0, item[1].x0))

def visual_rects(page, cap):
    candidates, page_rect = [], page.rect
    for block in page.get_text("dict").get("blocks", []):
        if block.get("type") == 1:
            rect = fitz.Rect(block["bbox"])
            if rect.y1 <= cap.y0 + 3 and rect.get_area() < page_rect.get_area() * .85: candidates.append(rect)
    for drawing in page.get_drawings():
        rect = fitz.Rect(drawing["rect"])
        if rect.y1 <= cap.y0 + 3 and rect.get_area() > 16: candidates.append(rect)
    return candidates

def associated_clip(page, cap):
    candidates = visual_rects(page, cap)
    if candidates:
        group = [max(candidates, key=lambda rect: rect.y1)]
        changed = True
        while changed:
            changed = False
            union = fitz.Rect(group[0])
            for rect in group[1:]: union |= rect
            expanded = fitz.Rect(union.x0-30, union.y0-30, union.x1+30, union.y1+30)
            for rect in candidates:
                if rect not in group and (expanded.intersects(rect) or abs(rect.y1-union.y0) < 24):
                    group.append(rect); changed = True
        clip = fitz.Rect(group[0])
        for rect in group[1:]: clip |= rect
        clip |= cap
        return fitz.Rect(clip.x0-12, clip.y0-12, clip.x1+12, clip.y1+8) & page.rect, False
    top = max(page.rect.y0, cap.y0 - min(360, page.rect.height*.48))
    if cap.width < page.rect.width*.72: left, right = max(page.rect.x0, cap.x0-18), min(page.rect.x1, cap.x1+18)
    else: left, right = page.rect.x0+18, page.rect.x1-18
    return fitz.Rect(min(left, cap.x0), top, max(right, cap.x1), min(page.rect.y1, cap.y1+8)), True

def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--pdf", required=True, type=Path); parser.add_argument("--output-root", type=Path, default=None); parser.add_argument("--dpi", type=int, default=300); parser.add_argument("--replace", action="store_true"); args = parser.parse_args()
    pdf = args.pdf.resolve()
    if not pdf.is_file() or pdf.suffix.lower() != ".pdf": raise SystemExit(f"PDF not found: {pdf}")
    output_root = (args.output_root if args.output_root is not None else default_output_root()).resolve(); paper_dir = (output_root/pdf.stem).resolve()
    if output_root not in paper_dir.parents: raise SystemExit("Unsafe output path")
    if paper_dir.exists():
        if not args.replace: raise SystemExit(f"Output already exists: {paper_dir}")
        shutil.rmtree(paper_dir)
    paper_dir.mkdir(parents=True); complete = panels = fallbacks = 0; doc = fitz.open(pdf)
    seen = set()
    for page_number, page in enumerate(doc, start=1):
        for caption, cap_rect in caption_blocks(page):
            match = CAPTION_RE.match(caption); label = match.group(1) if match else str(complete+1); safe = re.sub(r"[^A-Za-z0-9]+","",label).zfill(2); folder = paper_dir/f"Figure_{safe}"; version = 2
            while folder.exists(): folder = paper_dir/f"Figure_{safe}_v{version}"; version += 1
            if safe in seen:
                print(f"WARNING: repeated caption for figure {label} on page {page_number}; inspect for continuation")
                continue
            seen.add(safe)
            folder.mkdir(); clip, fallback = associated_clip(page, cap_rect); scale = args.dpi/72; pix = page.get_pixmap(matrix=fitz.Matrix(scale,scale), clip=clip, alpha=False); image = Image.frombytes("RGB",(pix.width,pix.height),pix.samples).convert("RGB"); base = folder.name
            image.save(folder/f"{base}.jpeg","JPEG",quality=95,subsampling=0); (folder/"caption.txt").write_text(caption+f"\n\n[PDF page {page_number}]\n",encoding="utf-8"); complete += 1; fallbacks += int(fallback)
    doc.close()
    if complete == 0: paper_dir.rmdir(); raise SystemExit("No figure captions were detected; manual extraction is required.")
    print(f"output={paper_dir}\ncomplete_figures={complete}\npanel_crops={panels}\nfallback_crops={fallbacks}"); return 0

if __name__ == "__main__": raise SystemExit(main())
