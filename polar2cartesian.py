import os, math, json
import pandas as pd
import numpy as np
import sys

dir=str(sys.argv[1])
files = sorted([dir+"/"+f for f in os.listdir(dir) if f.endswith('.txt')])

scans = []
for f in files:
    epoch_ms = int(f.replace(dir+"/",'').replace('.txt',''))
    df = pd.read_csv(f'{f}', sep='\t', header=None,
                     names=['flag','intensity','angle_deg','distance_mm'])
    # Convert polar to Cartesian (standard math convention: 0° = East, CCW)
    df['angle_rad'] = df['angle_deg'] * math.pi / 180.0
    df['x'] = (df['distance_mm'] * df['angle_rad'].apply(math.cos)).round(2)
    df['y'] = (df['distance_mm'] * df['angle_rad'].apply(math.sin)).round(2)
    
    pts = df[["x","y"]].values
    scans.append(pts)

scans=np.array(scans)
print(scans.shape)
np.save(dir+"/lidar_scans_cartesian.npy",scans)
