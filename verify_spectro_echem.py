from pathlib import Path
import json,re
checks=[('spectrophotometer',Path(r'C:\Users\hz-user\Desktop\全自动\spectrophotometer_records.json'),Path(r'C:\Users\hz-user\Desktop\全自动\outputs\spectrophotometer_series\分光光度计_含配件_全英文HTML_参数完整版.xlsx')),('electrochemistry',Path(r'C:\Users\hz-user\Desktop\全自动\electrochemistry_records.json'),Path(r'C:\Users\hz-user\Desktop\全自动\outputs\electrochemistry_series\电化学系列产品_含电极配件_全英文HTML_参数完整版.xlsx'))]
for label,jp,xp in checks:
    payload=json.loads(jp.read_text(encoding='utf-8')); recs=payload[0]['records']
    cjk=sum(1 for r in recs if re.search(r'[\u4e00-\u9fff]',r.get('代码','')))
    src=sum(1 for r in recs if r.get('来源'))
    email=sum(1 for r in recs if 'EMAIL: inquiry@atomfair.com' not in r.get('代码',''))
    acc=sum(1 for r in recs if ('Accessories' in r.get('网站分类','') or 'Electrodes' in r.get('网站分类','')))
    main=[r for r in recs if r not in [] and 'Accessories' not in r.get('网站分类','') and 'Electrodes' not in r.get('网站分类','')]
    rows=[(r['型号'], r['代码'].count('<tr>')) for r in main[:6]]
    print(label,'rows',len(recs),'main_rows',len(main),'accessory_or_electrode_rows',acc,'html_cjk_issues',cjk,'source_nonblank',src,'email_missing',email,'xlsx_exists',xp.exists(),'size_kb',round(xp.stat().st_size/1024,1) if xp.exists() else 0,'sample_tr_counts',rows)
