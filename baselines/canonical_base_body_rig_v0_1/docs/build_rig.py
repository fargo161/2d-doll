from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

PROJECT = Path('/mnt/data/canonical_base_body_rig_v0_1')
CANVAS_W, CANVAS_H = 1000, 1700
AA = 3
SKIN = np.array([218, 164, 136], dtype=np.float32)

PART_IDS = [
    'calf_L', 'calf_R', 'foot_L', 'foot_R',
    'thigh_L', 'thigh_R',
    'forearm_L', 'forearm_R', 'upper_arm_L', 'upper_arm_R',
    'hand_L', 'hand_R',
    'pelvis', 'mid_torso', 'chest'
]

TREE = {
    'pelvis': 'root',
    'mid_torso': 'pelvis',
    'chest': 'mid_torso',
    'upper_arm_L': 'chest',
    'forearm_L': 'upper_arm_L',
    'hand_L': 'forearm_L',
    'upper_arm_R': 'chest',
    'forearm_R': 'upper_arm_R',
    'hand_R': 'forearm_R',
    'thigh_L': 'pelvis',
    'calf_L': 'thigh_L',
    'foot_L': 'calf_L',
    'thigh_R': 'pelvis',
    'calf_R': 'thigh_R',
    'foot_R': 'calf_R',
}

JOINT_FOR_PART = {
    'pelvis': 'pelvis',
    'mid_torso': 'waist',
    'chest': 'chest',
    'upper_arm_L': 'shoulder_L',
    'forearm_L': 'elbow_L',
    'hand_L': 'wrist_L',
    'upper_arm_R': 'shoulder_R',
    'forearm_R': 'elbow_R',
    'hand_R': 'wrist_R',
    'thigh_L': 'hip_L',
    'calf_L': 'knee_L',
    'foot_L': 'ankle_L',
    'thigh_R': 'hip_R',
    'calf_R': 'knee_R',
    'foot_R': 'ankle_R',
}

LIMITS = {
    'pelvis': [-18, 18],
    'mid_torso': [-14, 14],
    'chest': [-12, 12],
    'upper_arm_L': [-65, 65],
    'forearm_L': [-12, 112],
    'hand_L': [-35, 35],
    'upper_arm_R': [-65, 65],
    'forearm_R': [-112, 12],
    'hand_R': [-35, 35],
    'thigh_L': [-38, 38],
    'calf_L': [-8, 98],
    'foot_L': [-28, 28],
    'thigh_R': [-38, 38],
    'calf_R': [-98, 8],
    'foot_R': [-28, 28],
}

COLORS = {
    'pelvis': '#ff5a78', 'mid_torso': '#f2ad4d', 'chest': '#ffd966',
    'upper_arm_L': '#5ec8ff', 'forearm_L': '#3f9ce8', 'hand_L': '#2a79c7',
    'upper_arm_R': '#a57cff', 'forearm_R': '#8159df', 'hand_R': '#6640c2',
    'thigh_L': '#70de8c', 'calf_L': '#42bd6a', 'foot_L': '#24944c',
    'thigh_R': '#ff9b65', 'calf_R': '#e66f3f', 'foot_R': '#c84f2a',
}

@dataclass
class ViewDef:
    id: str
    label: str
    pivots: Dict[str, Tuple[float, float]]
    near_side: str
    z: Dict[str, int]
    facing: str


def cubic(p0, p1, p2, p3, n=30):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
        y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
        out.append((x, y))
    return out


def quad_centerline(p0, pc, p1, n=72):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = u*u*p0[0] + 2*u*t*pc[0] + t*t*p1[0]
        y = u*u*p0[1] + 2*u*t*pc[1] + t*t*p1[1]
        pts.append(np.array([x, y], dtype=float))
    return pts


