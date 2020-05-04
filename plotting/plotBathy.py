import h5netcdf
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import os

from mpl_toolkits.axes_grid1 import make_axes_locatable
import re
import cartopy.crs as ccrs
import cartopy.util as cutil
import xarray as xr
from matplotlib import animation
import matplotlib.backends.backend_pdf
pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")

with xr.open_dataset('manual_baths_4deg_test.nc') as f:
    bathymetry = f['bathymetry'].values
    mask = f['mask'].values

    xt = f['xt'].values
    #xt = np.roll(xt,45)
    yt = f['yt'].values

    time = [0,5,10,15,20,25,30,35,40,45,50,55,60,65]


    
    for i, t in enumerate(time):
        with xr.open_dataset('../map_manipulation/bathymetrys/Originals/TopoBathyc{}.nc'.format(t)) as trueset:
            lat = trueset['latitude'].values
            longt = trueset['longitude'].values
            Z = trueset['Z'].values

        xt = f['xt'].values
        fig = plt.figure()
        ax = plt.subplot(projection=ccrs.PlateCarree())
        ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='gray', alpha=0.5, linestyle='--')
        bt = bathymetry[i]
        bt[mask[i] == 1] = np.nan
        #bt = np.roll(bt,45)
        bt, xt = cutil.add_cyclic_point(bt, coord=xt)
        
        realb = Z
        realb[realb < -100] = np.nan
        realb[realb >= -100] = 0

        lowb = mask[i]
        lowb[lowb == 0] = np.nan
        lowb = np.roll(lowb,45, axis=1)

        

        col = plt.pcolormesh(xt,yt,np.roll(bathymetry[i],45, axis=1), cmap='plasma', transform=ccrs.PlateCarree())
        
        fig.colorbar(col,format='%i m', fraction=0.025, pad=0.08)
        plt.pcolormesh(xt,yt,lowb, cmap='gray', transform=ccrs.PlateCarree())
        plt.pcolor(longt,lat,realb, cmap='binary', transform=ccrs.PlateCarree(), alpha=0.6, snap=True)
        plt.title('Bathymetry %dMa' % (t), y=1.08)
        #plt.show()
        pdf.savefig( fig )
        print('done %s' % (t))
pdf.close()
        
