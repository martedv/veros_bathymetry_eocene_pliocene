import h5netcdf
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import matplotlib
import csv
import os
import re
from PIL import Image
import xarray as xr
import scipy.misc
from scipy import ndimage
from scipy.sparse.csgraph import connected_components
from scipy.sparse import csr_matrix
import struct


dirname = os.path.dirname(__file__)
def resize_bathy(file,time):
    with xr.open_dataset(file) as f:
        topo_z = f['Z'].values

        topo_z[topo_z >= -100] = 0.

        

        maskimg = Image.fromarray(topo_z >= 0)
        maskimg = maskimg.rotate(180)
        maskimg = maskimg.transpose(Image.FLIP_LEFT_RIGHT)
        #maskimg = maskimg.crop((0, 20, 720, 360))
        maskimg.save("masks_4deg/mask_original{}.jpg".format(time))

        oceanfloor = Image.fromarray(topo_z)
        oceanfloor = oceanfloor.crop((0, 20, 720, 360))
        oceanfloor_resize = np.array(oceanfloor.resize((90, 40), resample=3))
        oceanfloor_resize[0:2] = 0.
        oceanfloor_resize[-2::] = 0.


        marginal = (
            scipy.ndimage.binary_erosion(
                scipy.ndimage.binary_fill_holes(
                    scipy.ndimage.binary_dilation(oceanfloor_resize > -50)
                )
            )
        )
        
        oceanfloor_resize[marginal] = 0.

        

        mask = np.array(oceanfloor_resize) >= -30

        maskimg = Image.fromarray(mask)
        maskimg = maskimg.rotate(180)
        maskimg = maskimg.transpose(Image.FLIP_LEFT_RIGHT)
        maskimg.save("masks_4deg/mask{}.jpg".format(time))
        

        
        oceanfloor_resize[oceanfloor_resize > 0.] = 0.
        oceanfloor_resize[mask] = 0.

        actual = np.array(oceanfloor_resize)


        return np.roll(actual, 45)
with h5netcdf.File('simplified_baths_old.nc', 'r') as f:
    xt = f['xt'][:]
    yt = f['yt'][:]


with h5netcdf.File('simplified_baths_4deg.nc', 'w') as oc:
    oc._create_dimension("xt", 90)
    oc._create_dimension("yt", 40)
    oc._create_dimension("Time", 14)


    oc.create_variable("xt", ("xt",),
                       data=xt)
    oc.create_variable("yt", ("yt",),
                       data=yt)
    time = [i*5 for i in range(14)]
    
    
    oc.create_variable("Time", ("Time",),
                       data=time)
    allbaths = []
    for i in range(14):
        allbaths = allbaths + \
            [resize_bathy('Originals/TopoBathyc{}.nc'.format(i*5),i*5)]
   
    oc.create_variable("bathymetry", ("Time", "yt", "xt",),
                       data=allbaths)
