from pathlib import Path
import json,re
jp=Path(r'C:\Users\hz-user\Desktop\全自动\pipetting_records.json')
xp=Path(r'C:\Users\hz-user\Desktop\全自动\outputs\pipetting_series\移液系列产品_含配件_全英文HTML_参数完整版.xlsx')
payload=json.loads(jp.read_text(encoding='utf-8')); recs=payload[0]['records']
cjk=sum(1 for r in recs if re.search(r'[\u4e00-\u9fff]',r.get('代码','')))
src=sum(1 for r in recs if r.get('来源'))
email=sum(1 for r in recs if 'EMAIL: inquiry@atomfair.com' not in r.get('代码',''))
acc=sum(1 for r in recs if 'Accessories' in r.get('网站分类',''))
main=[r for r in recs if 'Accessories' not in r.get('网站分类','')]
rows=[(r['型号'],r['代码'].count('<tr>')) for r in main[:8]]
print('pipetting rows',len(recs),'main_rows',len(main),'accessory_rows',acc,'html_cjk_issues',cjk,'source_nonblank',src,'email_missing',email,'xlsx_exists',xp.exists(),'size_kb',round(xp.stat().st_size/1024,1) if xp.exists() else 0,'sample_tr_counts',rows)
