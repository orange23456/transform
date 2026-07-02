from pathlib import Path
import zipfile, math
from PIL import Image, ImageOps, ImageDraw
src = Path(r'C:\Users\hz-user\Desktop\离心系列产品.docx')
out = Path(r'C:\Users\hz-user\Desktop\全自动\centrifuge_source_images')
out.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(src) as z:
    media = [n for n in z.namelist() if n.startswith('word/media/')]
    def sort_key(n):
        import re
        m = re.search(r'image(\d+)', n)
        return int(m.group(1)) if m else 9999
    media = sorted(media, key=sort_key)
    files=[]
    for n in media:
        dest = out / Path(n).name
        dest.write_bytes(z.read(n))
        files.append(dest)
thumbs=[]
for f in files:
    im = Image.open(f).convert('RGB')
    im.thumbnail((220, 220))
    canvas = Image.new('RGB', (240, 260), 'white')
    canvas.paste(im, ((240-im.width)//2, 10))
    d=ImageDraw.Draw(canvas)
    d.text((10, 235), f.name, fill='black')
    thumbs.append(canvas)
cols=4
rows=math.ceil(len(thumbs)/cols)
sheet=Image.new('RGB', (cols*240, rows*260), 'white')
for i,t in enumerate(thumbs): sheet.paste(t, ((i%cols)*240, (i//cols)*260))
sheet.save(out/'contact_sheet.jpg', quality=90)
print(out)
print(len(files))
