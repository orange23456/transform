from pathlib import Path
from PIL import Image
root=Path(r'C:\Users\hz-user\Desktop\全自动')
sets=[('mixer_shaker_source_images', list(range(3,31))), ('electrophoresis_source_images', list(range(1,12)))]
for folder, nums in sets:
    out=root/(folder+'_crops')
    out.mkdir(exist_ok=True)
    for n in nums:
        p=root/folder/f'image{n}.png'
        if not p.exists(): continue
        im=Image.open(p).convert('RGB')
        w,h=im.size
        crops={
            'full2x': (0,0,w,h),
            'bottom2x': (0,int(h*0.45),w,h),
            'right2x': (int(w*0.45),0,w,h),
            'left2x': (0,0,int(w*0.58),h),
        }
        for name,box in crops.items():
            c=im.crop(box)
            c=c.resize((c.width*2,c.height*2))
            c.save(out/f'image{n}_{name}.png')
print('done')
