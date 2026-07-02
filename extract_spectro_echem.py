from pathlib import Path
import zipfile, re, math
from PIL import Image, ImageDraw
from xml.etree import ElementTree as ET
root=Path(r'C:\Users\hz-user\Desktop\全自动')
docs=[('spectrophotometer',Path(r'C:\Users\hz-user\Desktop\分光光度计.docx'),root/'spectrophotometer_source_images'),('electrochemistry',Path(r'C:\Users\hz-user\Desktop\电化学系列产品.docx'),root/'electrochemistry_source_images')]
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def sort_key(n):
    m=re.search(r'image(\d+)',n); return int(m.group(1)) if m else 999999
for label,src,out in docs:
    out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(src) as z:
        names=z.namelist(); media=sorted([n for n in names if n.startswith('word/media/')],key=sort_key)
        txt=[]; tables=0
        if 'word/document.xml' in names:
            rootxml=ET.fromstring(z.read('word/document.xml'))
            tables=len(rootxml.findall('.//w:tbl',NS))
            for p in rootxml.findall('.//w:p',NS):
                s=''.join([t.text for t in p.findall('.//w:t',NS) if t.text])
                if s: txt.append(s)
        files=[]
        for n in media:
            dest=out/Path(n).name; dest.write_bytes(z.read(n)); files.append(dest)
    (out/'extracted_text.txt').write_text('\n'.join(txt),encoding='utf-8')
    thumbs=[]
    for f in files:
        try: im=Image.open(f).convert('RGB')
        except Exception: continue
        im.thumbnail((320,260)); canvas=Image.new('RGB',(350,320),'white')
        canvas.paste(im,((350-im.width)//2,10)); d=ImageDraw.Draw(canvas)
        d.text((10,282),f.name,fill='black'); d.text((10,300),f'{Image.open(f).size[0]}x{Image.open(f).size[1]}',fill='gray')
        thumbs.append(canvas)
    cols=3; rows=max(1,math.ceil(len(thumbs)/cols)); sheet=Image.new('RGB',(cols*350,rows*320),'white')
    for i,t in enumerate(thumbs): sheet.paste(t,((i%cols)*350,(i//cols)*320))
    sheet.save(out/'contact_sheet.jpg',quality=92)
    print(label, 'media', len(files), 'paragraphs', len(txt), 'tables', tables, 'contact', out/'contact_sheet.jpg')
