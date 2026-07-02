from pathlib import Path
import json
p=Path(r'C:\Users\hz-user\Desktop\全自动\product_collection_records.json')
payload=json.loads(p.read_text(encoding='utf-8'))
name_map={
'AF-LH-DTITRE-PRO-10ML':'电子滴定器 dTitre-Pro 10mL',
'AF-LH-DTITRE-PRO-25ML':'电子滴定器 dTitre-Pro 25mL',
'AF-LH-DTITRE-PRO-50ML':'电子滴定器 dTitre-Pro 50mL',
'AF-LH-DTITRE-S-10ML':'电子滴定器 dTitre-S 10mL',
'AF-LH-DTITRE-S-25ML':'电子滴定器 dTitre-S 25mL',
'AF-LH-DTITRE-S-50ML':'电子滴定器 dTitre-S 50mL',
'AF-LH-DFLOW-PRO-10ML':'电子瓶口分液器 dFlow-Pro 10mL',
'AF-LH-DFLOW-PRO-25ML':'电子瓶口分液器 dFlow-Pro 25mL',
'AF-LH-DFLOW-PRO-50ML':'电子瓶口分液器 dFlow-Pro 50mL',
'AF-LH-DTITRE-10ML':'电子滴定器 dTitre 10mL',
'AF-LH-PCOLL-ACC-001':'试剂瓶底托',
'AF-LH-PCOLL-ACC-002':'补液转接件',
'AF-LH-PCOLL-ACC-003':'漏斗转接件',
'AF-LH-PCOLL-ACC-004':'底座',
'AF-LH-PCOLL-ACC-005':'漏斗',
'AF-LH-PCOLL-ACC-006':'pH计',
'AF-LH-PCOLL-ACC-007':'蓝牙打印机（热敏）',
'AF-LH-PCOLL-ACC-008':'鹅色传感器',
'AF-LH-PCOLL-ACC-009':'上位机软件',
}
changed=0
for group in payload:
    for r in group['records']:
        model=r.get('型号')
        if model in name_map:
            r['商品中文名称']=name_map[model]
            changed+=1
p.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
print('changed',changed,'records',sum(len(g['records']) for g in payload))
