import rasterio
import numpy as np
import math

print ("Lendo arquivos MTL")
pre_MTL = ['pre_MTL.txt']
pos_MTL = ['pos_MTL.txt']

print ("Lendo bandas")
pre_b5 = rasterio.open("pre_b5.tif")
pre_b7 = rasterio.open("pre_b7.tif")
pos_b5 = rasterio.open("pos_b5.tif")
pos_b7 = rasterio.open("pos_b7.tif")

print ("Extraindo dados dos arquivos MTL")
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
sin_pre_SUN_E = math.sin(math.radians(pre_SUN_ELEVATION))
sin_pos_SUN_E = math.sin(math.radians(pos_SUN_ELEVATION))

print ("Efetuando os cálculos (Banda 5 pré-fogo)")
r_pre_b5 = ((pre_REFLECTANCE_MULT_BAND_5*nd_pre_b5)+(pre_REFLECTANCE_ADD_BAND_5))/(sin_pre_SUN_E)

r_pre_b5Image = rasterio.open('r_pre_b5.tif','w',driver='Gtiff',
                          width = pre_b5.width, 
                          height = pre_b5.height, 
                          count=1, crs = pre_b5.crs, 
                          transform = pre_b5.transform, 
                          dtype='float64')
r_pre_b5Image.write(r_pre_b5,1)
r_pre_b5Image.close()

print ("Efetuando os cálculos (Banda 7 pré-fogo)")
r_pre_b7 = ((pre_REFLECTANCE_MULT_BAND_7*nd_pre_b7)+(pre_REFLECTANCE_ADD_BAND_7))/(sin_pre_SUN_E)

r_pre_b7Image = rasterio.open('r_pre_b7.tif','w',driver='Gtiff',
                          width = pre_b7.width, 
                          height = pre_b7.height, 
                          count=1, crs = pre_b7.crs, 
                          transform = pre_b7.transform, 
                          dtype='float64')
r_pre_b7Image.write(r_pre_b7,1)
r_pre_b7Image.close()

print ("Efetuando os cálculos (Banda 5 pós-fogo)")
r_pos_b5 = ((pos_REFLECTANCE_MULT_BAND_5*nd_pos_b5)+(pos_REFLECTANCE_ADD_BAND_5))/(sin_pos_SUN_E)

r_pos_b5Image = rasterio.open('r_pos_b5.tif','w',driver='Gtiff',
                          width = pos_b5.width, 
                          height = pos_b5.height, 
                          count=1, crs = pos_b5.crs, 
                          transform = pos_b5.transform, 
                          dtype='float64')
r_pos_b5Image.write(r_pos_b5,1)
r_pos_b5Image.close()

print ("Efetuando os cálculos (Banda 7 pós-fogo)")
r_pos_b7 = ((pos_REFLECTANCE_MULT_BAND_7*nd_pos_b7)+(pos_REFLECTANCE_ADD_BAND_7))/(sin_pos_SUN_E)

r_pos_b7Image = rasterio.open('r_pos_b7.tif','w',driver='Gtiff',
                          width = pos_b7.width, 
                          height = pos_b7.height, 
                          count=1, crs = pos_b7.crs, 
                          transform = pos_b7.transform, 
                          dtype='float64')
r_pos_b7Image.write(r_pos_b7,1)
r_pos_b7Image.close()

print ("Efetuando o calculo do NBR pré-fogo.")
nbr_pre = np.where((r_pre_b5 + r_pre_b7)==0., 0,
        (r_pre_b5 - r_pre_b7)/(r_pre_b5 + r_pre_b7))

nbr_preImage = rasterio.open('nbr_pre.tif','w',driver='Gtiff',
                          width = pre_b5.width, 
                          height = pre_b5.height, 
                          count=1, crs = pre_b5.crs, 
                          transform = pre_b5.transform, 
                          dtype='float64')
nbr_preImage.write(nbr_pre,1)
nbr_preImage.close()

print ("Efetuando o calculo do NBR pos-fogo.")
nbr_pos = np.where((r_pos_b5 + r_pos_b7)==0., 0,
        (r_pos_b5 - r_pos_b7)/(r_pos_b5 + r_pos_b7))

nbr_posImage = rasterio.open('nbr_pos.tif','w',driver='Gtiff',
                          width = pos_b5.width, 
                          height = pos_b5.height, 
                          count=1, crs = pos_b5.crs, 
                          transform = pos_b5.transform, 
                          dtype='float64')
nbr_posImage.write(nbr_pos,1)
nbr_posImage.close()
print ('---FIM---')