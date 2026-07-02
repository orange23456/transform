import json, re, html
from pathlib import Path

OUT = Path(r'C:\Users\hz-user\Desktop\全自动\generated_html_full\Atomfair_centrifuge_HTML')
JSON_OUT = Path(r'C:\Users\hz-user\Desktop\全自动\centrifuge_records.json')
OUT.mkdir(parents=True, exist_ok=True)

def esc(s): return html.escape(str(s or ''), quote=True)
def slug(s): return re.sub(r'[^A-Za-z0-9]+','_',str(s)).strip('_')[:90]
def li(xs): return ''.join(f'<li style="margin-bottom:9px;">{esc(x)}</li>' for x in xs)
def tr(rows): return ''.join(f'<tr><td style="border:1px solid #d7d7d7;padding:10px 12px;font-weight:700;vertical-align:top;">{esc(k)}</td><td style="border:1px solid #d7d7d7;padding:10px 12px;vertical-align:top;">{esc(v)}</td></tr>' for k,v in rows)
def otr(rows): return ''.join(f'<tr><td style="border:1px solid #d7d7d7;padding:10px 12px;font-weight:700;">{esc(a)}</td><td style="border:1px solid #d7d7d7;padding:10px 12px;">{esc(b)}</td><td style="border:1px solid #d7d7d7;padding:10px 12px;">{esc(c)}</td></tr>' for a,b,c in rows)
def ptxt(xs): return ''.join(f'<p style="margin:0 0 14px 0;font-size:15px;color:#444;text-align:justify;">{esc(x)}</p>' for x in xs)
items = []
def add(cn,en,model,kind,overview,features,specs,orders):
    items.append(dict(cn=cn,en=en,model=model,kind=kind,overview=overview,features=features,specs=specs,orders=orders))

add('D1012U 掌上离心机 / 微量高速离心机','Palm Micro High-Speed Centrifuge','AF-CF-MICRO-D1012U','Centrifuge',[
'The D1012U palm micro high-speed centrifuge is designed for rapid spin-down collection, micro-filtration and cell separation workflows, including pre- and post-PCR processing.',
'The compact unit combines one-knob time and speed operation, OLED display, wide-mouth rotor chamber and support for brake or inertial stop modes.'
],['Maximum speed 12000 rpm with 7490 x g maximum RCF.','OLED display supports speed and time display.','Includes rotors for microtubes, PCR strips and 0.2 mL PCR tubes.','Compact body with approximately 1.5 kg weight.'],[
('Speed range','1000-12000 rpm, step 1000 rpm'),('Maximum RCF','6708 x g for 0.5/1.5/2 mL tubes; 6596-7490 x g for PCR tubes'),('Rotor capacity','12 x 0.5/1.5/2 mL; 44 x 0.2 mL PCR tubes; 4 x 0.2 mL PCR 8-strip tubes'),('Time setting range','10 s to 20 min'),('Display','OLED'),('Motor type','DC motor'),('Acceleration / deceleration','1 up / 2 down'),('Power','AC100-240 V, 50/60 Hz, 40 W'),('Noise','Less than or equal to 58 dB'),('Dimensions','210 x 180 x 130 mm'),('Weight','1.5 kg')],[('AF-CF-MICRO-D1012U-01','D1012U standard unit','1000-12000 rpm palm micro high-speed centrifuge')])

add('D1008/D1008E 掌上离心机 / 低速离心机','Palm Low-Speed Centrifuge Series','AF-CF-PALM-D1008','Centrifuge',[
'The D1008/D1008E palm centrifuge series is prepared for rapid spin-down, micro-filtration and cell separation with compact, quiet operation.',
'The series uses simple switching, low-noise running and interchangeable rotors for microtubes and PCR tubes.'
],['Simple on/off operation with lid-closing start and lid-opening stop.','Stable and quiet operation with noise less than or equal to 45 dB.','Compatible with 8 x 2 mL rotor and 4 x PCR strip rotor.'],[
('D1008 maximum speed','7000 rpm'),('D1008E maximum speed','5000 rpm'),('D1008 maximum RCF','2680 x g'),('D1008E maximum RCF','1360 x g'),('Rotor capacity','8 x 0.2/0.5/1.5/2 mL; 32 x 0.2 mL PCR tubes; 4 x 0.2 mL PCR 8-strips'),('Running mode','Continuous operation'),('Motor type','DC motor'),('Power','AC100-240 V, 50/60 Hz, 20 W'),('Noise','Less than or equal to 45 dB'),('Dimensions','160 x 170 x 122 mm'),('Weight','0.5 kg')],[('AF-CF-PALM-D1008-01','D1008 unit','7000 rpm, 2680 x g'),('AF-CF-PALM-D1008E-02','D1008E unit','5000 rpm, 1360 x g')])