def limb_polygon(p0, p1, r0, r1, bulge=0.12, curve=(0,0), overlap0=34, overlap1=34, n=72):
    p0=np.array(p0,dtype=float); p1=np.array(p1,dtype=float)
    vec=p1-p0; length=np.linalg.norm(vec); unit=vec/length
    p0e=p0-unit*overlap0; p1e=p1+unit*overlap1
    mid=(p0e+p1e)/2+np.array(curve,dtype=float)
    center=quad_centerline(p0e,mid,p1e,n)
    left=[]; right=[]
    for i,c in enumerate(center):
        t=i/n
        if i==0: tangent=center[1]-center[0]
        elif i==n: tangent=center[-1]-center[-2]
        else: tangent=center[i+1]-center[i-1]
        tangent=tangent/(np.linalg.norm(tangent)+1e-6)
        perp=np.array([-tangent[1],tangent[0]])
        base=r0*(1-t)+r1*t
        muscle=1+bulge*math.sin(math.pi*t)
        width=base*muscle
        left.append(tuple(c+perp*width))
        right.append(tuple(c-perp*width))
    return left+right[::-1]


def hand_polygon(wrist, end, width=34, side='L', overlap=26):
    wrist=np.array(wrist,float); end=np.array(end,float)
    v=end-wrist; length=np.linalg.norm(v); u=v/(length+1e-6); p=np.array([-u[1],u[0]])
    start=wrist-u*overlap
    pts=[
        start+p*width*0.65,
        wrist+p*width*0.82,
        wrist+u*length*0.38+p*width,
        end+p*width*0.48,
        end+u*10,
        end-p*width*0.50,
        wrist+u*length*0.42-p*width*0.92,
        wrist-p*width*0.75,
        start-p*width*0.60,
    ]
    return [tuple(x) for x in pts]


def foot_polygon(ankle, toe, width=38, overlap=28, heel_drop=22):
    ankle=np.array(ankle,float); toe=np.array(toe,float)
    v=toe-ankle; length=np.linalg.norm(v); u=v/(length+1e-6); p=np.array([-u[1],u[0]])
    start=ankle-u*overlap
    heel=ankle-u*8+np.array([0,heel_drop])
    pts=[
        tuple(start+p*width*0.65),
        tuple(ankle+p*width*0.86),
        tuple(toe+p*width*0.50),
        tuple(toe+u*16),
        tuple(toe-p*width*0.50),
        tuple(heel-p*width*0.70),
        tuple(start-p*width*0.58),
    ]
    return pts


def make_mask(polygons: List[List[Tuple[float,float]]], ellipses=None):
    W,H=CANVAS_W*AA,CANVAS_H*AA
    im=Image.new('L',(W,H),0)
    d=ImageDraw.Draw(im)
    for poly in polygons:
        d.polygon([(int(x*AA),int(y*AA)) for x,y in poly],fill=255)
    for box in ellipses or []:
        d.ellipse(tuple(int(v*AA) for v in box),fill=255)
    return im.resize((CANVAS_W,CANVAS_H),Image.Resampling.LANCZOS)


