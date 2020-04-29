import h5netcdf
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import os
import re
import cartopy.crs as ccrs
import cartopy.util as cutil
import xarray as xr
from matplotlib import animation

with xr.open_dataset('manual_baths_4deg_test.nc') as f:
    bathymetry = f['bathymetry'].values
    mask = f['mask'].values

    xt = f['xt'].values
    #xt = np.roll(xt,45)
    yt = f['yt'].values

    time = [0,5,10,15,20,25,30,35,40,45,50,55,60,65]


    
    for i, t in enumerate(time):
        xt = f['xt'].values
        fig = plt.figure()
        ax = plt.subplot(projection=ccrs.PlateCarree())
        
        bt = bathymetry[i]
        bt[mask[i] == 1] = np.nan
        #bt = np.roll(bt,45)
        bt, xt = cutil.add_cyclic_point(bt, coord=xt)
        plt.pcolormesh(xt,yt,mask[i])
        plt.show()
        