add('D2012S 小型离心机 / 微量高速离心机','Compact Micro High-Speed Centrifuge','AF-CF-MICRO-D2012S','Centrifuge',[
'The D2012S compact micro high-speed centrifuge is designed for molecular biology sample preparation including DNA/RNA extraction, nucleic acid purification, virus separation and micro-sample processing.',
'The system provides instant spin, fast operation, variable speed control and multiple rotor options for microtubes and PCR tubes.'
],['Maximum speed 15000 rpm and maximum RCF 16520 x g.','Brushless DC motor accelerates quickly to set speed.','Quiet running with noise less than or equal to 55 dB.','Door-lock, over-speed and status diagnosis protection.'],[
('Speed range','300-15000 rpm, step 100 rpm'),('Speed accuracy','+/-20 rpm'),('Maximum RCF','16520 x g'),('Rotor capacity','12 x 0.2/0.5/1.5/2 mL; 18 x 0.2/0.5/1.5/2 mL; 6 x 0.5/1.5/2 mL; 4 x 0.2 mL PCR strips'),('Time setting range','30 s to 99 min'),('Motor type','Brushless DC motor'),('Safety','Door lock, over-speed, over-temperature and status diagnosis'),('Display','LCD'),('Power','100-240 V, 50/60 Hz, 70 W'),('Noise','Less than or equal to 55 dB'),('Dimensions','272 x 260 x 154 mm'),('Weight','6.2 kg')],[('AF-CF-MICRO-D2012S-01','D2012S unit','300-15000 rpm compact micro high-speed centrifuge')])

add('D2012 Plus 小型离心机 / 微量高速离心机','Compact Micro High-Speed Centrifuge Plus','AF-CF-MICRO-D2012P','Centrifuge',[
'The D2012 Plus micro centrifuge is a compact high-speed centrifuge for molecular biology and clinical sample preparation where fast, quiet and safe operation is required.',
'It supports instant spin, fast acceleration, speed/RCF switching and multiple adapters for common microtube volumes.'
],['Maximum speed 15000 rpm and maximum RCF 15100 x g.','Quiet operation with noise less than or equal to 54 dB.','Door-lock and over-speed detection improve safety.','Conforms to IEC/EN 61010-2-20 centrifuge safety requirements.'],[
('Maximum speed','15000 rpm, 500-15000 rpm, step 100 rpm'),('Maximum RCF','15100 x g, step 100 x g'),('Speed accuracy','+/-20 rpm'),('Rotor capacity','12 x 0.2/0.5/1.5/2 mL'),('Running time','30 s to 99 min, continuous operation'),('Acceleration / deceleration','11 s up / 9 s down'),('Motor type','Brushless DC motor'),('Power','AC100-240 V, 50/60 Hz, 70 W'),('Noise','Less than or equal to 54 dB'),('Dimensions','255 x 245 x 140 mm'),('Weight','6 kg')],[('AF-CF-MICRO-D2012P-01','D2012 Plus unit','500-15000 rpm compact micro high-speed centrifuge plus')])
add('DG1616/DG1616RE 大容量高速离心机 / 大容量高速冷冻离心机','Large-Capacity High-Speed Centrifuge Series','AF-CF-HC-DG1616','Centrifuge',[
'The DG1616/DG1616RE large-capacity centrifuge series is designed for laboratories requiring high-speed processing of larger sample volumes across life science, pharmaceutical, environmental, food, soil, petrochemical, textile and microbiology applications.',
'The refrigerated model supports low-temperature separation for temperature-sensitive samples, while both models provide high capacity, rotor recognition, imbalance protection and program storage.'
],['Maximum speed 16000 rpm and maximum RCF 28621 x g.','Refrigerated model supports -20 C to 40 C operation.','Fast cooling from room temperature to 4 C in approximately seven minutes.','Stores up to 100 programs.','Compatible with broad rotor and adapter selections.'],[
('Maximum speed','16000 rpm, 300-16000 rpm, step 1 rpm'),('Maximum RCF','28621 x g, step 1 x g'),('Maximum capacity','4 x 400 mL'),('Timer','30 s to 99 h 59 min 59 s, continuous operation'),('Temperature range','DG1616RE: -20 C to 40 C'),('Acceleration / deceleration','9 up / 9 down'),('Program storage','100 programs'),('Motor type','Brushless DC motor'),('Noise','Less than or equal to 70 dB'),('DG1616 power','100-240 V, 50/60 Hz, 650 W'),('DG1616RE power','100-240 V, 50/60 Hz, 1050 W'),('DG1616 dimensions','440 x 640 x 375 mm'),('DG1616RE dimensions','623 x 640 x 375 mm'),('DG1616 weight','70 kg'),('DG1616RE weight','90 kg')],[('AF-CF-HC-DG1616-01','DG1616 unit','16000 rpm, 28621 x g, 4 x 400 mL'),('AF-CF-HC-DG1616RE-02','DG1616RE unit','16000 rpm, 28621 x g, -20 C to 40 C, 4 x 400 mL')])

