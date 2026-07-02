import zipfile, re
p = r'C:\Users\hz-user\Desktop\离心系列产品.docx'
with zipfile.ZipFile(p) as z:
    names = z.namelist()
    media = [n for n in names if n.startswith('word/media/')]
    xml = ''
    for n in names:
        if n.startswith('word/') and n.endswith('.xml'):
            xml += z.read(n).decode('utf-8', errors='ignore') + '\n'
    texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', xml)
    print('entries', len(names))
    print('media', len(media))
    print('texts', len(texts))
    print('preview')
    for t in texts[:40]: print(t[:200])
