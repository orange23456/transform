from pathlib import Path
import zipfile, re
p = Path(r'C:\Users\hz-user\Desktop\加热搅拌系列产品.docx')
with zipfile.ZipFile(p) as z:
    names = z.namelist()
    media = [n for n in names if n.startswith('word/media/')]
    xml_text = ''
    for n in names:
        if n.startswith('word/') and n.endswith('.xml'):
            try:
                xml_text += z.read(n).decode('utf-8', errors='ignore') + '\n'
            except Exception:
                pass
    texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', xml_text)
    txbx = re.findall(r'<[^>]*t[^>]*>([^<>]{2,})</[^>]*t>', xml_text)
    print('zip_entries', len(names))
    print('media_count', len(media))
    print('media_first', media[:20])
    print('w_t_count', len(texts))
    print('w_t_preview')
    for t in texts[:80]: print(t[:200])
    print('xml_size', len(xml_text))