add('D1524/D1524R 高速离心机 / 高速冷冻离心机','High-Speed Micro Centrifuge Series','AF-CF-HS-D1524','Centrifuge',[
'The D1524/D1524R high-speed centrifuge series is intended for temperature-sensitive sample processing in molecular biology and biochemistry laboratories.',
'Applications include DNA/RNA samples, PCR precipitates, protein precipitation, antibody separation, enzyme reactions, cell debris removal and bacterial or yeast fractionation.'
],['Electric lock design supports one-hand lid closing.','Refrigerated model can automatically start after pre-cooling.','Temperature setting range -20 C to 40 C on refrigerated model.','Stores up to 9 programs.','Five rotor options cover 0.2 mL to 5 mL and PCR tube formats.'],[
('Maximum speed','15000 rpm, 200-15000 rpm, step 10 rpm'),('Maximum RCF','21380 x g, step 10 x g'),('Capacity','36 x 0.2/0.5 mL; 24 x 1.5/2 mL; 4 x PCR 8-strips; 12 x 5 mL round-bottom; 18 x 5 mL round-bottom'),('Temperature range','D1524R: -20 C to 40 C'),('Timer','30 s to 99 h, HOLD continuous mode'),('Acceleration / deceleration time','25 s up / 25 s down'),('Motor type','Brushless DC motor'),('D1524 power','200-240 V 50/60 Hz 210 W; 100-120 V 50/60 Hz 200 W'),('D1524R power','100-120/200-240 V 50/60 Hz 500 W'),('D1524 noise','Less than or equal to 64 dB'),('D1524R noise','Less than or equal to 56 dB'),('D1524 dimensions','280 x 400 x 240 mm'),('D1524R dimensions','332 x 553 x 283 mm'),('D1524 weight','8.8 kg'),('D1524R weight','30 kg')],[('AF-CF-HS-D1524-01','D1524 unit','15000 rpm, 21380 x g'),('AF-CF-HS-D1524R-02','D1524R unit','15000 rpm, 21380 x g, -20 C to 40 C')])