def torso_masks(view: ViewDef):
    p=view.pivots
    out={}
    if view.id=='front':
        chest_left = cubic((470,142),(448,190),(405,220),(345,260),22)
        chest_left += cubic((345,260),(330,315),(365,405),(420,495),28)
        chest_right = cubic((580,495),(635,405),(670,315),(655,260),28)
        chest_right += cubic((655,260),(595,220),(552,190),(530,142),22)
        chest=[(470,142)]+chest_left[1:]+[(580,495)]+chest_right[1:]+[(530,142)]
        mid_left=cubic((418,430),(398,500),(410,575),(440,645),28)
        mid_right=cubic((560,645),(590,575),(602,500),(582,430),28)
        mid=[(418,430)]+mid_left[1:]+[(560,645)]+mid_right[1:]
        pelvis_left=cubic((430,565),(392,610),(382,700),(405,790),28)
        pelvis_left+=cubic((405,790),(430,825),(462,822),(490,804),18)
        pelvis_right=cubic((510,804),(538,822),(570,825),(595,790),18)
        pelvis_right+=cubic((595,790),(618,700),(608,610),(570,565),28)
        pelvis=[(430,565)]+pelvis_left[1:]+[(510,804)]+pelvis_right[1:]
    elif view.id=='three_quarter':
        chest_left=cubic((486,142),(455,180),(410,220),(390,270),22)
        chest_left+=cubic((390,270),(380,340),(405,430),(445,505),28)
        chest_right=cubic((570,505),(610,430),(635,330),(615,275),28)
        chest_right+=cubic((615,275),(585,225),(552,185),(535,142),22)
        chest=[(486,142)]+chest_left[1:]+[(570,505)]+chest_right[1:]+[(535,142)]
        mid_left=cubic((444,430),(425,500),(438,580),(463,650),28)
        mid_right=cubic((555,650),(590,580),(597,505),(570,430),28)
        mid=[(444,430)]+mid_left[1:]+[(555,650)]+mid_right[1:]
        pelvis_left=cubic((455,565),(420,625),(420,715),(445,800),28)
        pelvis_left+=cubic((445,800),(470,825),(500,817),(520,802),18)
        pelvis_right=cubic((540,802),(568,818),(592,815),(610,785),18)
        pelvis_right+=cubic((610,785),(625,690),(607,610),(575,565),28)
        pelvis=[(455,565)]+pelvis_left[1:]+[(540,802)]+pelvis_right[1:]
    else: # back
        chest_left=cubic((470,142),(445,188),(402,220),(348,262),22)
        chest_left+=cubic((348,262),(335,330),(368,415),(420,500),28)
        chest_right=cubic((580,500),(632,415),(665,330),(652,262),28)
        chest_right+=cubic((652,262),(598,220),(555,188),(530,142),22)
        chest=[(470,142)]+chest_left[1:]+[(580,500)]+chest_right[1:]+[(530,142)]
        mid_left=cubic((420,430),(402,505),(415,582),(443,645),28)
        mid_right=cubic((557,645),(585,582),(598,505),(580,430),28)
        mid=[(420,430)]+mid_left[1:]+[(557,645)]+mid_right[1:]
        pelvis_left=cubic((432,565),(398,620),(388,705),(410,795),28)
        pelvis_left+=cubic((410,795),(438,830),(470,826),(498,805),18)
        pelvis_right=cubic((502,805),(530,826),(562,830),(590,795),18)
        pelvis_right+=cubic((590,795),(612,705),(602,620),(568,565),28)
        pelvis=[(432,565)]+pelvis_left[1:]+[(502,805)]+pelvis_right[1:]
    out['chest']=make_mask([chest])
    out['mid_torso']=make_mask([mid])
    out['pelvis']=make_mask([pelvis])
    return out


def build_view_defs():
    front_p={
        'root':(500,690),'pelvis':(500,690),'waist':(500,575),'chest':(500,450),'neck_socket':(500,150),
        'shoulder_L':(655,280),'elbow_L':(702,565),'wrist_L':(718,810),
        'shoulder_R':(345,280),'elbow_R':(298,565),'wrist_R':(282,810),
        'hip_L':(570,705),'knee_L':(592,1115),'ankle_L':(605,1480),
        'hip_R':(430,705),'knee_R':(408,1115),'ankle_R':(395,1480),
    }
    tq_p={
        'root':(515,695),'pelvis':(515,695),'waist':(510,575),'chest':(510,450),'neck_socket':(510,150),
        'shoulder_L':(600,292),'elbow_L':(650,562),'wrist_L':(666,805), # far side
        'shoulder_R':(405,282),'elbow_R':(345,565),'wrist_R':(325,810), # near side
        'hip_L':(570,710),'knee_L':(606,1110),'ankle_L':(620,1475),
        'hip_R':(445,705),'knee_R':(420,1118),'ankle_R':(410,1484),
    }
    back_p={
        'root':(500,690),'pelvis':(500,690),'waist':(500,575),'chest':(500,450),'neck_socket':(500,150),
        'shoulder_L':(345,280),'elbow_L':(298,565),'wrist_L':(282,810),
        'shoulder_R':(655,280),'elbow_R':(702,565),'wrist_R':(718,810),
        'hip_L':(430,705),'knee_L':(408,1115),'ankle_L':(395,1480),
        'hip_R':(570,705),'knee_R':(592,1115),'ankle_R':(605,1480),
    }
    front_z={p:i*10 for i,p in enumerate(PART_IDS)}
    # More intentional layering
    front_z.update({'calf_L':10,'calf_R':10,'foot_L':20,'foot_R':20,'thigh_L':30,'thigh_R':30,
                    'forearm_L':20,'forearm_R':20,'upper_arm_L':35,'upper_arm_R':35,
                    'hand_L':45,'hand_R':45,'pelvis':50,'mid_torso':60,'chest':70})
    tq_z={
        'calf_L':8,'foot_L':9,'thigh_L':10,'forearm_L':12,'upper_arm_L':14,'hand_L':16,
        'pelvis':40,'mid_torso':50,'chest':60,
        'calf_R':65,'foot_R':67,'thigh_R':70,'upper_arm_R':74,'forearm_R':76,'hand_R':78,
    }
    back_z=front_z.copy()
    return [
        ViewDef('front','Front',front_p,'symmetric',front_z,'forward'),
        ViewDef('three_quarter','3/4 Side',tq_p,'R',tq_z,'stage-right'),
        ViewDef('back','Back',back_p,'symmetric',back_z,'backward'),
    ]


