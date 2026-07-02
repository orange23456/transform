from pathlib import Path
import json,re
jp=Path(r'C:\Users\hz-user\Desktop\全自动\pipetting_records.json')
xp=Path(r'C:\Users\hz-user\Desktop\全自动\outputs\pipetting_series\移液系列产品_含配件_全英文HTML_多道规格补全版.xlsx')
recs=json.loads(jp.read_text(encoding='utf-8'))[0]['records']
cjk=sum(1 for r in recs if re.search(r'[\u4e00-\u9fff]',r.get('代码','')))
src=sum(1 for r in recs if r.get('来源'))
email=sum(1 for r in recs if 'EMAIL: inquiry@atomfair.com' not in r.get('代码',''))
ch8=[r['型号'] for r in recs if '8CH' in r['型号']]
ch12=[r['型号'] for r in recs if '12CH' in r['型号']]
ch16=[r['型号'] for r in recs if '16CH' in r['型号']]
acc=sum(1 for r in recs if 'Accessories' in r.get('网站分类',''))
print('pipetting rows',len(recs),'accessory_rows',acc,'8ch',len(ch8),ch8,'12ch',len(ch12),ch12,'16ch',len(ch16),ch16,'html_cjk_issues',cjk,'source_nonblank',src,'email_missing',email,'xlsx_exists',xp.exists(),'size_kb',round(xp.stat().st_size/1024,1) if xp.exists() else 0)