add('DM0612 低速离心机','Low-Speed Centrifuge','AF-CF-LS-DM0612','Centrifuge',[
'The DM0612 low-speed centrifuge is designed for biology, medicine, chemistry and environmental laboratories, including serum, plasma, cell suspension, urine and sample separation before analysis.',
'The unit provides a large touch interface, rotor recognition, automatic lid opening after completion, multiple braking modes and imbalance protection.'
],['Large touch-screen interface for easy operation.','Maximum speed 6500 rpm.','Rotor identification improves efficiency when changing rotors.','Automatic lid opening after completion.','Supports 9 program presets.'],[
('Speed range','300-6500 rpm, step 1 rpm'),('Maximum RCF','4000 x g, step 1 x g'),('Speed accuracy','+/-20 rpm'),('Rotor capacity','60 mL x 6 angle rotor'),('Running time','30 s to 99 h 59 min 59 s / HOLD continuous operation'),('Display','LCD touch screen'),('Program storage','9 programs'),('Acceleration / deceleration','1 up / 3 down'),('Power','Single-phase 100-240 V, 50 Hz/60 Hz'),('Dimensions','408 x 315 x 220 mm'),('Weight','12 kg')],[('AF-CF-LS-DM0612-01','DM0612 unit','300-6500 rpm low-speed centrifuge')])

add('DM0436E 低速离心机','Low-Speed Centrifuge','AF-CF-LS-DM0436E','Centrifuge',[
'The DM0436E low-speed centrifuge is suitable for clinical chemistry, cytology, research laboratories and industrial laboratories.',
'It can be equipped with multiple rotors and adapters for blood collection tubes, urine collection tubes and microplates.'
],['Speed range 100-3500 rpm.','Compatible with multiple rotor capacities.','Supports relative centrifugal force and speed mode switching.','Six acceleration/deceleration levels.','LCD display shows operating parameters.'],[
('Speed range','100-3500 rpm, step 100 rpm'),('Maximum RCF','2260 x g'),('Speed accuracy','+/-20 rpm'),('Rotor capacity','12 x 10 mL internal; 12 x 15 mL external; 12 x 15 mL; 6 x 50 mL; 36 x 7 mL; 2 x 96-well microplates'),('Time setting range','30 s to 99 min 59 s, continuous operation'),('Display','LCD'),('Noise','Less than or equal to 55 dB'),('Acceleration / deceleration','6 up / 6 down'),('Power','100-240 V, 50/60 Hz, 170 W'),('Dimensions','481.5 x 414 x 253.5 mm'),('Weight','15 kg')],[('AF-CF-LS-DM0436E-01','DM0436E unit','100-3500 rpm low-speed centrifuge')])

add('DM0306 低速离心机','Low-Speed Centrifuge','AF-CF-LS-DM0306','Centrifuge',[
'The DM0306 low-speed centrifuge is a compact laboratory centrifuge for blood, blood cell, body-fluid and sample separation in clinical, biochemical and medical laboratories.',
'It is intended as a routine instrument for low-speed sample processing where small footprint and simple operation are important.'
],['Compact body saves bench space.','Maximum speed 3400 rpm and maximum RCF 1600 x g.','Rotor capacity 6 x 3-10 mL tubes.','Electronic timer supports 0.5-30 min and continuous operation.','LED display shows remaining running time.'],[
('Maximum speed','3400 rpm'),('Maximum RCF','1600 x g'),('Rotor capacity','6 x 3-10 mL tubes'),('Maximum acceleration time','Less than 10 s'),('Maximum deceleration time','Less than 20 s'),('Timer display','LED'),('Time setting range','0.5-30 min, continuous operation'),('Motor type','AC motor'),('Noise','Less than or equal to 63 dB'),('Power','80 W'),('Dimensions','359 x 318 x 222 mm'),('Weight','5.3 kg')],[('AF-CF-LS-DM0306-01','DM0306 unit','3400 rpm compact low-speed centrifuge')])
add('DM0412 低速离心机','Low-Speed Centrifuge','AF-CF-LS-DM0412','Centrifuge',[
'The DM0412 low-speed centrifuge is prepared for blood, plasma, cells, urine and routine laboratory sample separation in clinical and biochemical laboratories.',
'It supports touch-button control, LCD display, electronic door lock, instant spin and multiple rotor compatibility.'
],['LCD display and user-friendly interface.','Speed and RCF can be toggled for display.','Brushless DC motor is maintenance-free.','One-key instant spin.','Electronic door lock with automatic lid opening after completion.'],[
('Speed range','300-4500 rpm, step 100 rpm'),('Maximum RCF','2490 x g'),('Speed accuracy','+/-20 rpm'),('Rotor type','A12-10P or A6-50P, not interchangeable'),('Running time','30 s to 99 min; HOLD continuous operation'),('Motor type','Brushless DC motor'),('Display','LCD'),('Acceleration/deceleration','A12-10P: 20 s up / 13 s down; A6-50P: 20 s up / 90 s down'),('Power','100-240 V, 50/60 Hz, 3 A, 70 W'),('Dimensions','354 x 304 x 215 mm'),('Weight','6 kg')],[('AF-CF-LS-DM0412-01','DM0412 unit','300-4500 rpm low-speed centrifuge')])

