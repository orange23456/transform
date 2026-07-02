from pathlib import Path
import json,re,html
ROOT=Path(r'C:\Users\hz-user\Desktop\全自动')
OUT=ROOT/'generated_html_full'/'Atomfair_product_collection_HTML'
OUT.mkdir(parents=True,exist_ok=True)
HEADERS=["来源","商品中文名称","型号","产品名称（英文）","URL","简介","产品详情","代码","网站分类","主图","详情图","图片文件名","alt text","title","Caption","价格","💲","是否上传"]
def esc(x): return html.escape(str(x),quote=True)
def slug(s): return re.sub(r'[^A-Za-z0-9]+','_',s).strip('_')[:90] or 'item'
def dt(headers,rows):
    th=''.join(f'<th style="background:#111;color:#fff;border:1px solid #111;padding:11px 12px;text-align:left;">{esc(h)}</th>' for h in headers)
    trs=[]
    for r in rows:
        tds=[]
        for i,c in enumerate(r):
            wt='font-weight:700;' if i==0 else ''
            tds.append(f'<td style="border:1px solid #d7d7d7;padding:10px 12px;{wt}vertical-align:top;">{esc(c)}</td>')
        trs.append('<tr>'+''.join(tds)+'</tr>')
    return f'<table style="border-collapse:collapse;border:1px solid #111;font-size:14px;" border="0" width="100%" cellspacing="0" cellpadding="0"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table>'
def sec(t,b): return f'<table style="margin-bottom:34px;" border="0" width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td style="border-left:5px solid #111;padding-left:15px;padding-bottom:12px;"><h2 style="margin:0;font-size:18px;color:#111;text-transform:uppercase;font-weight:800;">{esc(t)}</h2></td></tr><tr><td style="padding-top:18px;">{b}</td></tr></tbody></table>'
def page(title,model,ptype,overview,features,specs,ordering,accessories=None):
    p=[f'<!-- Atomfair Complete Product HTML - Full-English Release --><div style="width:100%;background:#ffffff;padding:0;" align="center"><table style="width:100%;font-family:Arial,Helvetica,sans-serif;color:#333;line-height:1.58;background:#fff;" border="0" width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td style="padding:38px 20px;border-bottom:4px solid #111;"><h1 style="margin:0;font-size:26px;color:#111;font-weight:800;text-transform:uppercase;">{esc(title)}</h1><div style="margin-top:8px;font-size:14px;color:#333;">Product Type: {esc(ptype)}</div><div class="model" style="margin-top:10px;font-size:15px;color:#333;font-weight:700;">Atomfair Model: {esc(model)}</div><div style="margin-top:15px;display:inline-block;background:#111;color:#fff;padding:6px 15px;font-size:13px;font-weight:bold;letter-spacing:.6px;text-transform:uppercase;">Research-grade liquid handling platform</div></td></tr><tr><td style="padding:38px 20px;">']
    p.append(sec('Product Overview',''.join(f'<p style="margin:0 0 14px 0;font-size:15px;color:#444;text-align:justify;">{esc(x)}</p>' for x in overview)))
    p.append(sec('Key Features and Advantages','<ul style="margin:0;padding-left:22px;font-size:14px;color:#444;line-height:1.85;">'+''.join(f'<li style="margin-bottom:9px;">{esc(x)}</li>' for x in features)+'</ul>'))
    p.append(sec('Technical Specifications',dt(['Parameter','Specification / Available Values'],specs)))
    if accessories: p.append(sec('Included and Compatible Accessories',dt(['Accessory / Module','Reference Code','Specification','Compatibility / Use'],accessories)))
    p.append(sec('Atomfair Product Ordering and Configuration Table',dt(ordering[0],ordering[1])))
    p.append('<table style="background:#f7f7f7;border:1px solid #e0e0e0;margin-bottom:34px;" border="0" width="100%" cellspacing="0" cellpadding="22"><tbody><tr><td style="font-size:14px;color:#333;"><div style="margin-bottom:10px;"><strong>Data Handling Standard:</strong> HTML content is English only. Volume range, resolution, piston size, speed, temperature range, ISO standard, connectivity, battery, memory, screen and accuracy data are preserved in structured tables.</div><div><strong>Ordering Standard:</strong> Each titrator, dispenser, volume specification, accessory or software module receives a unique Atomfair order model.</div></td></tr></tbody></table></td></tr><tr><td style="padding:25px 20px;background:#111;text-align:center;"><div style="color:#fff;font-size:20px;font-weight:bold;margin-bottom:8px;letter-spacing:1px;">TAILORED SOLUTIONS FOR RESEARCH</div><div style="color:#ddd;font-size:13px;margin-bottom:18px;">For bulk orders, OEM requirements, accessory matching, platform selection or configuration confirmation, contact our engineering sales team.</div><div style="display:inline-block;background:#fff;color:#111;padding:12px 35px;font-weight:800;font-size:13px;text-transform:uppercase;letter-spacing:1px;border-radius:2px;">EMAIL: inquiry@atomfair.com</div></td></tr><tr><td style="padding:28px 20px;text-align:center;font-size:12px;color:#888;letter-spacing:1px;"><div style="margin-bottom:5px;text-transform:uppercase;"><strong>Supplier:</strong> Atomfair</div><div style="text-transform:uppercase;"><strong>Brand:</strong> ATOMFAIR&reg;</div></td></tr></tbody></table></div>')
    return ''.join(p)
