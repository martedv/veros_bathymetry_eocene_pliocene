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

def resize_bathy(file):
    with xr.open_dataset(file) as f:
        topo_z = f['Z'].values

        topo_z[topo_z > 0] = 0

        oceanfloor = Image.fromarray(topo_z)
        oceanfloor = oceanfloor.crop((0, 20, 720, 340))
        oceanfloor_resize = np.array(oceanfloor.resize((90, 40), resample=3))


        return oceanfloor_resize

with h5netcdf.File('simplified_baths_old.nc', 'r') as f:
    xt = f['xt'][:]
    yt = f['yt'][:]

with h5netcdf.File('manual_baths_4deg_test.nc', 'w') as oc:
    oc._create_dimension("xt", 90)
    oc._create_dimension("yt", 40)
    oc._create_dimension("Time", 14)


    oc.create_variable("xt", ("xt",),
                       data=xt)
    oc.create_variable("yt", ("yt",),
                       data=yt)
    time = [i*5 for i in range(14)]                   
    #oc.create_variable("Time", ("Time",),
     #                  data=time)
    
    allbaths = []
    allislands = []
    for t in time:
        print(t)
        with Image.open('redone_masks/mask{}.jpg'.format(t)) as i:
            arr = np.copy(np.asarray(i))
        arr[arr > 155] = 255
        arr[arr <= 155] = 0

        mask = arr > 10
        #mask[0:1] = True
        #mask[-1::] = True
        
        z_data = np.flip(resize_bathy('Originals/TopoBathyc{}.nc'.format(t)),0)
        z_data[z_data >= 0] = 0

        islands = np.zeros(mask.shape)
        islands[mask] = 1

        allislands= allislands + \
            [np.flip(islands,0)]
        allbaths = allbaths + \
            [np.flip(z_data,0)]

    oc.create_variable("bathymetry", ("Time", "yt", "xt",),
                       data=allbaths)
    oc.create_variable("mask", ("Time", "yt", "xt"), data=allislands)