add('DM0424&DM0408 低速离心机（临床）','Clinical Low-Speed Centrifuge Series','AF-CF-CLIN-DM04','Centrifuge',[
'The DM0424/DM0408 clinical low-speed centrifuge series is suitable for clinical, blood, whole-blood, serum, urine and biochemical analysis applications.',
'It provides LCD or LED control, program storage for common sample types, brushless DC motor operation and multiple rotor options.'
],['Compact structure with clear display control.','Speed and RCF can be switched for display.','Three stored programs are available for blood, urine and stool samples.','Maximum speed 4000 rpm.','Maximum capacity up to 4 x 50 mL.'],[
('DM0424 speed range','500-4000 rpm, step 100 rpm'),('DM0408 speed range','300-4000 rpm, step 100 rpm'),('DM0424 maximum RCF','2500 x g'),('DM0408 maximum RCF','1900 x g'),('Speed accuracy','+/-100 rpm'),('DM0424 rotor capacity','Swing rotor 6 x 15 mL; swing rotor 4 x 50 mL; angle rotor 24 x 15 mL; angle rotor 12 x 10 mL or 8 x 15 mL'),('DM0408 rotor capacity','Angle rotor 12 x 10 mL or 8 x 15 mL'),('Running time','1-99 min, continuous operation'),('DM0424 display','LCD'),('DM0408 display','LED'),('Program storage','Blood: 3200 rpm 10 min; urine: 1800 rpm 5 min; stool: 1300 rpm 10 min'),('DM0424 dimensions','364 x 440 x 268 mm'),('DM0408 dimensions','286 x 367 x 227 mm'),('DM0424 weight','14.5 kg'),('DM0408 weight','9.2 kg')],[('AF-CF-CLIN-DM0424-01','DM0424 unit','500-4000 rpm, 2500 x g'),('AF-CF-CLIN-DM0408-02','DM0408 unit','300-4000 rpm, 1900 x g')])

add('DM0506 低速离心机','Low-Speed Centrifuge','AF-CF-LS-DM0506','Centrifuge',[
'The DM0506 low-speed centrifuge is intended for medical, biochemical and laboratory applications including blood, serum, urine and sample separation.',
'It combines LCD parameter display, two program presets, adjustable acceleration and deceleration, and rotor options for 15 mL and 50 mL tubes.'
],['Speed range 300-5000 rpm.','Speed and RCF can be switched for display.','Two programs can be customized and recalled by P1/P2.','Acceleration and deceleration levels are adjustable.','Running end automatically opens the lid.'],[
('Speed range','300-5000 rpm, step 10 rpm'),('Maximum RCF','2600 x g, step 10 x g'),('Speed accuracy','+/-20 rpm'),('Rotor capacity','6 x 1.5/5/7/10/15 mL; 4 x 20/50 mL'),('Running time','30 s to 99 min, HOLD continuous operation'),('Display','LCD'),('Custom program storage','P1/P2'),('Acceleration/deceleration','1 up / 2 down'),('Power','100-240 V, 50/60 Hz, 70 W'),('Dimensions','300 x 240 x 180 mm'),('Weight','5.2 kg')],[('AF-CF-LS-DM0506-01','DM0506 unit','300-5000 rpm low-speed centrifuge')])