def rec(cn,model,en,intro,code,cat):
    r={h:'' for h in HEADERS}; r.update({'来源':'','商品中文名称':cn,'型号':model,'产品名称（英文）':en,'简介':intro,'代码':code,'网站分类':cat}); return r
records=[]
common_features=['Electronic operation supports controlled titration, dispensing and liquid-transfer workflows.','Model-specific volume range and accuracy values are preserved as separate ordering rows.','Suitable for chemical analysis, food industry, water analysis and other laboratory titration or dispensing tasks.','Accessories and software modules are listed separately for complete configuration.']
precision={
'10 mL':[('10 mL','10 mL','Systematic error +/-20 uL +/-0.2%','CV +/-7 uL +/-0.07%'),('10 mL','5 mL','Systematic error +/-20 uL +/-0.4%','CV +/-7 uL +/-0.14%'),('10 mL','1 mL','Systematic error +/-20 uL +/-2.0%','CV +/-7 uL +/-0.7%')],
'25 mL':[('25 mL','25 mL','Systematic error +/-50 uL +/-0.2%','CV +/-17.5 uL +/-0.07%'),('25 mL','12.5 mL','Systematic error +/-50 uL +/-0.4%','CV +/-17.5 uL +/-0.14%'),('25 mL','2.5 mL','Systematic error +/-50 uL +/-2.0%','CV +/-17.5 uL +/-0.7%')],
'50 mL':[('50 mL','50 mL','Systematic error +/-100 uL +/-0.2%','CV +/-25 uL +/-0.05%'),('50 mL','25 mL','Systematic error +/-100 uL +/-0.4%','CV +/-25 uL +/-0.10%'),('50 mL','5 mL','Systematic error +/-100 uL +/-2.0%','CV +/-25 uL +/-0.5%')]
}
product_specs=[]
for family,base,source,pc in [('dTitre-Pro','AF-LH-DTITRE-PRO','dTitre-Pro electronic titrator','Type-C and WiFi'),('dTitre-S','AF-LH-DTITRE-S','dTitre-S electronic titrator','Not listed'),('dFlow-Pro','AF-LH-DFLOW-PRO','dFlow-Pro electronic bottle-top dispenser','Type-C and WiFi')]:
    for vol,work,minmove in [('10 mL','0.010 mL to 99.999 mL; single maximum transfer 10 mL; minimum 10 uL','0.1-2 mL/s'),('25 mL','0.020 mL to 99.999 mL; single maximum transfer 25 mL; minimum 20 uL','0.5-5 mL/s'),('50 mL','0.020 mL to 99.999 mL; single maximum transfer 50 mL; minimum 20 uL','0.1-10 mL/s')]:
        product_specs.append((family,base,source,pc,vol,work,minmove))
