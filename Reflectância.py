import rasterio
import numpy as np
import math
import os

pre_MTL = [i for i in os.listdir('.') if i.endswith('pre_MTL.txt')]
pos_MTL = [i for i in os.listdir('.') if i.endswith('pos_MTL.txt')]
pre_b5 = rasterio.open("pre_b5.tif")
pre_b7 = rasterio.open("pre_b7.tif")
pos_b5 = rasterio.open("pos_b5.tif")
pos_b7 = rasterio.open("pos_b7.tif")

for line in open(pre_MTL[0]):
    if 'REFLECTANCE_MULT_BAND_5' in line:
        pre_REFLECTANCE_MULT_BAND_5 = float(line.split('=')[-1])
    elif 'REFLECTANCE_MULT_BAND_7' in line:
        pre_REFLECTANCE_MULT_BAND_7 = float(line.split('=')[-1])
    elif 'REFLECTANCE_ADD_BAND_5' in line:
        pre_REFLECTANCE_ADD_BAND_5 = float(line.split('=')[-1])
    elif 'REFLECTANCE_ADD_BAND_7' in line:
        pre_REFLECTANCE_ADD_BAND_7 = float(line.split('=')[-1])
    elif 'SUN_ELEVATION' in line:
        pre_SUN_ELEVATION = float(line.split('=')[-1])       
for line in open(pos_MTL[0]):
    if 'REFLECTANCE_MULT_BAND_5' in line:
        pos_REFLECTANCE_MULT_BAND_5 = float(line.split('=')[-1])
    elif 'REFLECTANCE_MULT_BAND_7' in line:
        pos_REFLECTANCE_MULT_BAND_7 = float(line.split('=')[-1])
    elif 'REFLECTANCE_ADD_BAND_5' in line:
        pos_REFLECTANCE_ADD_BAND_5 = float(line.split('=')[-1])
    elif 'REFLECTANCE_ADD_BAND_7' in line:
        pos_REFLECTANCE_ADD_BAND_7 = float(line.split('=')[-1])
    elif 'SUN_ELEVATION' in line:
        pos_SUN_ELEVATION = float(line.split('=')[-1])

nd_pre_b5 = pre_b5.read(1).astype('float64')
nd_pre_b7 = pre_b7.read(1).astype('float64')
nd_pos_b5 = pos_b5.read(1).astype('float64')
nd_pos_b7 = pos_b7.read(1).astype('float64')
sin_pre_SUN_E = math.sin(pre_SUN_ELEVATION)
sin_pos_SUN_E = math.sin(pos_SUN_ELEVATION)

r_pre_b5=np.where(
    (nd_pre_b5)==0., 
    0, 
    ((pre_REFLECTANCE_MULT_BAND_5*nd_pre_b5)+(pre_REFLECTANCE_ADD_BAND_5))/(sin_pre_SUN_E))

r_pre_b5Image = rasterio.open('r_pre_b5.tif','w',driver='Gtiff',
                          width = pre_b5.width, 
                          height = pre_b5.height, 
                          count=1, crs = pre_b5.crs, 
                          transform = pre_b5.transform, 
                          dtype='float64')
r_pre_b5Image.write(r_pre_b5,1)
r_pre_b5Image.close()