add('DM0636 低速离心机（多用途）','Multipurpose Low-Speed Centrifuge','AF-CF-LS-DM0636','Centrifuge',[
'The DM0636 multipurpose low-speed centrifuge is designed for clinical chemistry, cytology, research laboratories and industrial laboratories.',
'It supports multiple blood collection, urine collection and 100 mL standard test tube applications through rotors and adapters.'
],['Electric lock design allows one-hand lid closing.','Speed setting range 300-6000 rpm.','Maximum capacity 4 x 100 mL.','Nine acceleration and ten deceleration levels.','Rotor self-identification and instant spin functions.','Nine programs can be stored.'],[
('Speed range','300-6000 rpm, step 10 rpm'),('Maximum RCF','4100 x g'),('Speed accuracy','+/-20 rpm'),('Rotor capacity','4 x 100 mL'),('Running time','30 s to 99 min, continuous operation'),('Motor type','Brushless DC motor'),('Display','LCD'),('Custom program storage','9 programs'),('Acceleration/deceleration','9 up / 10 down'),('Power','660 W; AC220-240 V 50/60 Hz 6.3 A; AC110-120 V 50/60 Hz 10 A'),('Noise','Less than or equal to 65 dB'),('Dimensions','570 x 445 x 295 mm'),('Weight','36 kg')],[('AF-CF-LS-DM0636-01','DM0636 unit','300-6000 rpm, 4100 x g, 4 x 100 mL')])

accessories = [
('A4-PCR8P rotor','PCR Strip Rotor','AF-CF-ROT-A4PCR8P','For D1008/D1008E','7000 rpm max; 2680 x g; 32 x 0.2 mL PCR tubes or 4 x 0.2 mL PCR 8-strips'),
('A8-2P rotor','Microtube Rotor','AF-CF-ROT-A8-2P','For D1008/D1008E','7000 rpm max; 2680 x g; 8 x 0.2/0.5/1.5/2 mL'),
('SA02P2 adapter','0.2 mL Tube Adapter','AF-CF-ADP-SA02P2','For A8-2P rotor','8 pieces per pack'),
('SA05P2 adapter','0.5 mL Tube Adapter','AF-CF-ADP-SA05P2','For A8-2P rotor','8 pieces per pack'),
('A18-2P rotor','18-Place Microtube Rotor','AF-CF-ROT-A18-2P','For D2012S','15000 rpm max; 16750 x g; 18 x 0.2/0.5/1.5/2 mL'),
('A6-5VP rotor','6-Place Tube Rotor','AF-CF-ROT-A6-5VP','For D2012S','15000 rpm max; 16520 x g; 6 x 0.5 mL plus adapters'),
('A4-PCR8 rotor','PCR Strip Rotor','AF-CF-ROT-A4PCR8','For D2012S','15000 rpm max; 4 x 0.2 mL PCR 8-strips'),
('A12-2P rotor','12-Place Microtube Rotor','AF-CF-ROT-A12-2P','For D2012 Plus','15000 rpm max; 15100 x g; 12 x 0.2/0.5/1.5/2 mL'),
('A02P2 adapter','0.2 mL Tube Adapter','AF-CF-ADP-A02P2','For A12-2P, AS24-2 and A24-2P rotors','24 pieces per pack'),
('A05P2 adapter','0.5 mL Tube Adapter','AF-CF-ADP-A05P2','For A12-2P, AS24-2 and A24-2P rotors','24 pieces per pack'),
('AH6-15P rotor','6-Place 15 mL Rotor','AF-CF-ROT-AH6-15P','For DM0612','6500 rpm max; 4333 x g; 6 x 15 mL'),
('A12-10P rotor','12-Place 10 mL Rotor','AF-CF-ROT-A12-10P','For DM0612 and DM0412','4500 rpm max; 2490 x g; 12 x 10 mL'),
('AE6-50 rotor','6-Place 50 mL Rotor','AF-CF-ROT-AE6-50','For DM0612','4000 rpm max; 1968 x g; 6 x 50 mL'),
('A5P17 adapter','5 mL Tube Adapter','AF-CF-ADP-A5P17','For AH6-15P and A12-10P rotors','Fits 13 x 75 mm collection tubes'),
('A2P17 adapter','1.5/2 mL Tube Adapter','AF-CF-ADP-A2P17','For AH6-15P and A12-10P rotors','Fits 11 x 43 mm conical tubes and 1.5/2 mL microtubes'),
('SE6-10P rotor','6-Place Clinical Rotor','AF-CF-ROT-SE6-10P','For DM0306','4000 rpm max; 1600 x g; 6 x 10 mL'),
('A6-15P rotor','6-Place 15 mL Rotor','AF-CF-ROT-A6-15P','For DM0506','5000 rpm max; 2600 x g; 6 x 15 mL'),
('A4-50P rotor','4-Place 50 mL Rotor','AF-CF-ROT-A4-50P','For DM0506','5000 rpm max; 2600 x g; 4 x 50 mL'),
('DM0436E rotor set','Rotor Set for DM0436E','AF-CF-ROT-DM0436E-SET','For DM0436E','Supports 12 x 10 mL, 12 x 15 mL, 6 x 50 mL, 36 x 7 mL and 2 x 96-well plate configurations'),
('DM0424/DM0408 rotor set','Rotor Set for Clinical Low-Speed Series','AF-CF-ROT-DM04-SET','For DM0424 and DM0408','Includes compatible swing and angle rotor options for blood tubes, urine tubes and 50 mL tubes')]
for cn,en,model,compat,spec in accessories:
    add(cn,en,model,'Accessory',[f'The {en} is an Atomfair centrifuge accessory prepared for compatible centrifuge configurations.',f'It is listed as a standalone accessory because rotor, adapter and tube compatibility directly affect ordering, sample capacity and application matching.'],['Standalone accessory record with unique Atomfair model.','Compatibility is retained from the source manual.','Specification and tube capacity information is preserved for ordering.'],[('Accessory type',en),('Compatibility',compat),('Specification',spec)],[(model,cn,spec)])
