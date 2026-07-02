import json, re
from pathlib import Path
records = json.loads(Path(r'C:\Users\hz-user\Desktop\全自动\heating_stirring_records.json').read_text(encoding='utf-8'))
issues=[]
for group in records:
    for rec in group['records']:
        html = rec.get('代码','')
        found = re.findall(r'[\u4e00-\u9fff]+', html)
        if found:
            issues.append((rec.get('商品中文名称'), found[:5]))
print('html_cjk_issues', len(issues))
for item in issues[:20]: print(item)