# dTitre from page 43
product_specs.append(('dTitre','AF-LH-DTITRE','dTitre electronic titrator','Cable connection and remote control support', '10 mL','0.01 mL to 99.99 mL; maximum piston volume 10 mL; minimum 10 uL','16 stages'))
for family,base,source,pc,vol,work,speed in product_specs:
    model=base+'-'+vol.split()[0].replace('.','')+'ML'
    en=f'ATOMFAIR® {family} {vol} Electronic Titration / Dispensing System'
    ptype='Electronic Titrator' if 'Titre' in family else 'Electronic Bottle-Top Dispenser'
    specs=[('Source product',source),('Volume specification',vol),('Working range',work),('Speed / dispensing range',speed),('Working temperature range','10-30 C' if family!='dTitre' else '15-40 C'),('Quality standard','ISO 8655'),('Bluetooth function','Available' if family in ('dTitre-Pro','dFlow-Pro') else 'Not listed'),('WiFi function','Available' if family in ('dTitre-Pro','dFlow-Pro') else 'Not listed'),('Control mode','Supports program control; dFlow-Pro supports automatic dispensing programs and manual/custom dispensing modes'),('Battery capacity','3500 mAh' if family in ('dTitre-Pro','dFlow-Pro') else 'Not listed'),('Memory','1000 experiment records' if family in ('dTitre-Pro','dFlow-Pro') else 'Not listed'),('Screen','4.3-inch TFT touch screen, 800 x 480 resolution' if family in ('dTitre-Pro','dFlow-Pro') else 'LCD large display'),('PC interface',pc),('Weight','1.2 kg' if family in ('dTitre-Pro','dFlow-Pro') else 'Not listed')]
    order=[]
    for rng,test,sys,cv in precision.get(vol,[]): order.append([model,rng,test,sys,cv])
    if family=='dTitre': order=[ [model,'10 mL','10 / 5 / 1 mL','Systematic error R=0.2% / 0.2% / 1.0%','CV=0.7% / 0.7% / 0.5%'] ]
    code=page(en,model,ptype,[f'{family} {vol} is an electronic liquid-handling system for accurate titration, dispensing, aspiration and repetitive liquid transfer.', 'The volume-specific model is separated as its own Atomfair ordering line so the 10 mL, 25 mL and 50 mL specifications remain clear.'],common_features,specs,(['Unique Atomfair Order Model','Nominal Volume','Test Volume','Systematic Error R','Coefficient of Variation CV'],order))
    (OUT/(slug(model)+'.html')).write_text(code,encoding='utf-8')
    records.append(rec('产品集 '+family+' '+vol,model,en,f'{family} {vol}: {work}.',code,'Liquid Handling'))
acc=[('Trial bottle holder','17001682','Holder for standard reagent bottles, preventing operator contact during reagent or titration-liquid handling'),('Titration tube clip','17001681','Fixes titration tube and supports connection to burette or external container'),('Waste bottle accessory','17001680','Allows reagent discharge without liquid remaining inside the titration head'),('Base','17001679','Holds titrator/dispenser securely on the operating bench'),('Funnel','17900433','Guides filling or liquid transfer'),('pH probe','17900519','Auxiliary titration endpoint judgment'),('Printer','17900518','Prints titration result data'),('Gooseneck tube','17900541','Auxiliary titration endpoint judgment'),('Host PC software','AF-PC-SOFTWARE','Computer connection software for titration or dispensing configuration and record handling')]
for i,(name,ref,spec) in enumerate(acc,1):
    model=f'AF-LH-PCOLL-ACC-{i:03d}'; en=f'ATOMFAIR® {name}'; intro=f'{name} is a configuration accessory for electronic titration or dispensing systems.'
    specs=[('Accessory name',name),('Reference code',ref),('Function',spec),('Compatibility','dTitre-Pro, dTitre-S, dTitre and dFlow-Pro configurations as applicable')]
    code=page(en,model,'Liquid Handling Accessory',[intro,'Accessories are listed separately so each holder, clip, probe, printer, software module or liquid-path accessory can be ordered and replaced independently.'],['Unique Atomfair accessory model.','Reference code and function are retained from the source page.','Supports complete configuration, titration endpoint handling, result printing or PC operation.'],specs,(['Unique Atomfair Order Model','Reference Code','Source Item / Component','Specification Value'],[[model,ref,name,spec]]))
    (OUT/(slug(model)+'_'+slug(name)+'.html')).write_text(code,encoding='utf-8')
    records.append(rec('产品集配件 '+name,model,en,intro,code,'Liquid Handling Accessories'))
path=ROOT/'product_collection_records.json'
path.write_text(json.dumps([{'sheetName':'Product Collection','folder':str(OUT),'records':records}],ensure_ascii=False,indent=2),encoding='utf-8')
bad=sum(1 for r in records if re.search(r'[\u4e00-\u9fff]',r['代码']))
print('Product Collection records',len(records),'html_cjk_issues',bad)
