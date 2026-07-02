from pathlib import Path
import zipfile, re, math
from PIL import Image, ImageDraw, ImageFont
from xml.etree import ElementTree as ET

docs = [
    (Path(r'C:\Users\hz-user\Desktop\混匀&摇床系列产品.docx'), Path(r'C:\Users\hz-user\Desktop\全自动\mixer_shaker_source_images')),
    (Path(r'C:\Users\hz-user\Desktop\电泳仪系列产品.docx'), Path(r'C:\Users\hz-user\Desktop\全自动\electrophoresis_source_images')),
]
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def sort_key(n):
    m=re.search(r'image(\d+)', n)
    return int(m.group(1)) if m else 999999

for src,out in docs:
    out.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(src) as z:
        names=z.namelist()
        media=sorted([n for n in names if n.startswith('word/media/')], key=sort_key)
        txt=[]
        if 'word/document.xml' in names:
            root=ET.fromstring(z.read('word/document.xml'))
            for p in root.findall('.//w:p', NS):
                parts=[t.text for t in p.findall('.//w:t', NS) if t.text]
                if parts:
                    txt.append(''.join(parts))
        tables=0
        if 'word/document.xml' in names:
            root=ET.fromstring(z.read('word/document.xml'))
            tables=len(root.findall('.//w:tbl', NS))
        files=[]
        for n in media:
            dest=out/Path(n).name
            dest.write_bytes(z.read(n))
            files.append(dest)
    (out/'extracted_text.txt').write_text('\n'.join(txt), encoding='utf-8')
    thumbs=[]
    for f in files:
        try:
            im=Image.open(f).convert('RGB')
        except Exception:
            continue
        im.thumbnail((300,260))
        canvas=Image.new('RGB',(330,315),'white')
        canvas.paste(im,((330-im.width)//2,10))
        d=ImageDraw.Draw(canvas)
        d.text((10,278),f.name,fill='black')
        try:
            d.text((10,294),f'{Image.open(f).size[0]}x{Image.open(f).size[1]}',fill='gray')
        except Exception:
            pass
        thumbs.append(canvas)
    cols=3
    rows=max(1, math.ceil(len(thumbs)/cols))
    sheet=Image.new('RGB',(cols*330,rows*315),'white')
    for i,t in enumerate(thumbs):
        sheet.paste(t,((i%cols)*330,(i//cols)*315))
    sheet_path=out/'contact_sheet.jpg'
    sheet.save(sheet_path, quality=92)
    print(f'{src.name}\tmedia={len(files)}\tparagraphs={len(txt)}\ttables={tables}\tcontact={sheet_path}')
