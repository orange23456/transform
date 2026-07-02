from pathlib import Path
import json, re
checks = [
    ('mixer', Path(r'C:\Users\hz-user\Desktop\全自动\mixer_shaker_records.json'), Path(r'C:\Users\hz-user\Desktop\全自动\outputs\mixer_shaker_series\混匀摇床系列产品_含配件_全英文HTML.xlsx')),
    ('electrophoresis', Path(r'C:\Users\hz-user\Desktop\全自动\electrophoresis_records.json'), Path(r'C:\Users\hz-user\Desktop\全自动\outputs\electrophoresis_series\电泳仪系列产品_含配件_全英文HTML.xlsx')),
]
for label, jp, xp in checks:
    payload = json.loads(jp.read_text(encoding='utf-8'))
    recs = payload[0]['records']
    cjk = sum(1 for r in recs if re.search(r'[\u4e00-\u9fff]', r.get('代码', '')))
    source_nonblank = sum(1 for r in recs if r.get('来源'))
    accessories = sum(1 for r in recs if 'Accessories' in r.get('网站分类', ''))
    email_missing = sum(1 for r in recs if 'EMAIL: inquiry@atomfair.com' not in r.get('代码', ''))
    footer_missing = sum(1 for r in recs if 'Supplier:</strong> Atomfair' not in r.get('代码', '') or 'Brand:</strong> ATOMFAIR' not in r.get('代码', ''))
    doctype_count = sum(1 for r in recs if '<!doctype html>' in r.get('代码', '').lower())
    print(label, 'rows', len(recs), 'accessory_rows', accessories, 'html_cjk_issues', cjk, 'source_nonblank', source_nonblank, 'email_missing', email_missing, 'footer_missing', footer_missing, 'doctype_count', doctype_count, 'xlsx_exists', xp.exists(), 'size_kb', round(xp.stat().st_size / 1024, 1) if xp.exists() else 0)