def create_part_masks(view: ViewDef):
    p=view.pivots
    masks=torso_masks(view)
    # Side-specific scale for 3/4 depth.
    if view.id=='three_quarter':
        side_scale={'L':0.83,'R':1.12}
    else:
        side_scale={'L':1.0,'R':1.0}
    for side in ['L','R']:
        s=side_scale[side]
        sh=p[f'shoulder_{side}']; el=p[f'elbow_{side}']; wr=p[f'wrist_{side}']
        # Curves point slightly away from torso.
        dir_sign=1 if el[0]>sh[0] else -1
        ua=limb_polygon(sh,el,54*s,43*s,bulge=0.16,curve=(dir_sign*10,0),overlap0=24,overlap1=26)
        fa=limb_polygon(el,wr,44*s,31*s,bulge=0.18,curve=(dir_sign*6,0),overlap0=25,overlap1=20)
        hand_end=(wr[0]+dir_sign*8,wr[1]+96)
        hand=hand_polygon(wr,hand_end,31*s,side,overlap=29)
        masks[f'upper_arm_{side}']=make_mask([ua],ellipses=[(sh[0]-56*s,sh[1]-56*s,sh[0]+56*s,sh[1]+56*s),(el[0]-44*s,el[1]-44*s,el[0]+44*s,el[1]+44*s)])
        masks[f'forearm_{side}']=make_mask([fa],ellipses=[(el[0]-43*s,el[1]-43*s,el[0]+43*s,el[1]+43*s),(wr[0]-32*s,wr[1]-32*s,wr[0]+32*s,wr[1]+32*s)])
        masks[f'hand_{side}']=make_mask([hand],ellipses=[(wr[0]-30*s,wr[1]-30*s,wr[0]+30*s,wr[1]+30*s),(hand_end[0]-25*s,hand_end[1]-22*s,hand_end[0]+25*s,hand_end[1]+22*s)])

        hip=p[f'hip_{side}']; knee=p[f'knee_{side}']; ankle=p[f'ankle_{side}']
        leg_dir=1 if knee[0]>hip[0] else -1
        thigh=limb_polygon(hip,knee,72*s,55*s,bulge=0.20,curve=(leg_dir*7,0),overlap0=34,overlap1=30)
        calf=limb_polygon(knee,ankle,57*s,35*s,bulge=0.35,curve=(leg_dir*6,0),overlap0=30,overlap1=20)
        toe=(ankle[0]+(58 if side=='L' else -58),ankle[1]+75)
        if view.id=='back':
            toe=(ankle[0]+(-58 if side=='L' else 58),ankle[1]+75)
        if view.id=='three_quarter':
            toe=(ankle[0]+(68 if side=='L' else -52),ankle[1]+72)
        foot=foot_polygon(ankle,toe,36*s,overlap=32,heel_drop=22)
        masks[f'thigh_{side}']=make_mask([thigh],ellipses=[(hip[0]-72*s,hip[1]-72*s,hip[0]+72*s,hip[1]+72*s),(knee[0]-56*s,knee[1]-56*s,knee[0]+56*s,knee[1]+56*s)])
        masks[f'calf_{side}']=make_mask([calf],ellipses=[(knee[0]-55*s,knee[1]-55*s,knee[0]+55*s,knee[1]+55*s),(ankle[0]-36*s,ankle[1]-36*s,ankle[0]+36*s,ankle[1]+36*s)])
        masks[f'foot_{side}']=make_mask([foot],ellipses=[(ankle[0]-34*s,ankle[1]-34*s,ankle[0]+34*s,ankle[1]+34*s),(toe[0]-20*s,toe[1]-18*s,toe[0]+20*s,toe[1]+18*s)])
    return masks