def make_html(x):
    return f'''<!-- Atomfair Complete Product HTML - Centrifuge and Accessories Full-English Release -->
<div style="width:100%;background:#ffffff;padding:0;" align="center"><table style="width:100%;font-family:Arial,Helvetica,sans-serif;color:#333;line-height:1.58;background:#fff;" border="0" width="100%" cellspacing="0" cellpadding="0"><tbody>
<tr><td style="padding:38px 20px;border-bottom:4px solid #111;"><h1 style="margin:0;font-size:26px;color:#111;font-weight:800;text-transform:uppercase;">ATOMFAIR&reg; {esc(x['en'])}</h1><div style="margin-top:8px;font-size:14px;color:#333;">Product Type: {esc(x['kind'])}</div><div class="model" style="margin-top:10px;font-size:15px;color:#333;font-weight:700;">Atomfair Model: {esc(x['model'])}</div><div style="margin-top:15px;display:inline-block;background:#111;color:#fff;padding:6px 15px;font-size:13px;font-weight:bold;letter-spacing:.6px;text-transform:uppercase;">Research-grade centrifuge platform</div></td></tr>
<tr><td style="padding:38px 20px;"><table style="margin-bottom:34px;" border="0" width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td style="border-left:5px solid #111;padding-left:15px;padding-bottom:12px;"><h2 style="margin:0;font-size:18px;color:#111;text-transform:uppercase;font-weight:800;">Product Overview</h2></td></tr><tr><td style="padding-top:18px;">{ptxt(x['overview'])}</td></tr></tbody></table>
<table style="margin-bottom:34px;" border="0" width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td style="border-left:5px solid #111;padding-left:15px;padding-bottom:12px;"><h2 style="margin:0;font-size:18px;color:#111;text-transform:uppercase;font-weight:800;">Key Features and Advantages</h2></td></tr><tr><td><ul style="margin:18px 0 0 0;padding-left:22px;font-size:14px;color:#444;line-height:1.85;">{li(x['features'])}</ul></td></tr></tbody></table>
<table style="margin-bottom:34px;" border="0" width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td style="border-left:5px solid #111;padding-left:15px;padding-bottom:12px;"><h2 style="margin:0;font-size:18px;color:#111;text-transform:uppercase;font-weight:800;">Technical Specifications</h2></td></tr><tr><td><table style="border-collapse:collapse;border:1px solid #111;font-size:14px;" border="0" width="100%" cellspacing="0" cellpadding="0"><thead><tr><th style="background:#111;color:#fff;border:1px solid #111;padding:11px 12px;text-align:left;">Parameter</th><th style="background:#111;color:#fff;border:1px solid #111;padding:11px 12px;text-align:left;">Specification / Available Values</th></tr></thead><tbody>{tr(x['specs'])}</tbody></table></td></tr></tbody></table>
<table style="margin-bottom:34px;" border="0" width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td style="border-left:5px solid #111;padding-left:15px;padding-bottom:12px;"><h2 style="margin:0;font-size:18px;color:#111;text-transform:uppercase;font-weight:800;">Atomfair Product Ordering and Configuration Table</h2></td></tr><tr><td><table style="border-collapse:collapse;border:1px solid #111;font-size:14px;" border="0" width="100%" cellspacing="0" cellpadding="0"><thead><tr><th style="background:#111;color:#fff;border:1px solid #111;padding:11px 12px;text-align:left;">Unique Atomfair Order Model</th><th style="background:#111;color:#fff;border:1px solid #111;padding:11px 12px;text-align:left;">Source Item / Component</th><th style="background:#111;color:#fff;border:1px solid #111;padding:11px 12px;text-align:left;">Specification Value</th></tr></thead><tbody>{otr(x['orders'])}</tbody></table></td></tr></tbody></table>
<table style="background:#f7f7f7;border:1px solid #e0e0e0;margin-bottom:34px;" border="0" width="100%" cellspacing="0" cellpadding="22"><tbody><tr><td style="font-size:14px;color:#333;"><div style="margin-bottom:10px;"><strong>Data Handling Standard:</strong> HTML content is English only. Technical parameters, dimensions, speed ranges, rotor capacities, accessory compatibility, power and model-specific values are preserved in structured tables.</div><div><strong>Ordering Standard:</strong> Each centrifuge, rotor, adapter or accessory receives a unique Atomfair order model.</div></td></tr></tbody></table></td></tr>
<tr><td style="padding:25px 20px;background:#111;text-align:center;"><div style="color:#fff;font-size:20px;font-weight:bold;margin-bottom:8px;letter-spacing:1px;">TAILORED SOLUTIONS FOR RESEARCH</div><div style="color:#ddd;font-size:13px;margin-bottom:18px;">For bulk orders, OEM requirements, rotor matching, adapter selection or configuration confirmation, contact our engineering sales team.</div><div style="display:inline-block;background:#fff;color:#111;padding:12px 35px;font-weight:800;font-size:13px;text-transform:uppercase;letter-spacing:1px;border-radius:2px;">EMAIL: inquiry@atomfair.com</div></td></tr>
<tr><td style="padding:28px 20px;text-align:center;font-size:12px;color:#888;letter-spacing:1px;"><div style="margin-bottom:5px;text-transform:uppercase;"><strong>Supplier:</strong> Atomfair</div><div style="text-transform:uppercase;"><strong>Brand:</strong> ATOMFAIR&reg;</div></td></tr></tbody></table></div>'''

records=[]
for x in items:
    code = make_html(x)
    if re.search(r'[\u4e00-\u9fff]', code):
        raise SystemExit('Chinese character found in HTML for '+x['cn'])
    (OUT/(slug(x['model'])+'.html')).write_text(code, encoding='utf-8')
    records.append({'来源':'','商品中文名称':x['cn'],'型号':x['model'],'产品名称（英文）':'ATOMFAIR® '+x['en'],'URL':'','简介':' '.join(x['overview']),'产品详情':'','代码':code,'网站分类':'','主图':'','详情图':'','图片文件名':'','alt text':'','title':'','Caption':'','价格':'','💲':'','是否上传':''})
payload=[{'sheetName':'离心系列全部产品','folder':str(OUT),'records':records}]
JSON_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'records':len(records),'html_dir':str(OUT),'json':str(JSON_OUT)}, ensure_ascii=False))
