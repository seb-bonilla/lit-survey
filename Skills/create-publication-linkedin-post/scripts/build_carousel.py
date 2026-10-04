"""Assemble inspected paper crops into uniform images and a figure-only PDF."""
import argparse
from pathlib import Path
import pymupdf as fitz
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def build(pdf, rect, figures, output, size):
    figures = [Path(p).resolve(strict=True) for p in figures]
    output = Path(output).resolve()
    names = ['00-cover.jpg'] + [f'{i:02d}-figure-{i:02d}.jpg' for i in range(1, len(figures)+1)]
    targets = [output/'images'/n for n in names] + [output/'carousel.pdf']
    if any(p.exists() for p in targets):
        raise FileExistsError('Output already exists; choose a new version directory.')
    with fitz.open(pdf) as doc:
        clip = fitz.Rect(rect)
        if clip.is_empty or not doc[0].rect.contains(clip):
            raise ValueError('Header crop must lie within the first page.')
        pix = doc[0].get_pixmap(matrix=fitz.Matrix(300/72,300/72), clip=clip, alpha=False)
        cover = Image.frombytes('RGB', (pix.width,pix.height), pix.samples)
    output.joinpath('images').mkdir(parents=True,exist_ok=True)
    width,height = size
    if min(size) < 600:
        raise ValueError('Page size must preserve figure readability.')
    for i,target in enumerate(targets[:-1]):
        if i == 0:
            image = cover
        else:
            with Image.open(figures[i-1]) as src:
                image = src.convert('RGB')
        image = ImageOps.contain(image,(width-100,height-100), Image.Resampling.LANCZOS)
        page = Image.new('RGB',size,'white')
        page.paste(image,((width-image.width)//2,(height-image.height)//2))
        page.save(target,quality=97,subsampling=0)
    c = canvas.Canvas(str(targets[-1]),pagesize=(width/2,height/2))
    c.setTitle('Paper title and complete figures')
    for path in targets[:-1]:
        c.drawImage(ImageReader(str(path)),0,0,width=width/2,height=height/2)
        c.showPage()
    c.save()
    with fitz.open(targets[-1]) as check:
        assert len(check) == len(figures)+1
    print(f'Created {len(figures)+1} image pages and {targets[-1]}')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pdf',required=True,type=Path)
    p.add_argument('--header-rect',required=True,nargs=4,type=float)
    p.add_argument('--figures',required=True,nargs='+',type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--size',nargs=2,type=int,default=[1600,1200])
    a=p.parse_args()
    build(a.pdf,a.header_rect,a.figures,a.output,tuple(a.size))