def skin_rgba(mask: Image.Image, view: ViewDef, part_id: str):
    m=np.array(mask).astype(np.float32)/255.0
    yy,xx=np.mgrid[0:CANVAS_H,0:CANVAS_W]
    if view.id=='front':
        center=500
        light=1.08-0.00022*np.abs(xx-center)
        light+=0.035*np.cos((yy/CANVAS_H)*math.pi)
    elif view.id=='three_quarter':
        light=1.02+0.00020*(500-xx)
        light+=0.025*np.cos((yy/CANVAS_H)*math.pi)
    else:
        light=1.02-0.00012*np.abs(xx-480)
        light+=0.025*np.cos((yy/CANVAS_H)*math.pi)
    dist=ndimage.distance_transform_edt(m>0.3)
    edge=np.clip(dist/18.0,0,1)
    light*=0.97+0.03*edge
    # subtle part-dependent shading
    if 'L' in part_id and view.id=='three_quarter': light*=0.94
    if 'R' in part_id and view.id=='three_quarter': light*=1.03
    rgb=np.zeros((CANVAS_H,CANVAS_W,3),dtype=np.float32)
    for c in range(3): rgb[:,:,c]=SKIN[c]*light
    # slight warm vertical gradient
    rgb[:,:,0]+=4*(1-yy/CANVAS_H)
    rgb=np.clip(rgb,0,255).astype(np.uint8)
    a=(m*255).astype(np.uint8)
    rgba=np.dstack([rgb,a])
    im=Image.fromarray(rgba,'RGBA')
    return im


def add_anatomy(im: Image.Image, mask: Image.Image, view: ViewDef, part_id: str):
    overlay=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(overlay)
    p=view.pivots
    line=(105,66,54,65); light=(255,235,220,45)
    if part_id=='chest':
        if view.id=='front':
            d.arc((410,230,500,390),210,330,fill=line,width=4)
            d.arc((500,230,590,390),210,330,fill=line,width=4)
            d.line((500,250,500,455),fill=(116,73,58,45),width=3)
            d.arc((430,178,570,300),200,340,fill=light,width=4)
        elif view.id=='three_quarter':
            d.arc((420,225,535,390),210,335,fill=line,width=4)
            d.arc((505,235,605,390),205,325,fill=(100,62,50,48),width=3)
            d.line((520,250,505,455),fill=(116,73,58,40),width=3)
        else:
            d.arc((405,250,495,380),200,325,fill=line,width=4)
            d.arc((505,250,595,380),215,340,fill=line,width=4)
            d.line((500,190,500,485),fill=(105,66,54,50),width=3)
    elif part_id=='mid_torso':
        if view.id!='back':
            d.line((500,460,500,635),fill=(120,76,62,35),width=3)
            d.ellipse((492,570,508,582),fill=(110,68,55,70))
        else:
            d.line((500,455,500,635),fill=(100,62,50,40),width=3)
            d.arc((440,500,560,640),205,335,fill=(255,235,220,35),width=3)
    elif part_id=='pelvis':
        if view.id=='front':
            d.arc((400,610,500,790),250,355,fill=(110,68,55,32),width=3)
            d.arc((500,610,600,790),185,290,fill=(110,68,55,32),width=3)
        elif view.id=='back':
            d.arc((398,650,505,815),210,355,fill=(100,60,48,50),width=4)
            d.arc((495,650,602,815),185,330,fill=(100,60,48,50),width=4)
            d.line((500,705,500,805),fill=(100,60,48,38),width=3)
        else:
            d.arc((425,640,535,810),220,355,fill=(100,60,48,40),width=3)
            d.arc((500,640,615,805),185,320,fill=(100,60,48,36),width=3)
    # Clip overlay to part mask.
    clipped=Image.new('RGBA',im.size,(0,0,0,0))
    clipped=Image.composite(overlay,clipped,mask)
    return Image.alpha_composite(im,clipped)


