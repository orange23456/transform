from pathlib import Path
import json,re
jp=Path(r'C:\Users\hz-user\Desktop\全自动\product_collection_records.json')
xp=Path(r'C:\Users\hz-user\Desktop\全自动\outputs\product_collection\产品集_电子滴定分液_含配件_全英文HTML_中文名称修正版.xlsx')
recs=json.loads(jp.read_text(encoding='utf-8'))[0]['records']
print('rows',len(recs),'first_names',[r['商品中文名称'] for r in recs[:5]],'source_nonblank',sum(1 for r in recs if r.get('来源')),'html_cjk_issues',sum(1 for r in recs if re.search(r'[\u4e00-\u9fff]',r.get('代码',''))),'email_missing',sum(1 for r in recs if 'EMAIL: inquiry@atomfair.com' not in r.get('代码','')),'xlsx_exists',xp.exists(),'size_kb',round(xp.stat().st_size/1024,1) if xp.exists() else 0)
