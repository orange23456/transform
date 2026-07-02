from pathlib import Path
import json,re
jp=Path(r'C:\Users\hz-user\Desktop\全自动\product_collection_records.json')
xp=Path(r'C:\Users\hz-user\Desktop\全自动\outputs\product_collection\产品集_电子滴定分液_含配件_全英文HTML_参数完整版.xlsx')
recs=json.loads(jp.read_text(encoding='utf-8'))[0]['records']
cjk=sum(1 for r in recs if re.search(r'[\u4e00-\u9fff]',r.get('代码','')))
src=sum(1 for r in recs if r.get('来源'))
email=sum(1 for r in recs if 'EMAIL: inquiry@atomfair.com' not in r.get('代码',''))
acc=sum(1 for r in recs if 'Accessories' in r.get('网站分类',''))
specs=[r['型号'] for r in recs if r['型号'].endswith('10ML') or r['型号'].endswith('25ML') or r['型号'].endswith('50ML')]
print('product_collection rows',len(recs),'volume_spec_rows',len(specs),specs,'accessory_rows',acc,'html_cjk_issues',cjk,'source_nonblank',src,'email_missing',email,'xlsx_exists',xp.exists(),'size_kb',round(xp.stat().st_size/1024,1) if xp.exists() else 0)