def alpha_outline(mask: Image.Image, color, width=3):
    m=np.array(mask)>64
    dil=ndimage.binary_dilation(m,iterations=width)
    ero=ndimage.binary_erosion(m,iterations=1)
    edge=(dil^ero).astype(np.uint8)*255
    out=Image.new('RGBA',mask.size,(0,0,0,0))
    rgba=np.zeros((CANVAS_H,CANVAS_W,4),dtype=np.uint8)
    rgb=tuple(int(color.lstrip('#')[i:i+2],16) for i in (0,2,4))
    rgba[:,:,0]=rgb[0]; rgba[:,:,1]=rgb[1]; rgba[:,:,2]=rgb[2]; rgba[:,:,3]=edge
    return Image.fromarray(rgba,'RGBA')


def save_part_assets(view: ViewDef, masks, manifest_view):
    aligned_dir=PROJECT/'assets'/view.id/'aligned'
    cropped_dir=PROJECT/'assets'/view.id/'cropped'
    mask_dir=PROJECT/'assets'/view.id/'masks'
    outline_dir=PROJECT/'assets'/view.id/'outlines'
    for d in [aligned_dir,cropped_dir,mask_dir,outline_dir]: d.mkdir(parents=True,exist_ok=True)
    for part_id,mask in masks.items():
        im=skin_rgba(mask,view,part_id)
        im=add_anatomy(im,mask,view,part_id)
        im.save(aligned_dir/f'{part_id}.png')
        mask.save(mask_dir/f'{part_id}.png')
        alpha_outline(mask,COLORS.get(part_id,'#ffffff'),2).save(outline_dir/f'{part_id}.png')
        bbox=mask.getbbox()
        pad=55
        if bbox:
            x0=max(0,bbox[0]-pad); y0=max(0,bbox[1]-pad); x1=min(CANVAS_W,bbox[2]+pad); y1=min(CANVAS_H,bbox[3]+pad)
        else: x0=y0=0; x1=y1=1
        crop=im.crop((x0,y0,x1,y1)); crop.save(cropped_dir/f'{part_id}.png')
        joint_id=JOINT_FOR_PART[part_id]
        pivot=view.pivots[joint_id]
        manifest_view['parts'][part_id]={
            'assetAligned':f'assets/{view.id}/aligned/{part_id}.png',
            'assetCropped':f'assets/{view.id}/cropped/{part_id}.png',
            'mask':f'assets/{view.id}/masks/{part_id}.png',
            'outline':f'assets/{view.id}/outlines/{part_id}.png',
            'parent':TREE[part_id],
            'pivotId':joint_id,
            'pivot':[round(pivot[0],2),round(pivot[1],2)],
            'crop':[x0,y0,x1-x0,y1-y0],
            'pivotInCrop':[round(pivot[0]-x0,2),round(pivot[1]-y0,2)],
            'zIndex':view.z[part_id],
            'rotationLimitsDeg':LIMITS[part_id],
            'defaultRotationDeg':0,
        }


def neutral_composite(view: ViewDef, masks, use_outlines=False, diagnostic=False):
    canvas=Image.new('RGBA',(CANVAS_W,CANVAS_H),(0,0,0,0))
    ordered=sorted(masks.keys(),key=lambda p:view.z[p])
    for part in ordered:
        im=Image.open(PROJECT/f'assets/{view.id}/aligned/{part}.png').convert('RGBA')
        canvas=Image.alpha_composite(canvas,im)
        if use_outlines:
            ol=Image.open(PROJECT/f'assets/{view.id}/outlines/{part}.png').convert('RGBA')
            canvas=Image.alpha_composite(canvas,ol)
    if diagnostic:
        d=ImageDraw.Draw(canvas)
        font=ImageFont.load_default()
        for jid,(x,y) in view.pivots.items():
            if jid=='root': col=(255,70,100,255)
            elif jid in ('waist','chest','pelvis'): col=(255,205,80,255)
            elif 'shoulder' in jid or 'elbow' in jid or 'wrist' in jid: col=(80,200,255,255)
            elif 'hip' in jid or 'knee' in jid or 'ankle' in jid: col=(90,240,130,255)
            else: col=(255,255,255,255)
            r=8
            d.ellipse((x-r,y-r,x+r,y+r),fill=col,outline=(25,25,25,255),width=2)
            d.text((x+11,y-7),jid,fill=(25,25,25,240),font=font,stroke_width=2,stroke_fill=(255,255,255,220))
    return canvas


