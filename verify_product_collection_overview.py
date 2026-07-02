from pathlib import Path
import json,re
jp=Path(r'C:\Users\hz-user\Desktop\全自动\product_collection_records.json')
xp=Path(r'C:\Users\hz-user\Desktop\全自动\outputs\product_collection\产品集_电子滴定分液_含配件_全英文HTML_ProductOverview扩写版.xlsx')
recs=json.loads(jp.read_text(encoding='utf-8'))[0]['records']
cjk=sum(1 for r in recs if re.search(r'[\u4e00-\u9fff]',r.get('代码','')))
src=sum(1 for r in recs if r.get('来源'))
email=sum(1 for r in recs if 'EMAIL: inquiry@atomfair.com' not in r.get('代码',''))
para_counts=[]
for r in recs[:5]:
    m=re.search(r'Product Overview</h2>.*?padding-top:18px;">(.*?)</td></tr></tbody></table>', r['代码'], flags=re.S)
    para_counts.append((r['型号'], m.group(1).count('<p ') if m else 0))
print('rows',len(recs),'overview_sample_paragraphs',para_counts,'source_nonblank',src,'html_cjk_issues',cjk,'email_missing',email,'xlsx_exists',xp.exists(),'size_kb',round(xp.stat().st_size/1024,1) if xp.exists() else 0)
