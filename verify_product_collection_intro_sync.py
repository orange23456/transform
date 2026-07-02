from pathlib import Path
import json,re
jp=Path(r'C:\Users\hz-user\Desktop\全自动\product_collection_records.json')
xp=Path(r'C:\Users\hz-user\Desktop\全自动\outputs\product_collection\产品集_电子滴定分液_含配件_全英文HTML_简介同步扩写版.xlsx')
recs=json.loads(jp.read_text(encoding='utf-8'))[0]['records']
print('rows',len(recs),'intro_lengths',[len(r['简介']) for r in recs[:5]],'first_intro',recs[0]['简介'][:160],'source_nonblank',sum(1 for r in recs if r.get('来源')),'html_cjk_issues',sum(1 for r in recs if re.search(r'[\u4e00-\u9fff]',r.get('代码',''))),'email_missing',sum(1 for r in recs if 'EMAIL: inquiry@atomfair.com' not in r.get('代码','')),'xlsx_exists',xp.exists(),'size_kb',round(xp.stat().st_size/1024,1) if xp.exists() else 0)
