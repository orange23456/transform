from pathlib import Path
import zipfile
p = Path(r'C:\Users\hz-user\Desktop\加热搅拌系列产品.docx')
out = Path(r'C:\Users\hz-user\Desktop\全自动\source_doc_images')
out.mkdir(exist_ok=True)
with zipfile.ZipFile(p) as z:
    media = [n for n in z.namelist() if n.startswith('word/media/')]
    for n in media[:8]:
        (out / Path(n).name).write_bytes(z.read(n))
print(out)
print(len(media))
