from pathlib import Path
import json, re, html

ROOT = Path(r'C:\Users\hz-user\Desktop\全自动')
GEN = ROOT / 'generated_html_full'
MIX_DIR = GEN / 'Atomfair_mixer_shaker_HTML'
EP_DIR = GEN / 'Atomfair_electrophoresis_HTML'
OUT_MIX = ROOT / 'mixer_shaker_records.json'
OUT_EP = ROOT / 'electrophoresis_records.json'
for d in [MIX_DIR, EP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

HEADERS = ["来源", "商品中文名称", "型号", "产品名称（英文）", "URL", "简介", "产品详情", "代码", "网站分类", "主图", "详情图", "图片文件名", "alt text", "title", "Caption", "价格", "💲", "是否上传"]

def esc(x):
    return html.escape(str(x), quote=True)

def slug(s):
    return re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_')[:80] or 'item'

def detail_table(headers, rows):
    th = ''.join(
        f'<th style="background:#111;color:#fff;border:1px solid #111;padding:11px 12px;text-align:left;">{esc(h)}</th>'
        for h in headers
    )
    trs = []
    for row in rows:
        cells = []
        for idx, c in enumerate(row):
            weight = 'font-weight:700;' if idx == 0 else ''
            cells.append(f'<td style="border:1px solid #d7d7d7;padding:10px 12px;{weight}vertical-align:top;">{esc(c)}</td>')
        trs.append('<tr>' + ''.join(cells) + '</tr>')
    return f'<table style="border-collapse:collapse;border:1px solid #111;font-size:14px;" border="0" width="100%" cellspacing="0" cellpadding="0"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table>'

def section(title, body_html):
    return (
        '<table style="margin-bottom:34px;" border="0" width="100%" cellspacing="0" cellpadding="0"><tbody>'
        '<tr><td style="border-left:5px solid #111;padding-left:15px;padding-bottom:12px;">'
        f'<h2 style="margin:0;font-size:18px;color:#111;text-transform:uppercase;font-weight:800;">{esc(title)}</h2>'
        '</td></tr><tr><td style="padding-top:18px;">'
        f'{body_html}'
        '</td></tr></tbody></table>'
    )

def page(title, model, subtitle, overview, features, specs, ordering, accessories=None):
    product_type = 'Accessory' if 'Accessory' in subtitle else subtitle.replace(' Series', '')
    parts = [f'''<!-- Atomfair Complete Product HTML - Full-English Release -->
<div style="width:100%;background:#ffffff;padding:0;" align="center"><table style="width:100%;font-family:Arial,Helvetica,sans-serif;color:#333;line-height:1.58;background:#fff;" border="0" width="100%" cellspacing="0" cellpadding="0"><tbody>
<tr><td style="padding:38px 20px;border-bottom:4px solid #111;"><h1 style="margin:0;font-size:26px;color:#111;font-weight:800;text-transform:uppercase;">{esc(title)}</h1><div style="margin-top:8px;font-size:14px;color:#333;">Product Type: {esc(product_type)}</div><div class="model" style="margin-top:10px;font-size:15px;color:#333;font-weight:700;">Atomfair Model: {esc(model)}</div><div style="margin-top:15px;display:inline-block;background:#111;color:#fff;padding:6px 15px;font-size:13px;font-weight:bold;letter-spacing:.6px;text-transform:uppercase;">Research-grade laboratory platform</div></td></tr>
<tr><td style="padding:38px 20px;">''']
    overview_html = ''.join(f'<p style="margin:0 0 14px 0;font-size:15px;color:#444;text-align:justify;">{esc(p)}</p>' for p in overview)
    parts.append(section('Product Overview', overview_html))
    features_html = '<ul style="margin:0;padding-left:22px;font-size:14px;color:#444;line-height:1.85;">' + ''.join(f'<li style="margin-bottom:9px;">{esc(f)}</li>' for f in features) + '</ul>'
    parts.append(section('Key Features and Advantages', features_html))
    parts.append(section('Technical Specifications', detail_table(['Parameter', 'Specification / Available Values'], [[k, v] for k, v in specs])))
    if accessories:
        parts.append(section('Included and Compatible Accessories', detail_table(['Accessory / Module', 'Reference Code', 'Specification', 'Compatibility / Use'], accessories)))
    order_headers = list(ordering[0])
    if order_headers and order_headers[0] == 'Order Model':
        order_headers[0] = 'Unique Atomfair Order Model'
    if len(order_headers) > 1 and order_headers[1] in ('Product', 'Accessory'):
        order_headers[1] = 'Source Item / Component'
    if len(order_headers) > 2 and order_headers[2] in ('Configuration Notes', 'Compatibility', 'Core Configuration'):
        order_headers[2] = 'Specification Value'
    parts.append(section('Atomfair Product Ordering and Configuration Table', detail_table(order_headers, ordering[1])))
    parts.append('<table style="background:#f7f7f7;border:1px solid #e0e0e0;margin-bottom:34px;" border="0" width="100%" cellspacing="0" cellpadding="22"><tbody><tr><td style="font-size:14px;color:#333;"><div style="margin-bottom:10px;"><strong>Data Handling Standard:</strong> HTML content is English only. Technical parameters, dimensions, speed ranges, capacities, accessory compatibility, power and model-specific values are preserved in structured tables.</div><div><strong>Ordering Standard:</strong> Each instrument, platform, fixture, adapter, tray, comb, clamp or accessory receives a unique Atomfair order model.</div></td></tr></tbody></table></td></tr>')
    parts.append('<tr><td style="padding:25px 20px;background:#111;text-align:center;"><div style="color:#fff;font-size:20px;font-weight:bold;margin-bottom:8px;letter-spacing:1px;">TAILORED SOLUTIONS FOR RESEARCH</div><div style="color:#ddd;font-size:13px;margin-bottom:18px;">For bulk orders, OEM requirements, accessory matching, platform selection or configuration confirmation, contact our engineering sales team.</div><div style="display:inline-block;background:#fff;color:#111;padding:12px 35px;font-weight:800;font-size:13px;text-transform:uppercase;letter-spacing:1px;border-radius:2px;">EMAIL: inquiry@atomfair.com</div></td></tr>')
    parts.append('<tr><td style="padding:28px 20px;text-align:center;font-size:12px;color:#888;letter-spacing:1px;"><div style="margin-bottom:5px;text-transform:uppercase;"><strong>Supplier:</strong> Atomfair</div><div style="text-transform:uppercase;"><strong>Brand:</strong> ATOMFAIR&reg;</div></td></tr></tbody></table></div>')
    return ''.join(parts)

def record(cn, model, en, intro, code, category):
    r = {h: '' for h in HEADERS}
    r.update({"来源": "", "商品中文名称": cn, "型号": model, "产品名称（英文）": en, "简介": intro, "代码": code, "网站分类": category})
    return r

features_default = [
    'Robust laboratory construction for repeatable daily operation.',
    'Clear operating modes support quick setup and consistent sample handling.',
    'Accessory-based configuration allows tubes, plates, flasks, racks, or trays to be matched to the application.',
    'Suitable for molecular biology, microbiology, clinical sample preparation, staining, extraction, and general laboratory mixing workflows.'
]

mixer_products = [
('漩涡混匀仪 MX-S+', 'AF-MX-SPLUS', 'ATOMFAIR® MX-S+ Vortex Mixer', '100-3000 rpm; circular orbit; touch or continuous mode; accepts tube adapters and plate accessories.', [('Speed range','100-3000 rpm'),('Motion','Circular'),('Operating mode','Touch mode and continuous mode'),('Capacity','Adapter dependent'),('Recommended accessory family','VT1 and VT2 adapter systems')]),
('光感应款漩涡混匀仪 MX-Pro', 'AF-MX-PRO', 'ATOMFAIR® MX-Pro Light-Sensing Vortex Mixer', '100-3000 rpm; circular orbit; light-sensing/touch and continuous modes for efficient tube and plate mixing.', [('Speed range','100-3000 rpm'),('Motion','Circular'),('Operating mode','Light-sensing touch mode and continuous mode'),('Capacity','Adapter dependent'),('Recommended accessory family','VT2 adapter systems')]),
('漩涡仪 MX-S', 'AF-MX-S', 'ATOMFAIR® MX-S Adjustable Vortex Mixer', '0-3000 rpm vortex mixer for tubes, vessels, and small accessories.', [('Speed range','0-3000 rpm'),('Motion','Circular'),('Operating mode','Touch mode and continuous mode'),('Capacity','Adapter dependent'),('Recommended accessory family','VT1 adapter systems')]),
('漩涡仪 MX-F', 'AF-MX-F', 'ATOMFAIR® MX-F Fixed-Speed Vortex Mixer', 'Fixed 3000 rpm vortex mixer for fast tube resuspension and small sample mixing.', [('Speed','3000 rpm fixed'),('Motion','Circular'),('Operating mode','Touch mode and continuous mode'),('Capacity','Adapter dependent')]),
('经济款固定转速漩涡仪 MX-E', 'AF-MX-E', 'ATOMFAIR® MX-E Economy Fixed-Speed Vortex Mixer', 'Compact fixed-speed mixer with 3000 rpm circular vortex action and touch operation.', [('Speed','3000 rpm fixed'),('Motion','Circular'),('Operating mode','Touch mode'),('Capacity','Single-tube cup style operation')]),
('细胞破碎仪 MX-C', 'AF-MX-C', 'ATOMFAIR® MX-C Cell Disruptor', '0-3000 rpm cell disruption mixer supplied for 8 x 2 mL sample processing.', [('Speed range','0-3000 rpm'),('Motion','Circular'),('Operating mode','Touch mode and continuous mode'),('Capacity','8 x 2 mL')]),
('96孔板混匀仪 MX-M', 'AF-MX-M', 'ATOMFAIR® MX-M Microplate Mixer', '0-1500 rpm circular microplate mixer with 0.5 kg shaking load.', [('Speed range','0-1500 rpm'),('Motion','Circular'),('Operating mode','Continuous mode'),('Capacity','0.5 kg')]),
('圆盘旋转混匀仪 MX-RD-Pro', 'AF-MX-RD-PRO', 'ATOMFAIR® MX-RD-Pro LCD Tube Rotator', '10-70 rpm 360-degree rotating mixer for tube disks and centrifuge tubes up to 50 mL.', [('Speed range','10-70 rpm'),('Motion','360-degree rotation'),('Operating mode','Timer mode and continuous mode'),('Capacity','60 x 1.5 mL, 16 x 15 mL, or 8 x 50 mL depending on disk')]),
('长轴旋转混匀仪 MX-RL-Pro', 'AF-MX-RL-PRO', 'ATOMFAIR® MX-RL-Pro LCD Long-Axis Tube Rotator', '10-70 rpm 360-degree rotating mixer for long-axis tube clamps and multiple tube formats.', [('Speed range','10-70 rpm'),('Motion','360-degree rotation'),('Operating mode','Timer mode and continuous mode'),('Capacity','48 x 1.5 mL, 24 x 15 mL, or 24 x 50 mL depending on clamp set')]),
('圆盘旋转混匀仪 MX-RD-E', 'AF-MX-RD-E', 'ATOMFAIR® MX-RD-E Economy Tube Rotator', '0-80 rpm continuous 360-degree rotation for tube disks and gentle sample mixing.', [('Speed range','0-80 rpm'),('Motion','360-degree rotation'),('Operating mode','Continuous mode'),('Capacity','48 x 2 mL, 16 x 15 mL, or 8 x 50 mL depending on disk')]),
('长轴旋转混匀仪 MX-RL-E', 'AF-MX-RL-E', 'ATOMFAIR® MX-RL-E Economy Long-Axis Tube Rotator', '0-80 rpm continuous 360-degree rotation for 32 x 2 mL, 20 x 15 mL, or 16 x 50 mL tubes.', [('Speed range','0-80 rpm'),('Motion','360-degree rotation'),('Operating mode','Continuous mode'),('Capacity','32 x 2 mL, 20 x 15 mL, or 16 x 50 mL')]),
('翘板混匀仪 SK-R30S-E', 'AF-SK-R30S-E', 'ATOMFAIR® SK-R30S-E Rocking Shaker', '0-30 rpm rocking shaker with 30 +/- 3 degree tilt for 10 x 10 mL or 4 x 50 mL tubes.', [('Speed range','0-30 rpm'),('Motion','Rocking, 30 +/- 3 degrees'),('Capacity','10 x 10 mL or 4 x 50 mL')]),
('翘板混匀仪 SK-R30L-E', 'AF-SK-R30L-E', 'ATOMFAIR® SK-R30L-E Large Rocking Shaker', '0-30 rpm rocking shaker with 30 +/- 3 degree tilt for 16 x 10 mL or 6 x 50 mL tubes.', [('Speed range','0-30 rpm'),('Motion','Rocking, 30 +/- 3 degrees'),('Capacity','16 x 10 mL or 6 x 50 mL')]),
('翘板混匀仪 SK-R30D-E', 'AF-SK-R30D-E', 'ATOMFAIR® SK-R30D-E Double-Deck Rocking Shaker', '0-30 rpm double-deck rocking shaker with 40 +/- 3 degree tilt for 32 x 10 mL or 12 x 50 mL tubes.', [('Speed range','0-30 rpm'),('Motion','Rocking, 40 +/- 3 degrees'),('Capacity','32 x 10 mL or 12 x 50 mL')]),
('滚轴混匀仪 MX-T6-Pro', 'AF-MX-T6-PRO', 'ATOMFAIR® MX-T6-Pro LCD Tube Roller Mixer', '0-70 rpm six-roller mixer with 360-degree rolling and rocking action and 4 kg load.', [('Speed range','0-70 rpm'),('Motion','360-degree rolling and rocking'),('Operating mode','Timer mode and continuous mode'),('Capacity','4 kg')]),
('滚轴混匀仪 MX-T6-S+', 'AF-MX-T6-SPLUS', 'ATOMFAIR® MX-T6-S+ Tube Roller Mixer', '0-70 rpm six-roller mixer with continuous 360-degree rolling and rocking action and 4 kg load.', [('Speed range','0-70 rpm'),('Motion','360-degree rolling and rocking'),('Operating mode','Continuous mode'),('Capacity','4 kg')]),
('圆周摇床 SK-O330-Pro', 'AF-SK-O330-PRO', 'ATOMFAIR® SK-O330-Pro Orbital Shaker', 'LCD orbital shaker with 32 x 32 cm platform and 100-500 rpm speed range.', [('Platform size','32 x 32 cm'),('Display','LCD'),('Speed range','100-500 rpm'),('Load','7.5 kg')]),
('圆周摇床 SK-O180-Pro', 'AF-SK-O180-PRO', 'ATOMFAIR® SK-O180-Pro Orbital Shaker', 'LCD orbital shaker with 25 x 24.5 cm platform and 100-800 rpm speed range.', [('Platform size','25 x 24.5 cm'),('Display','LCD'),('Speed range','100-800 rpm'),('Load','2.5 kg')]),
('圆周摇床 SK-O330-M', 'AF-SK-O330-M', 'ATOMFAIR® SK-O330-M Orbital Shaker', 'LCD orbital shaker with 33.5 x 33.5 cm platform and 70-400 rpm speed range.', [('Platform size','33.5 x 33.5 cm'),('Display','LCD'),('Speed range','70-400 rpm'),('Load','3 kg')]),
('圆周摇床 SK-O180-C', 'AF-SK-O180-C', 'ATOMFAIR® SK-O180-C Compact Orbital Shaker', 'LED compact orbital shaker with 26.8 x 26.8 cm platform and 40-200 rpm speed range.', [('Platform size','26.8 x 26.8 cm'),('Display','LED'),('Speed range','40-200 rpm'),('Load','2 kg')]),
('圆周摇床 SK-O180-S', 'AF-SK-O180-S', 'ATOMFAIR® SK-O180-S Compact Orbital Shaker', 'LED orbital shaker with 26.8 x 26.8 cm platform and 40-200 rpm speed range.', [('Platform size','26.8 x 26.8 cm'),('Display','LED'),('Speed range','40-200 rpm'),('Load','2 kg')]),
('线性摇床 SK-L330-Pro', 'AF-SK-L330-PRO', 'ATOMFAIR® SK-L330-Pro Linear Shaker', 'LCD linear shaker with 32 x 32 cm platform and 100-350 rpm speed range.', [('Platform size','32 x 32 cm'),('Display','LCD'),('Speed range','100-350 rpm'),('Load','7.5 kg')]),
('线性摇床 SK-L180-Pro', 'AF-SK-L180-PRO', 'ATOMFAIR® SK-L180-Pro Linear Shaker', 'LCD linear shaker with 25 x 24.5 cm platform and 100-350 rpm speed range.', [('Platform size','25 x 24.5 cm'),('Display','LCD'),('Speed range','100-350 rpm'),('Load','2.5 kg')]),
('翘板摇床 SK-L180-S', 'AF-SK-L180-S', 'ATOMFAIR® SK-L180-S Rocking Shaker', 'LED compact rocking shaker with 26.8 x 26.8 cm platform and 40-200 rpm speed range.', [('Platform size','26.8 x 26.8 cm'),('Display','LED'),('Speed range','40-200 rpm'),('Load','2 kg')]),
('翘板摇床 SK-R330-Pro', 'AF-SK-R330-PRO', 'ATOMFAIR® SK-R330-Pro See-Saw Rocker', 'LCD rocking shaker with 30 x 28.5 cm platform and 10-70 rpm speed range.', [('Platform size','30 x 28.5 cm'),('Display','LCD'),('Speed range','10-70 rpm'),('Load','10 kg')]),
('翘板摇床 SK-R1807-S', 'AF-SK-R1807-S', 'ATOMFAIR® SK-R1807-S See-Saw Rocker', 'LED rocking shaker with 26.8 x 26.8 cm platform and 10-80 rpm speed range.', [('Platform size','26.8 x 26.8 cm'),('Display','LED'),('Speed range','10-80 rpm'),('Load','2 kg')]),
('3D摇床 SK-D3309-Pro', 'AF-SK-D3309-PRO', 'ATOMFAIR® SK-D3309-Pro 3D Shaker', 'LCD 3D shaker with 30 x 28.5 cm platform and 10-70 rpm speed range.', [('Platform size','30 x 28.5 cm'),('Display','LCD'),('Speed range','10-70 rpm'),('Load','5 kg')]),
('3D摇床 SK-D1810-S', 'AF-SK-D1810-S', 'ATOMFAIR® SK-D1810-S 3D Shaker', 'LED 3D shaker with 26.8 x 26.8 cm platform and 10-80 rpm speed range.', [('Platform size','26.8 x 26.8 cm'),('Display','LED'),('Speed range','10-80 rpm'),('Load','2 kg')]),
]

mixer_accessories = [
('VT1.3.1 tube adapter','18900020','48 x 4 mm holes for 0.1-0.5 mL tubes','MX-S and VT1 universal tray system'),
('VT1.3.2 tube adapter','18900021','15 x 8 mm holes for 1.5-2 mL tubes','MX-S and VT1 universal tray system'),
('VT1.3.3 tube adapter','18900022','16 x 9 mm holes for 2-5 mL tubes','MX-S and VT1 universal tray system'),
('VT1.3.4 tube adapter','18900023','8 x 14 mm holes for 10-15 mL tubes or 5 mL tapered tubes','MX-S and VT1 universal tray system'),
('VT1.3.5 tube adapter','18900024','8 x 17 mm holes for 20 mL tubes','MX-S and VT1 universal tray system'),
('VT1.3.6 platform pad','18900043','99 mm pad for triple-use tubes','MX-S vortex platform'),
('VT1.3.7 vacuum suction cup foot','18900158','General suction mounting foot','MX-S accessory installation'),
('VT1.3.8 tube adapter','18900395','24 holes, 8 mm for 1.5-2 mL tubes','MX-S and VT1 universal tray system'),
('VT1.3.9 PCR eight-strip adapter','18204185','56 x 5.5 mm openings for 0.1-0.5 mL PCR strip tubes','MX-S and VT1 universal tray system'),
('VT1.3.10 tube adapter','18900855','4 holes, 27 mm for 50 mL tubes','MX-S and VT1 universal tray system'),
('VT1.3.11 multi-tube adapter','18900862','12 x 9.8 mm plus 12 x 6.6 mm holes for 1.5, 2.0, 0.5, and 0.2 mL tubes','MX-S and VT1 universal tray system'),
('VT1.2 adapter removal wrench','18900044','Tool for removing and replacing adapters','MX-S adapter service'),
('VT1.3 universal tray','18900505','100 mm tray for tubes and suction pad','MX-S adapter base'),
('PS1.0 microplate tray','18204342','Tray for microplates, deep-well plates, and PCR plates','MX-S vortex microplate work'),
('VT1.3.12 large combined adapter','18900875','44 x 5 mm plus 55 x 6.6 mm plus 30 x 9.8 mm openings','MX-S high-density small tube work'),
('VT1.4 tube rack clamp accessory','18204566','Four-tube metal clamp for 0.2-1.5 mL tubes','MX-S tube rack clamping'),
('VT1.5 conical flask accessory kit','18204561','Adapter kit for 100 mL to 250 mL conical flasks; recommended below 1500 rpm','MX-S flask mixing'),
('VT2.3 universal tray','18901365','Universal tray compatible with VT1.3.1 to VT1.3.12 adapters','MX-S+, MX-Pro'),
('VT2.4 tube rack clamp accessory','18901366','Clamp for 0.2-1.5 mL tubes; mainly for latex tube racks','MX-S+, MX-Pro'),
('VT2.5 conical flask accessory','18901367','Adapter for 100 mL to 250 mL conical flasks; recommended below 1500 rpm','MX-S+, MX-Pro'),
('PS2.1 microplate tray','18901360','Tray for full-skirt, half-skirt, and non-skirt PCR plates and deep-well plates','MX-S+, MX-Pro microplate work'),
('VT2.1 MX-Pro head','18901379','Replacement head for MX-Pro','MX-Pro'),
('VT2.1 MX-S+ head','18901380','Replacement head for MX-S+','MX-S+'),
('VT2.2 standard platform pad','18901373','Flat rubber pad','MX-S+, MX-Pro'),
('VT2.6 snap-in universal tray','18901368','Universal tray for VT2.6.1 to VT2.6.5 adapters','MX-S+, MX-Pro RUN mode'),
('VT2.6.1 tube adapter','18901378','25 x 4.5 mm holes for 0.1-0.5 mL tubes','MX-S+, MX-Pro RUN mode'),
('VT2.6.2 tube adapter','18901377','21 x 8 mm holes for 1.5-2 mL tubes','MX-S+, MX-Pro RUN mode'),
('VT2.6.3 tube adapter','18901376','16 x 10 mm holes for 2-5 mL tubes','MX-S+, MX-Pro RUN mode'),
('VT2.6.4 tube adapter','18901375','8 x 14 mm holes for 10-15 mL tubes or 5 mL tapered tubes','MX-S+, MX-Pro RUN mode'),
('VT2.6.5 tube adapter','18901374','4 x 25.5 mm holes for 50 mL tubes','MX-S+, MX-Pro RUN mode'),
('VT2.7.4 horizontal clamp','18901870','24 positions for 1.5 mL tubes, circular plate','MX-S+, MX-Pro'),
('VT2.7.5 horizontal clamp','18901871','12 positions for 15 mL tubes, circular plate','MX-S+, MX-Pro'),
('VT2.7.6 horizontal clamp','18901872','6 positions for 50 mL tubes, circular plate','MX-S+, MX-Pro'),
('PS2.2 microplate tray','18901361','Tray for PCR plates, deep-well plates, and microplates','MX-S+, MX-Pro'),
('Disk accessory type 1','18900160','Disk centrifuge-tube clamp, supports 1.5 mL x 60 tubes','MX-RD-Pro'),
('Disk accessory type 2','18900161','Disk centrifuge-tube clamp, supports 15 mL x 16 tubes','MX-RD-Pro'),
('Disk accessory type 3','18900162','Disk centrifuge-tube clamp, supports 50 mL x 8 tubes','MX-RD-Pro'),
('Disk connection tube','18900140','Round-disk centrifuge tube clamp accessory; set of four','MX-RD-Pro disk installation'),
('Long-axis tube clamp type 1','18900142','Clamp for 1.5 mL x 48 tubes; horizontally mounted','MX-RL-Pro'),
('Long-axis tube clamp type 2','18900143','Clamp for 15 mL x 24 tubes; horizontally mounted','MX-RL-Pro'),
('Long-axis tube clamp type 3','18900144','Clamp for 50 mL x 24 tubes; horizontally mounted','MX-RL-Pro'),
('Long-axis tube clamp type 4','18900145','Clamp for 1.5 mL x 32 tubes; vertically mounted','MX-RL-Pro'),
('Long-axis tube clamp type 5','18900146','Clamp for 15 mL x 16 tubes; vertically mounted','MX-RL-Pro'),
('Long-axis tube clamp type 6','18900147','Clamp for 50 mL x 16 tubes; vertically mounted','MX-RL-Pro'),
('SK330.5 non-slip platform','18900155','Anti-slip platform, external size 30 x 28.5 cm','SK-O330, SK-L330, SK-R330, SK-D3309 series'),
('Silicone tube mat 15 mL','18202835','Tube mat, supports 7 x 15 mL tubes','SK-O330, SK-L330, SK-R330, SK-D3309 series'),
('Silicone tube mat 50 mL','18202846','Tube mat, supports 6 x 50 mL tubes','SK-O330, SK-L330, SK-R330, SK-D3309 series'),
('SK180.4 non-slip platform','18900185','Anti-slip platform, external size 24 x 21.5 cm','SK-O180, SK-L180, SK-R1807, SK-D1810 series'),
('SK330.4 universal platform','18900659','Universal platform, external size 34 x 34 cm','SK-O330-M'),
('SK330.6 bar platform','18900059','Bar platform for SK-O330-M / SK-O330-Pro / SK-L330-Pro','SK330 platform family'),
('SK180.5 bar platform','18900060','Bar platform for SK-O180-Pro / SK-L180-Pro','SK180 platform family'),
('Silicone tube mat 10 mL','18202852','Tube mat, supports 10 x 5-10 mL tubes','SK180 platform family'),
('Silicone tube mat 5 mL','18202853','Tube mat, supports 4 x 50 mL tubes','SK180 platform family'),
('SK330.1 universal clamp platform','18900027','33 x 23 cm platform with springs and flask clamp holes','SK-O330, SK-L330, SK-R330, SK-D3309 series'),
('SK330.3 universal clamp platform','18900040','32 x 32 cm platform for flask clamps and tube racks','SK-O330, SK-L330, SK-R330, SK-D3309 series'),
('SK180.1 universal clamp platform','18900025','25 x 24.5 cm platform for flask clamps','SK-O180, SK-L180, SK-R1807, SK-D1810 series'),
('SK180.3 universal clamp platform','18900038','25 x 24.5 cm platform for flask clamps and tube racks','SK-O180, SK-L180, SK-R1807, SK-D1810 series'),
('SK180.6 non-slip mat','18901220','23.8 x 23.8 cm silicone mat, maximum speed 220 rpm','SK180 platform family'),
('SK330.8 non-slip mat','18900211','28.4 x 29.6 cm silicone mat, maximum speed 220 rpm','SK330 platform family'),
('Black flask-clamp fixing rod for SK330','18900036','Clamp fixing rod for universal platform 18900027','SK330 clamp platforms'),
('Black flask-clamp fixing rod for SK180','18900037','Clamp fixing rod for universal platform 18900025','SK180 clamp platforms'),
('Double rod connector','18900280','Connector for connecting two fixing rods','SK platform accessories'),
('SK330.2 perforated platform','18900028','32 x 32 cm perforated platform','SK330 platform family'),
('SK180.2 perforated platform','18900026','25 x 24 cm perforated platform','SK180 platform family'),
('25 mL conical flask clamp','18900029','Clamp for conical flasks; platform quantity depends on platform model','SK platform family'),
('50 mL conical flask clamp','18900030','Clamp for conical flasks; platform quantity depends on platform model','SK platform family'),
('100 mL conical flask clamp','18900031','Clamp for conical flasks; platform quantity depends on platform model','SK platform family'),
('200/250 mL conical flask clamp','18900032','Clamp for conical flasks; platform quantity depends on platform model','SK platform family'),
('500 mL conical flask clamp','18900033','Clamp for conical flasks; platform quantity depends on platform model','SK platform family'),
('SK330 test-tube rack clamp','18900079','Rack clamp, 4 x 55 mm high; width 57.2 mm; usable width 29 mm','SK330 platform family'),
]

FULL_SPECS = {
'AF-MX-S': [('Voltage','100-120 V / 200-240 V, 50/60 Hz'),('Power','60 W'),('Mixing motion','Circular'),('Orbit diameter','4 mm'),('Motor type','Shaded-pole motor'),('Motor input power','58 W'),('Motor output power','10 W'),('Speed range','0-3000 rpm'),('Speed display','Scale'),('Operating mode','Touch mode and continuous mode'),('Dimensions (L x W x H)','127 x 130 x 160 mm'),('Weight','2.0 kg'),('Permissible ambient temperature','5-40 C'),('Permissible relative humidity','80% RH'),('Protection class','IP21'),('Standard head','VT1.1 standard head, reference code 18900034, for tubes and small vessels below 30 mm diameter')],
'AF-MX-F': [('Voltage','100-120 V / 200-240 V, 50/60 Hz'),('Power','60 W'),('Mixing motion','Circular'),('Orbit diameter','4 mm'),('Motor type','Shaded-pole motor'),('Motor input power','58 W'),('Motor output power','10 W'),('Speed','3000 rpm fixed'),('Speed display','Not applicable'),('Operating mode','Touch mode and continuous mode'),('Dimensions (L x W x H)','127 x 130 x 160 mm'),('Weight','2.0 kg'),('Permissible ambient temperature','5-40 C'),('Permissible relative humidity','80% RH'),('Protection class','IP21'),('Standard head','VT1.1 standard head, reference code 18900034, for tubes and small vessels below 30 mm diameter')],
'AF-MX-SPLUS': [('Speed range','100-3000 rpm'),('Display','LCD'),('Orbit diameter','4 mm'),('Operating mode','Touch mode and continuous mode'),('Timer range','1 s to 99 min 59 s'),('Motor type','Brushless DC motor'),('Dimensions (L x W x H)','160 x 146 x 115 mm'),('Weight','3.4 kg'),('Power supply','100-240 V, 50/60 Hz'),('Input voltage','12 V'),('Power','25 W'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Protection class','IP21')],
'AF-MX-PRO': [('Speed range','100-3000 rpm'),('Display','LCD'),('Orbit diameter','4.5 mm'),('Operating mode','Light-sensing mode and continuous mode'),('Timer range','1 s to 99 min 59 s'),('Motor type','Brushless DC motor'),('Dimensions (L x W x H)','160 x 145 x 145 mm'),('Weight','3.9 kg'),('Power supply','100-240 V, 50/60 Hz'),('Input voltage','24 V'),('Power','30 W'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Protection class','IP21')],
'AF-MX-E': [('Voltage','100-240 V'),('AC frequency','50/60 Hz'),('Power','12 W'),('Mixing motion','Circular'),('Orbit diameter','4.8 mm'),('Motor output power','10 W'),('Speed','3000 rpm fixed'),('Operating mode','Touch mode'),('Instrument dimensions','133 x 133 x 80 mm'),('Package dimensions','250 x 185 x 130 mm'),('Weight','0.6 kg'),('Permissible ambient temperature','5-40 C'),('Permissible relative humidity','80% RH or lower'),('Protection class','IP21')],
'AF-MX-C': [('Function','Disruption of yeast, fungi, bacteria, algae, and sample processing after preparation of cell suspensions'),('Operating mode','High-speed circular vortex and vibration function'),('Orbit diameter','4 mm'),('Speed range','0-3000 rpm, adjustable'),('Speed display','Scale'),('Throughput','8 x 2 mL'),('Voltage','200-240 V / 100-120 V, 50/60 Hz, 60 W'),('Dimensions (L x W x H)','127 x 130 x 160 mm'),('Weight','2.0 kg')],
'AF-MX-M': [('Operating mode','Circular'),('Orbit diameter','4.5 mm'),('Maximum load with holder','0.5 kg'),('Motor type','Brushless DC motor'),('Motor input power','18 W'),('Motor output power','10 W'),('Speed range','Single microplate: 0-1500 rpm; double microplate: 0-1000 rpm'),('Speed display','Scale'),('Voltage','100-240 V, 50/60 Hz'),('Power','20 W'),('Dimensions','260 x 150 x 80 mm'),('Weight','3 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Protection class','IP21')],
'AF-MX-RD-PRO': [('Motor type','Brushless DC motor'),('Host adjustable angle','0-90 degrees'),('Speed range','10-70 rpm'),('Speed display','LCD'),('Timer display','LCD'),('Timer setting range','1-1199 min'),('Operating mode','Continuous mode and timer mode'),('Voltage','100-240 V, 50/60 Hz'),('Power','40 W'),('Dimensions (L x W x H)','280 x 210 x 300 mm'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Protection class','IP21')],
'AF-MX-RL-PRO': [('Motor type','Brushless DC motor'),('Speed range','10-70 rpm'),('Speed display','LCD'),('Timer display','LCD'),('Timer setting range','1-1199 min'),('Operating mode','Continuous mode and timer mode'),('Voltage','100-240 V, 50/60 Hz'),('Power','40 W'),('Dimensions (L x W x H)','220 x 510 x 260 mm'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Protection class','IP21')],
'AF-MX-RD-E': [('Motor type','DC motor'),('Speed range','0-80 rpm'),('Speed display','Scale'),('Operating mode','Continuous mode'),('Voltage','100-240 V, 50/60 Hz'),('Power','20 W'),('Dimensions (L x W x H)','300 x 220 x 310 mm'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Protection class','IP21')],
'AF-MX-RL-E': [('Motor type','DC motor'),('Speed range','0-80 rpm'),('Speed display','Scale'),('Operating mode','Continuous mode'),('Voltage','100-240 V, 50/60 Hz'),('Power','20 W'),('Dimensions (L x W x H)','150 x 530 x 190 mm'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Protection class','IP21')],
'AF-SK-R30S-E': [('Tilt angle','30 +/- 3 degrees'),('Load','1 kg'),('Motor type','Brushless DC motor'),('Speed range','0-30 rpm'),('Operating mode','Continuous operation'),('Dimensions (L x W x H)','295 x 160 x 120 mm'),('Voltage','100-240 V, 50/60 Hz'),('Power','15 W'),('Weight','1.8 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH')],
'AF-SK-R30L-E': [('Tilt angle','30 +/- 3 degrees'),('Load','1 kg'),('Motor type','Brushless DC motor'),('Speed range','0-30 rpm'),('Operating mode','Continuous operation'),('Dimensions (L x W x H)','405 x 160 x 120 mm'),('Voltage','100-240 V, 50/60 Hz'),('Power','15 W'),('Weight','2.0 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH')],
'AF-SK-R30D-E': [('Tilt angle','40 +/- 3 degrees'),('Load','1 kg'),('Motor type','Brushless DC motor'),('Speed range','0-30 rpm'),('Operating mode','Continuous operation'),('Dimensions (L x W x H)','405 x 160 x 160 mm'),('Voltage','100-240 V, 50/60 Hz'),('Power','15 W'),('Weight','2.2 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH')],
'AF-MX-T6-PRO': [('Amplitude','24 mm'),('Motor type','Brushless DC motor'),('Motion','Rocking and rolling'),('Maximum load','4 kg'),('Number of rollers','6'),('Roller length','280 mm'),('Speed range','10-70 rpm'),('Speed display','LCD'),('Timer','Available'),('Timer display','LCD'),('Timer setting range','1-1199 min'),('Operating mode','Continuous mode and timer operation'),('Voltage','100-240 V, 50/60 Hz'),('Power','30 W'),('Dimensions (L x W x H)','485 x 250 x 100 mm'),('Weight','5.1 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Protection class','IP21')],
'AF-MX-T6-SPLUS': [('Amplitude','24 mm'),('Motor type','Brushless DC motor'),('Motion','Rocking and rolling'),('Maximum load','4 kg'),('Number of rollers','6'),('Roller length','280 mm'),('Speed range','0-70 rpm'),('Speed display','Scale'),('Timer','Not available'),('Operating mode','Continuous operation'),('Voltage','100-240 V, 50/60 Hz'),('Power','25 W'),('Dimensions (L x W x H)','485 x 250 x 100 mm'),('Weight','4.5 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Protection class','IP21')],
'AF-SK-O330-PRO': [('Orbit diameter','10 mm'),('Maximum load','7.5 kg'),('Motor type','Brushless DC motor'),('Motor input power','28 W'),('Motor output power','15 W'),('Speed range','100-500 rpm'),('Speed display','LCD'),('Timer display','LCD'),('Timer setting range','1 min to 99 h 59 min'),('Voltage','100-240 V, 50/60 Hz'),('Power','30 W'),('Weight','12 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Platform size','32 x 32 cm'),('Dimensions (L x W x H)','370 x 420 x 100 mm'),('Protection class','IP21'),('Data interface','RS232')],
'AF-SK-O180-PRO': [('Orbit diameter','4 mm'),('Maximum load','2.5 kg'),('Motor type','Brushless DC motor'),('Motor input power','28 W'),('Motor output power','15 W'),('Speed range','100-800 rpm'),('Speed display','LCD'),('Timer display','LCD'),('Timer setting range','1 min to 99 h 59 min'),('Voltage','100-240 V, 50/60 Hz'),('Power','30 W'),('Weight','8.1 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Platform size','25 x 24.5 cm'),('Dimensions (L x W x H)','300 x 340 x 100 mm'),('Protection class','IP20'),('Data interface','RS232')],
'AF-SK-O330-M': [('Orbit diameter','10 mm'),('Maximum load','3 kg'),('Motor type','Brushless DC motor'),('Motor input power','20 W'),('Motor output power','15 W'),('Speed range','70-400 rpm'),('Speed display','LCD'),('Timer display','LCD'),('Timer setting range','1 min to 99 h 59 min'),('Voltage','100-240 V, 50/60 Hz'),('Power','25 W'),('Weight','9.8 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Platform size','33.5 x 33.5 cm'),('Dimensions (L x W x H)','420 x 370 x 100 mm'),('Protection class','IP21'),('Working tray size','335 x 335 mm')],
'AF-SK-O180-C': [('Amplitude','20 mm'),('Maximum load including fixture','2 kg'),('Motor type','Brushless DC motor'),('Motor input power','16 W'),('Motor output power','10 W'),('Speed range','40-200 rpm'),('Main unit display','LED'),('Remote controller display','4.3-inch LCD screen'),('Timer setting range','1 min to 99 h 59 min'),('Voltage','100-240 V, 50/60 Hz'),('Power','20 W'),('Weight','3.4 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Dimensions (L x W x H)','Main unit: 294 x 348 x 130 mm; remote controller: 190 x 90 x 30 mm'),('Protection class','IP21'),('Interface','RS232')],
'AF-SK-O180-S': [('Orbit diameter','20 mm'),('Maximum load','2 kg'),('Motor type','Brushless DC motor'),('Motor input power','20 W'),('Motor output power','16 W'),('Speed range','40-200 rpm'),('Speed display','LED'),('Timer display','LED'),('Timer setting range','1 min to 99 h 59 min'),('Voltage','100-240 V, 50/60 Hz'),('Power','20 W'),('Weight','3.1 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Platform size','26.8 x 26.8 cm'),('Dimensions (L x W x H)','294 x 348 x 123 mm'),('Protection class','IP21'),('Working tray size','268 x 268 mm')],
'AF-SK-L330-PRO': [('Amplitude','10 mm'),('Maximum load including fixture','7.5 kg'),('Motor type','Brushless DC motor'),('Motor input power','28 W'),('Motor output power','15 W'),('Speed range','100-350 rpm'),('Speed display','LCD'),('Timer display','LCD'),('Timer setting range','1 min to 99 h 59 min'),('Voltage','100-240 V, 50/60 Hz'),('Power','30 W'),('Weight','13.5 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Platform size','32 x 32 cm'),('Dimensions (L x W x H)','370 x 420 x 100 mm'),('Protection class','IP21'),('Data interface','RS232')],
'AF-SK-L180-PRO': [('Amplitude','4 mm'),('Maximum load including fixture','2.5 kg'),('Motor type','Brushless DC motor'),('Motor input power','28 W'),('Motor output power','15 W'),('Speed range','100-350 rpm'),('Speed display','LCD'),('Timer display','LCD'),('Timer setting range','1 min to 99 h 59 min'),('Voltage','100-240 V, 50/60 Hz'),('Power','30 W'),('Weight','8.1 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Platform size','25 x 24.5 cm'),('Dimensions (L x W x H)','300 x 340 x 100 mm'),('Protection class','IP21'),('Data interface','RS232')],
'AF-SK-L180-S': [('Amplitude','20 mm'),('Maximum load including fixture','2 kg'),('Motor type','Brushless DC motor'),('Motor input power','16 W'),('Motor output power','10 W'),('Speed range','40-200 rpm'),('Speed display','LED'),('Timer display','LED'),('Timer setting range','1 min to 99 h 59 min'),('Voltage','100-240 V, 50/60 Hz'),('Power','20 W'),('Weight','3.4 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Platform size','26.8 x 26.8 cm'),('Dimensions (L x W x H)','294 x 348 x 130 mm'),('Protection class','IP21'),('Data interface','Not available')],
'AF-SK-R330-PRO': [('Tilt angle','9 degrees'),('Maximum load','10 kg'),('Motor type','DC motor'),('Motor input power','40 W'),('Motor output power','24 W'),('Speed range','10-70 rpm'),('Speed display','LCD'),('Timer display','LCD'),('Timer setting range','1 min to 99 h 59 min'),('Voltage','100-240 V, 50/60 Hz'),('Power','50 W'),('Weight','9 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Platform size','30 x 28.5 cm'),('Dimensions (L x W x H)','360 x 410 x 200 mm'),('Protection class','IP21')],
'AF-SK-R1807-S': [('Tilt angle','7 degrees'),('Maximum load','2 kg'),('Motor type','DC motor'),('Motor input power','20 W'),('Motor output power','16 W'),('Speed range','10-80 rpm'),('Speed display','LED'),('Timer display','LED'),('Timer setting range','1 min to 99 h 59 min'),('Voltage','100-240 V, 50/60 Hz'),('Power','20 W'),('Weight','3.1 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Platform size','26.8 x 26.8 cm'),('Dimensions (L x W x H)','294 x 348 x 123 mm'),('Protection class','IP21')],
'AF-SK-D3309-PRO': [('Tilt angle','9 degrees'),('Maximum load','5 kg'),('Motor type','DC motor'),('Motor input power','40 W'),('Motor output power','24 W'),('Speed range','10-70 rpm'),('Speed display','LCD'),('Timer display','LCD'),('Timer setting range','1 min to 99 h 59 min'),('Voltage','100-240 V, 50/60 Hz'),('Power','50 W'),('Weight','9 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Platform size','30 x 28.5 cm'),('Dimensions (L x W x H)','360 x 430 x 106 mm'),('Protection class','IP21')],
'AF-SK-D1810-S': [('Tilt angle','10 degrees'),('Maximum load','2 kg'),('Motor type','DC motor'),('Motor input power','16 W'),('Motor output power','10 W'),('Speed range','10-80 rpm'),('Speed display','LED'),('Timer display','LED'),('Timer setting range','1 min to 99 h 59 min'),('Voltage','100-240 V, 50/60 Hz'),('Power','20 W'),('Weight','3.7 kg'),('Permissible ambient temperature and humidity','5-40 C, 80% RH'),('Platform size','26.8 x 26.8 cm'),('Dimensions (L x W x H)','294 x 348 x 170 mm'),('Protection class','IP21')],
}

def mixer_code(prod):
    cn, model, en, intro, specs = prod
    specs = FULL_SPECS.get(model, specs)
    ordering_rows = [[model, en.replace('ATOMFAIR® ',''), '; '.join(f'{k}: {v}' for k, v in specs)]]
    return page(en, model, 'Mixing and Shaking Series',
        [intro, 'The instrument is configured around the source manual product name while Atomfair provides unified ordering models, English product documentation, and accessory mapping for complete quotation and catalog use.'],
        features_default, specs, (['Order Model','Product','Configuration Notes'], ordering_rows))

mixer_records = []
for prod in mixer_products:
    code = mixer_code(prod)
    (MIX_DIR / (slug(prod[1]) + '.html')).write_text(code, encoding='utf-8')
    mixer_records.append(record(prod[0], prod[1], prod[2], prod[3], code, 'Mixers and Shakers'))

for i, a in enumerate(mixer_accessories, 1):
    name, ref, spec, compat = a
    model = f'AF-MX-ACC-{i:03d}'
    en = f'ATOMFAIR® {name}'
    intro = f'{name} is an Atomfair mixing and shaking accessory for {compat.lower()}, with specification: {spec}.'
    code = page(en, model, 'Mixing and Shaking Accessory',
        [intro, 'This accessory is listed separately so ordering, replacement, compatibility checking, and after-sales support can be handled without losing the original configuration details from the product manual.'],
        ['Dedicated accessory record with unique Atomfair model.', 'Reference code from the source manual is retained for cross-checking.', 'Compatibility and capacity information is kept in structured tables.', 'Used to configure vortex mixers, rotators, rollers, rockers, orbital shakers, linear shakers, or 3D shakers according to application needs.'],
        [('Accessory name', name), ('Reference code', ref), ('Specification', spec), ('Compatibility / use', compat)],
        (['Order Model','Reference Code','Accessory','Compatibility'], [[model, ref, name, compat]]))
    (MIX_DIR / (slug(model) + '_' + slug(name) + '.html')).write_text(code, encoding='utf-8')
    mixer_records.append(record('混匀摇床配件 ' + name, model, en, intro, code, 'Mixers and Shakers Accessories'))

power_specs = [
('DEP-300','AF-EP-DEP300','ATOMFAIR® DEP-300 Electrophoresis Power Supply','LCD touch screen; voltage 0-300 V; current 0-600 mA; power 0-150 W; constant voltage/current/power output; 4 output groups; USB data recording; 100-140 V / 195-245 V, 50/60 Hz; 310 x 260 x 115 mm; 1.90 kg'),
('DEP-600','AF-EP-DEP600','ATOMFAIR® DEP-600 Electrophoresis Power Supply','LCD touch screen; voltage 0-600 V; current 0-600 mA; power 0-360 W; constant voltage/current/power output; 4 output groups; USB data recording; 100-140 V / 195-245 V, 50/60 Hz; 310 x 260 x 115 mm; 1.96 kg'),
('DEP-300HC','AF-EP-DEP300HC','ATOMFAIR® DEP-300HC Electrophoresis Power Supply','LCD touch screen; voltage 0-300 V; current 0-3000 mA; power 0-400 W; constant voltage/current/power output; 4 output groups; USB data recording; 100-240 V, 50/60 Hz; 310 x 260 x 115 mm; 2.05 kg'),
('DEP-600HC','AF-EP-DEP600HC','ATOMFAIR® DEP-600HC Electrophoresis Power Supply','LCD touch screen; voltage 0-600 V; current 0-2500 mA; power 0-500 W; constant voltage/current/power output; 4 output groups; USB data recording; 100-240 V, 50/60 Hz; 310 x 260 x 115 mm; 2.05 kg'),
]

POWER_FULL_SPECS = {
'AF-EP-DEP300': [('Display','LCD touch screen'),('Program capacity','Stores up to 20 programs; each program supports up to 20 steps'),('Output type','Constant voltage, constant current and constant power output, continuously adjustable'),('Voltage range','0-300 V'),('Current range','0-600 mA'),('Power range','0-150 W'),('Resolution','Voltage 1 V, current 1 mA, power 1 W'),('Timer setting range','1 min to 99 h 59 min'),('Interface','USB'),('Output sockets','4 groups'),('Input voltage','100-140 V / 195-245 V, 50/60 Hz'),('Ambient temperature and humidity','0-40 C, <=95% RH'),('Dimensions (L x W x H)','310 x 260 x 115 mm'),('Weight','1.90 kg')],
'AF-EP-DEP600': [('Display','LCD touch screen'),('Program capacity','Stores up to 20 programs; each program supports up to 20 steps'),('Output type','Constant voltage, constant current and constant power output, continuously adjustable'),('Voltage range','0-600 V'),('Current range','0-600 mA'),('Power range','0-360 W'),('Resolution','Voltage 1 V, current 1 mA, power 1 W'),('Timer setting range','1 min to 99 h 59 min'),('Interface','USB'),('Output sockets','4 groups'),('Input voltage','100-140 V / 195-245 V, 50/60 Hz'),('Ambient temperature and humidity','0-40 C, <=95% RH'),('Dimensions (L x W x H)','310 x 260 x 115 mm'),('Weight','1.96 kg')],
'AF-EP-DEP300HC': [('Display','LCD touch screen'),('Program capacity','Stores up to 20 programs; each program supports up to 20 steps'),('Output type','Constant voltage, constant current and constant power output, continuously adjustable'),('Voltage range','0-300 V'),('Current range','0-3000 mA'),('Power range','0-400 W'),('Resolution','Voltage 1 V, current 1 mA, power 1 W'),('Timer setting range','1 min to 99 h 59 min'),('Interface','USB'),('Output sockets','4 groups'),('Input voltage','100-240 V, 50/60 Hz'),('Ambient temperature and humidity','0-40 C, <=95% RH'),('Dimensions (L x W x H)','310 x 260 x 115 mm'),('Weight','2.05 kg')],
'AF-EP-DEP600HC': [('Display','LCD touch screen'),('Program capacity','Stores up to 20 programs; each program supports up to 20 steps'),('Output type','Constant voltage, constant current and constant power output, continuously adjustable'),('Voltage range','0-600 V'),('Current range','0-2500 mA'),('Power range','0-500 W'),('Resolution','Voltage 1 V, current 1 mA, power 1 W'),('Timer setting range','1 min to 99 h 59 min'),('Interface','USB'),('Output sockets','4 groups'),('Input voltage','100-240 V, 50/60 Hz'),('Ambient temperature and humidity','0-40 C, <=95% RH'),('Dimensions (L x W x H)','310 x 260 x 115 mm'),('Weight','2.05 kg')],
}

ep_products = [
('迷你型垂直电泳槽 DL-Mini01','AF-EP-DL-MINI01','ATOMFAIR® DL-Mini01 Mini Vertical Electrophoresis Cell','Gel area 83 x 73 mm; gel thickness 0.75, 1.0, or 1.5 mm; comb options 10 or 15 teeth.'),
('迷你型垂直电泳槽 DL-Mini04','AF-EP-DL-MINI04','ATOMFAIR® DL-Mini04 Mini Vertical Electrophoresis Cell','Gel quantity 1-4 gels; gel thickness 0.75, 1.0, or 1.5 mm; comb options 10 or 15 teeth; short plate 10.1 x 7.3 cm; long plate 10.1 x 8.2 cm; max hand-cast gel 8.3 x 7.3 cm; precast gel 8.6 x 6.8 cm.'),
('迷你型转移电泳槽 DL-ZY02','AF-EP-DL-ZY02','ATOMFAIR® DL-ZY02 Mini Transfer Electrophoresis Cell','Transfer area 110 x 90 mm; 4 cm electrode spacing; built-in ice box.'),
('迷你型转移电泳槽 DL-ZY03','AF-EP-DL-ZY03','ATOMFAIR® DL-ZY03 Mini Transfer Electrophoresis Cell','Transfer area 110 x 90 mm; 4 cm electrode spacing; built-in ice box and gas bubble roller.'),
('迷你型转移电泳槽 DL-ZY04','AF-EP-DL-ZY04','ATOMFAIR® DL-ZY04 Mini Transfer Electrophoresis Cell','Transfer area 110 x 90 mm; 5.5 cm electrode spacing; supports up to 83 x 73 mm gel transfer; includes gas bubble roller and filter paper.'),
('水平电泳槽 DL-SUB01','AF-EP-DL-SUB01','ATOMFAIR® DL-SUB01 Horizontal Electrophoresis Cell','Gel area 75 x 60 mm; sample throughput 6 or 11; buffer volume 300 mL.'),
('多功能型水平电泳槽 DL-SUB02','AF-EP-DL-SUB02','ATOMFAIR® DL-SUB02 Multifunction Horizontal Electrophoresis Cell','Gel areas: 120 x 120 mm, 120 x 60 mm, 60 x 120 mm, 60 x 60 mm; sample throughput 2, 3, 6, 8, 11, 13, 18, or 25; buffer volume 700 mL.'),
('多功能型水平电泳槽 DL-SUB03','AF-EP-DL-SUB03','ATOMFAIR® DL-SUB03 Multifunction Horizontal Electrophoresis Cell','Gel areas 13 x 20 cm and 13 x 15 cm; combs 1.0 mm 14, 18, and 26 teeth, 1.5 mm 18 teeth; buffer volume 800 mL; product size 340 x 170 x 130 mm; weight 0.94 kg.'),
('多功能型蓝光一体水平电泳槽 DL-SUB03+','AF-EP-DL-SUB03PLUS','ATOMFAIR® DL-SUB03+ Blue-Light Integrated Horizontal Electrophoresis Cell','Gel areas 13 x 20 cm and 13 x 15 cm; combs 1.0 mm 14, 18, and 26 teeth, 1.5 mm 18 teeth; buffer volume 800 mL; platinum alloy electrode 0.2 mm; product size 340 x 170 x 130 mm; weight 1.2 kg.'),
]

ep_configs = {
'AF-EP-DL-MINI01':[('Electrophoresis tank upper cover with wires','set','1'),('Electrophoresis tank lower tank','pc','1'),('Electrode core','set','1'),('Gel-casting glass plate','pc','5'),('Gel-casting thin glass plate','pc','5'),('10-well comb','pc','2'),('15-well comb','pc','2'),('Gel-making frame','pc','2'),('Clamp frame','pc','2'),('Glue shovel','pc','1'),('Single gel plate','pc','1')],
'AF-EP-DL-MINI04':[('Electrophoresis tank upper cover with wires','set','1'),('Electrophoresis tank lower tank','pc','1'),('Electrode core','pc','1'),('Electrode core','pc','1'),('Gel-casting glass plate','pc','5'),('Gel-casting thin glass plate','pc','5'),('10-well comb','pc','5'),('Continuous gel spacer','pc','2'),('Gasket','pc','4'),('Glue shovel','pc','1'),('Single gel plate','pc','1')],
'AF-EP-DL-ZY02':[('Electrophoresis tank upper cover with wires','set','1'),('Electrophoresis tank lower tank','pc','1'),('Transfer core','set','1'),('Three-sided transfer clamp','set','2'),('Transfer sponge pad','pc','4'),('White ice box','pc','1'),('Blue ice box','pc','2'),('Gas bubble roller','pc','1')],
'AF-EP-DL-ZY03':[('Electrophoresis tank upper cover with wires','set','1'),('Electrophoresis tank lower tank with electrode','set','1'),('Transfer core','set','1'),('Three-sided transfer clamp','set','2'),('Transfer sponge pad','pc','4'),('Blue ice box','pc','1'),('Gas bubble roller','pc','1')],
'AF-EP-DL-ZY04':[('Electrophoresis tank upper cover with wires','set','1'),('Electrophoresis tank lower tank','pc','1'),('Transfer core','set','1'),('Three-sided transfer clamp','set','4'),('Transfer sponge pad','pc','8'),('Blue ice box','pc','1'),('Gas bubble roller','pc','1'),('Filter paper','sheet','20')],
'AF-EP-DL-SUB01':[('Electrophoresis tank main body with electrode','pc','1'),('Electrophoresis tank upper cover with wire','pc','1'),('Gel tray','pc','1'),('Gel-making instrument','pc','1'),('1.0 mm 6-tooth comb','pc','2'),('1.5 mm 6-tooth comb','pc','2'),('1.5 mm 11-tooth comb','pc','2'),('1.0 mm 11-tooth comb','pc','2')],
'AF-EP-DL-SUB02':[('Electrophoresis tank upper cover with wires','set','1'),('Electrophoresis tank lower tank with electrode','set','1'),('Gel-making instrument','pc','1'),('Large gel tray 120 x 120','pc','1'),('Wide gel tray 120 x 60','pc','1'),('Long gel tray 60 x 120','pc','1'),('Small gel tray 60 x 60','pc','2'),('Comb 1.0 mm 2+3 teeth','pc','1'),('Comb 1.0 mm 6+13 teeth','pc','1'),('Comb 1.0 mm 8+18 teeth','pc','1'),('Comb 1.0 mm 11+25 teeth','pc','4')],
'AF-EP-DL-SUB03':[('Electrophoresis tank upper cover with wires','set','1'),('Electrophoresis tank lower tank with electrode','set','1'),('Gel-making instrument','pc','1'),('Large gel tray 130 x 200','pc','1'),('Small gel tray 130 x 150','pc','1'),('Comb 1.0 mm 14 teeth','pc','2'),('Comb 1.0 mm 18 teeth','pc','2'),('Comb 1.0 mm 26 teeth','pc','2'),('Comb 1.5 mm 18 teeth','pc','2')],
'AF-EP-DL-SUB03PLUS':[('Electrophoresis tank upper cover with wires','set','1'),('Electrophoresis tank lower tank with electrode and blue-light module','set','1'),('Gel-making instrument','pc','1'),('Large gel tray 130 x 200','pc','1'),('Small gel tray 130 x 150','pc','1'),('Comb 1.0 mm 14 teeth','pc','2'),('Comb 1.0 mm 18 teeth','pc','2'),('Comb 1.0 mm 26 teeth','pc','2'),('Comb 1.5 mm 18 teeth','pc','2')]
}

ep_records = []
for src_model, model, en, desc in power_specs:
    spec_pairs = POWER_FULL_SPECS.get(model, [])
    code = page(en, model, 'Electrophoresis Power Supply',
        [desc, 'The DEP series supplies constant voltage, constant current, and constant power output modes for horizontal, vertical, transfer, and high-current electrophoresis workflows.'],
        ['4.3-inch LCD touch interface with clear menu prompts.', 'Programmable operation, method memory, USB data export, and multiple protection functions.', 'Four output sockets can drive four electrophoresis cells at the same time.', 'Anti-slip groove design and pop-up support improve bench use.'],
        spec_pairs, (['Order Model','Source Model','Core Configuration'], [[model, src_model, desc]]))
    (EP_DIR / (slug(model) + '.html')).write_text(code, encoding='utf-8')
    ep_records.append(record('电泳仪电源 ' + src_model, model, en, desc, code, 'Electrophoresis'))

for cn, model, en, desc in ep_products:
    configs = ep_configs.get(model, [])
    spec_pairs = []
    for part in desc.split('; '):
        if ':' in part:
            k, v = part.split(':', 1)
            spec_pairs.append((k.strip(), v.strip()))
        else:
            spec_pairs.append(('Specification', part))
    code = page(en, model, 'Electrophoresis Cell',
        [desc, 'The cell uses transparent molded materials and a source-manual configuration list so gel casting, running, transfer, and accessory replacement can be ordered without ambiguity.'],
        ['High-transparency molded tank body supports visual monitoring.', 'Dedicated electrodes, gel trays, clamps, combs, and casting parts are recorded as separate ordering items.', 'Configuration tables preserve quantities, units, and functional roles from the source manual.', 'Suitable for SDS-PAGE, native PAGE, agarose electrophoresis, membrane transfer, and nucleic-acid separation workflows according to model type.'],
        spec_pairs, (['Order Model','Product','Configuration Scope'], [[model, en.replace('ATOMFAIR® ', ''), 'Main cell plus listed standard configuration parts']]),
        [[n, '', f'Unit: {u}; quantity: {q}', model] for n, u, q in configs])
    (EP_DIR / (slug(model) + '.html')).write_text(code, encoding='utf-8')
    ep_records.append(record(cn, model, en, desc, code, 'Electrophoresis'))

seen = {}
for host, rows in ep_configs.items():
    for n, u, q in rows:
        key = n.lower()
        seen.setdefault(key, {'name': n, 'unit': u, 'hosts': [], 'qtys': []})
        seen[key]['hosts'].append(host)
        seen[key]['qtys'].append(q)

for i, item in enumerate(seen.values(), 1):
    model = f'AF-EP-ACC-{i:03d}'
    name = item['name']
    hosts = ', '.join(sorted(set(item['hosts'])))
    qty = ', '.join(item['qtys'])
    en = f'ATOMFAIR® {name}'
    intro = f'{name} is an electrophoresis accessory used in standard configurations for {hosts}.'
    code = page(en, model, 'Electrophoresis Accessory',
        [intro, 'It is separated as an independent Atomfair ordering line so replacement parts, standard configuration verification, and accessory replenishment can be handled accurately.'],
        ['Unique Atomfair accessory model for ordering and after-sales tracking.', 'Standard configuration quantities are preserved from the product manual.', 'Compatibility is listed by host electrophoresis cell model.', 'Useful for maintaining complete electrophoresis systems without losing small parts such as combs, trays, clamps, glass plates, and transfer items.'],
        [('Accessory name', name), ('Unit in source configuration', item['unit']), ('Source quantities observed', qty), ('Compatible host models', hosts)],
        (['Order Model','Accessory','Compatible Host Models','Observed Quantities'], [[model, name, hosts, qty]]))
    (EP_DIR / (slug(model) + '_' + slug(name) + '.html')).write_text(code, encoding='utf-8')
    ep_records.append(record('电泳仪配件 ' + name, model, en, intro, code, 'Electrophoresis Accessories'))

payload_mix = [{'sheetName': 'Mixer Shaker Series', 'folder': str(MIX_DIR), 'records': mixer_records}]
payload_ep = [{'sheetName': 'Electrophoresis Series', 'folder': str(EP_DIR), 'records': ep_records}]
OUT_MIX.write_text(json.dumps(payload_mix, ensure_ascii=False, indent=2), encoding='utf-8')
OUT_EP.write_text(json.dumps(payload_ep, ensure_ascii=False, indent=2), encoding='utf-8')

for label, records in [('mixer', mixer_records), ('electrophoresis', ep_records)]:
    bad = []
    for r in records:
        if re.search(r'[\u4e00-\u9fff]', r['代码']):
            bad.append((r['型号'], r['产品名称（英文）']))
    print(label, 'records', len(records), 'html_cjk_issues', len(bad))
