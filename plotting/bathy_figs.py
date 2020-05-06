import h5netcdf
import re
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import os
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
import re
import cartopy.crs as ccrs
import cartopy.util as cutil
import xarray as xr
from matplotlib import animation
import matplotlib.backends.backend_pdf

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Computer Modern Roman'],'size'   : 11})
rc('text', usetex=True)


with h5netcdf.File('manual_baths_4deg_test.nc', 'r') as f:
    bathymetry = f['bathymetry'][:]
    mask = f['mask'][:]

    xt = f['xt'][:]
    #xt = np.roll(xt,45)
    yt = f['yt'][:]

    time = [0,5,10,15,20,25,30,35,40,45,50,55,60,65]

    for i, t in enumerate(time):
        xt = f['xt'][:]
        fig = plt.figure()
        ax = plt.subplot(projection=ccrs.Mercator())
        ax.set_extent([-180, 180, -75, 75])
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='gray', alpha=0.7, linestyle='--')
        ax.imshow(np.tile(np.array([[[0, 0, 0]]], 
            dtype=np.uint8), [2, 2, 1]),
        origin='upper',
        transform=ccrs.PlateCarree(),
        extent=[-180, 180, -180, 180])
        gl.xlabels_top = False
        gl.ylabels_left = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.ylocator = mticker.FixedLocator([-90, -60, -30, 0, 30, 60, 90])
        bt = bathymetry[i]
        bt[mask[i] == 1] = np.nan
        #bt = np.roll(bt,45)
        bt, xt = cutil.add_cyclic_point(bt, coord=xt)
        


        col = plt.pcolormesh(xt,yt,np.roll(bathymetry[i],45, axis=1), cmap='rainbow', transform=ccrs.PlateCarree())
        plt.title('Bathymetry %dMa' % (t))
        fig.colorbar(col,format='%i m', fraction=0.025, pad=0.08)
        plt.savefig('figures/bathymetry/baath_%d.png' % (t))
        