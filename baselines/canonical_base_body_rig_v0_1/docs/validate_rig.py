from pathlib import Path
from PIL import Image
import json, sys

ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'manifest.json').read_text())
errors=[]
expected_views={'front','three_quarter','back'}
expected_parts={'pelvis','mid_torso','chest','upper_arm_L','forearm_L','hand_L','upper_arm_R','forearm_R','hand_R','thigh_L','calf_L','foot_L','thigh_R','calf_R','foot_R'}
if set(m['views'])!=expected_views: errors.append('view set mismatch')
for vid,v in m['views'].items():
    if set(v['parts'])!=expected_parts: errors.append(f'{vid}: part set mismatch')
    if set(v['pivots'])!=set(m['stablePivotIds']): errors.append(f'{vid}: pivot set mismatch')
    for pid,p in v['parts'].items():
        for key in ['assetAligned','assetCropped','mask','outline']:
            path=ROOT/p[key]
            if not path.exists(): errors.append(f'missing {path}')
        aligned=Image.open(ROOT/p['assetAligned'])
        if aligned.size!=(1000,1700): errors.append(f'{vid}/{pid}: aligned size {aligned.size}')
        if aligned.mode!='RGBA': errors.append(f'{vid}/{pid}: aligned mode {aligned.mode}')
        if max(aligned.getchannel('A').getextrema())==0: errors.append(f'{vid}/{pid}: empty alpha')
if errors:
    print('\n'.join(errors));sys.exit(1)
print('PASS: 3 views, 45 body parts, stable pivot contract, all referenced assets present.')