def mat_mul(A,B): return A@B

def T(x,y): return np.array([[1,0,x],[0,1,y],[0,0,1]],dtype=float)

def R(deg):
    a=math.radians(deg); c=math.cos(a); s=math.sin(a)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]],dtype=float)

def around(pivot,deg): return T(*pivot)@R(deg)@T(-pivot[0],-pivot[1])


def posed_composite(view: ViewDef, angles: Dict[str,float], show_pivots=False):
    images={p:Image.open(PROJECT/f'assets/{view.id}/aligned/{p}.png').convert('RGBA') for p in PART_IDS}
    M={'root':np.eye(3)}
    def compute(node):
        if node in M: return M[node]
        par=TREE[node]
        Mp=compute(par)
        pivot=view.pivots[JOINT_FOR_PART[node]]
        M[node]=Mp@around(pivot,angles.get(node,0))
        return M[node]
    canvas=np.zeros((CANVAS_H,CANVAS_W,4),dtype=np.uint8)
    for part in sorted(PART_IDS,key=lambda p:view.z[p]):
        m=compute(part)
        # cv2 affine expects mapping source->dest in first 2 rows
        arr=np.array(images[part])
        warped=cv2.warpAffine(arr,m[:2,:],(CANVAS_W,CANVAS_H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
        src=warped.astype(np.float32)/255.0; dst=canvas.astype(np.float32)/255.0
        a=src[:,:,3:4]
        out_rgb=src[:,:,:3]*a+dst[:,:,:3]*(1-a)
        out_a=a+dst[:,:,3:4]*(1-a)
        canvas=np.dstack([out_rgb,out_a]); canvas=(np.clip(canvas,0,1)*255).astype(np.uint8)
    im=Image.fromarray(canvas,'RGBA')
    if show_pivots:
        d=ImageDraw.Draw(im); font=ImageFont.load_default()
        for part in PART_IDS:
            jid=JOINT_FOR_PART[part]; par=TREE[part]; Mp=compute(par)
            pt=np.array([*view.pivots[jid],1.0]); q=Mp@pt
            d.ellipse((q[0]-6,q[1]-6,q[0]+6,q[1]+6),fill=(20,220,255,255),outline=(0,0,0,255),width=2)
    return im


def trim_and_place(im: Image.Image, box, bg=(245,243,239,255)):
    bbox=im.getbbox(); crop=im.crop(bbox) if bbox else im
    target_w,target_h=box[2]-box[0],box[3]-box[1]
    crop.thumbnail((target_w,target_h),Image.Resampling.LANCZOS)
    x=box[0]+(target_w-crop.width)//2; y=box[1]+(target_h-crop.height)//2
    return crop,(x,y)


def make_previews(views):
    prev=PROJECT/'previews'; prev.mkdir(exist_ok=True)
    neutral=[]; diagnostics=[]
    for v in views:
        masks={p:Image.open(PROJECT/f'assets/{v.id}/masks/{p}.png').convert('L') for p in PART_IDS}
        n=neutral_composite(v,masks)
        n.save(prev/f'{v.id}_neutral.png')
        d=neutral_composite(v,masks,use_outlines=True,diagnostic=True)
        d.save(prev/f'{v.id}_pivot_diagnostic.png')
        neutral.append((v,n)); diagnostics.append((v,d))
    # Turnaround
    W,H=1800,1150
    sheet=Image.new('RGBA',(W,H),(242,240,236,255)); draw=ImageDraw.Draw(sheet)
    title_font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',38)
    label_font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',25)
    draw.text((40,25),'Canonical Base Body v0.1 — Neutral Turnaround',fill=(30,34,42),font=title_font)
    boxes=[(40,100,590,1080),(625,100,1175,1080),(1210,100,1760,1080)]
    for (v,im),box in zip(neutral,boxes):
        crop,pos=trim_and_place(im,box)
        sheet.alpha_composite(crop,pos)
        draw.text((box[0]+20,box[1]+10),v.label.upper(),fill=(45,50,60),font=label_font)
    sheet.convert('RGB').save(prev/'turnaround_neutral.jpg',quality=94)

    diag=Image.new('RGBA',(W,H),(242,240,236,255)); draw=ImageDraw.Draw(diag)
    draw.text((40,25),'Pivot and Part-Boundary Diagnostic',fill=(30,34,42),font=title_font)
    for (v,im),box in zip(diagnostics,boxes):
        crop,pos=trim_and_place(im,box)
        diag.alpha_composite(crop,pos)
        draw.text((box[0]+20,box[1]+10),v.label.upper(),fill=(45,50,60),font=label_font)
    diag.convert('RGB').save(prev/'pivot_diagnostic.jpg',quality=94)

    # Articulation sample poses.
    sample_angles={
        'front':{'mid_torso':-6,'chest':7,'upper_arm_L':-38,'forearm_L':52,'hand_L':-10,'upper_arm_R':35,'forearm_R':-45,'hand_R':12,'thigh_L':-14,'calf_L':28,'foot_L':-8,'thigh_R':16,'calf_R':-12,'foot_R':8},
        'three_quarter':{'mid_torso':7,'chest':-6,'upper_arm_L':20,'forearm_L':-38,'upper_arm_R':-45,'forearm_R':55,'hand_R':-12,'thigh_L':18,'calf_L':35,'thigh_R':-15,'calf_R':-24,'foot_R':10},
        'back':{'mid_torso':-5,'chest':6,'upper_arm_L':-42,'forearm_L':48,'upper_arm_R':40,'forearm_R':-52,'thigh_L':-16,'calf_L':30,'thigh_R':14,'calf_R':-20}
    }
    posed=[]
    for v in views:
        p=posed_composite(v,sample_angles[v.id],show_pivots=False)
        p.save(prev/f'{v.id}_articulation_test.png')
        posed.append((v,p))
    sheet2=Image.new('RGBA',(W,H),(235,239,244,255)); draw=ImageDraw.Draw(sheet2)
    draw.text((40,25),'Articulation Test — Same Pivot IDs Across Views',fill=(30,34,42),font=title_font)
    for (v,im),box in zip(posed,boxes):
        crop,pos=trim_and_place(im,box)
        sheet2.alpha_composite(crop,pos)
        draw.text((box[0]+20,box[1]+10),v.label.upper(),fill=(45,50,60),font=label_font)
    sheet2.convert('RGB').save(prev/'articulation_test.jpg',quality=94)


def build_manifest(views):
    manifest={
        'schemaVersion':'canonical-body-rig-0.1',
        'name':'Canonical Female Base Body',
        'canvas':{'width':CANVAS_W,'height':CANVAS_H,'units':'px'},
        'designIntent':'Headless, hairless, unclothed anatomical mannequin base with smooth non-explicit anatomy and real segmented articulation.',
        'forbiddenInThisPass':['heads','faces','hair','clothing','shoes','accessories'],
        'stablePivotIds':['root','pelvis','waist','chest','neck_socket','shoulder_L','elbow_L','wrist_L','shoulder_R','elbow_R','wrist_R','hip_L','knee_L','ankle_L','hip_R','knee_R','ankle_R'],
        'views':{}
    }
    for v in views:
        mv={
            'label':v.label,'facing':v.facing,'nearSide':v.near_side,
            'pivots':{k:[round(x,2),round(y,2)] for k,(x,y) in v.pivots.items()},
            'parts':{}
        }
        masks=create_part_masks(v)
        save_part_assets(v,masks,mv)
        manifest['views'][v.id]=mv
    (PROJECT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    return manifest


def main():
    views=build_view_defs()
    manifest=build_manifest(views)
    make_previews(views)
    print(json.dumps({'project':str(PROJECT),'views':list(manifest['views']),'partsPerView':len(PART_IDS)},indent=2))

if __name__=='__main__': main()
