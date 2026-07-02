from pathlib import Path
import json, re
checks = [
    ('mixer', Path(r'C:\Users\hz-user\Desktop\全自动\mixer_shaker_records.json'), Path(r'C:\Users\hz-user\Desktop\全自动\outputs\mixer_shaker_series\混匀摇床系列产品_含配件_全英文HTML_参数补全版.xlsx')),
    ('electrophoresis', Path(r'C:\Users\hz-user\Desktop\全自动\electrophoresis_records.json'), Path(r'C:\Users\hz-user\Desktop\全自动\outputs\electrophoresis_series\电泳仪系列产品_含配件_全英文HTML_参数补全版.xlsx')),
]
for label, jp, xp in checks:
    payload = json.loads(jp.read_text(encoding='utf-8'))
    recs = payload[0]['records']
    cjk = sum(1 for r in recs if re.search(r'[\u4e00-\u9fff]', r.get('代码', '')))
    source_nonblank = sum(1 for r in recs if r.get('来源'))
    accessories = sum(1 for r in recs if 'Accessories' in r.get('网站分类', ''))
    email_missing = sum(1 for r in recs if 'EMAIL: inquiry@atomfair.com' not in r.get('代码', ''))
    # Count table rows in representative main-product HTML to ensure expanded specs are present.
    main = [r for r in recs if 'Accessories' not in r.get('网站分类', '')]
    row_counts = [(r['型号'], r.get('代码','').count('<tr>')) for r in main[:8]]
    print(label, 'rows', len(recs), 'main_rows', len(main), 'accessory_rows', accessories, 'html_cjk_issues', cjk, 'source_nonblank', source_nonblank, 'email_missing', email_missing, 'xlsx_exists', xp.exists(), 'size_kb', round(xp.stat().st_size / 1024, 1) if xp.exists() else 0, 'sample_tr_counts', row_counts)
