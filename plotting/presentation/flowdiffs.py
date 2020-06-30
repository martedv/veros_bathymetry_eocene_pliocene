import h5netcdf
import re
import numpy as np
import calendar
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import scipy.interpolate as ip
import scipy.signal as sn
import os
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from mpl_toolkits.axes_grid1 import make_axes_locatable
import re
import cartopy.crs as ccrs
import cartopy.util as cutil
import xarray as xr
from matplotlib import animation
from matplotlib import cm

import string
import matplotlib.colors as mcolors
import matplotlib.backends.backend_pdf
from matplotlib import rc
import matplotlib.dates as mdates

rc('font',**{'family':'serif','serif':['Computer Modern Roman'],'size'   : 10})
rc('text', usetex=True)

rundir = '../../veros_setup/runs_4_degree_last/'
time = np.arange(0,70,5)
print(rundir)

yearsdone = []
ranfory = []
BSF = []
MOC = []
SSS = []
area_u = []
area_v = []
TEMP = []
SALT = []
u = []
v = []
xt = []
yt = []
zt = []
dzt = []
dyt = []
dxt = []
dyu = []

for year in time:
    if os.path.exists(rundir + 'Run%i/run_%ima.current_run' % (year,year)):
        with open(rundir + 'Run%i/run_%ima.current_run' % (year,year)) as f:
            ranfor = int(f.readline())
        ranfory.append(ranfor)
        yearsdone.append(year)
        with xr.open_dataset(rundir + 'Run%i/run_%ima.%04d.averages.nc'% (year,year,ranfor-1)) as ds:
            BSF.append((ds['psi'].values)[0])
            TEMP.append((ds['temp'].values)[0])
            SSS.append((ds['salt'].values)[0])
            u.append((ds['u'].values)[0])
            v.append((ds['v'].values)[0])
            if xt == []:
                xt = ds['xt'].values
                yt = ds['yt'].values
                zt = ds['zt'].values
        with xr.open_dataset(rundir + 'Run%i/run_%ima.%04d.overturning.nc'% (year,year,ranfor-1)) as ds:
            MOC.append(-(ds['vsf_depth'].values)[0] - (ds['bolus_depth'].values)[0])
        with xr.open_dataset(rundir + 'Run%i/run_%ima.%04d.snapshot.nc'% (year,year,ranfor -1)) as ds:
            area_u.append(ds['area_u'].values)
            area_v.append(ds['area_v'].values)
            if dzt == []:
                dzt = ds['dzt'].values
                dyt = ds['dyt'].values
                dxt = ds['dxt'].values
                dyu = ds['dyu'].values
print(ranfory)
from PIL import Image


def resize_array(toresize):
    asimg = Image.fromarray(toresize)
    _resize = np.array(asimg.resize((360, 160), resample=3))
    return _resize

with xr.open_dataset('../notebooks/Data/idealized_forcing_4deg.nc') as f:
    sss = resize_array(np.nanmean(f['sss'].values,axis=0))
    sst = resize_array(np.nanmean(f['sst'].values,axis=0))
    tau_x = resize_array(np.nanmean(f['tau_x'].values,axis=0))

with xr.open_dataset('../notebooks/Data/forcing_1deg_global.nc') as f:
    sss_1d = np.nanmean(f['sss'].values,axis=0)
    sst_1d = np.nanmean(f['sst'].values,axis=0)
    tau_x_1d = np.nanmean(f['tau_x'].values,axis=0)
    xt = f['xt'].values
    yt = f['yt'].values

mask = sss_1d == 0.
sss_1d[mask] = np.nan
sss[mask] = np.nan
sst_1d[mask] = np.nan
sst[mask] = np.nan

fig, axes = plt.subplots( 1,2, subplot_kw=dict(projection=ccrs.PlateCarree(central_longitude=180)),figsize=(2*8, 2*5))
fig.patch.set_alpha(0)

gl = axes[0].gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='gray', alpha=0.5, linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.ylabels_left = True
gl.ylocator = mticker.FixedLocator([-80, -60, -30, 0, 30, 60, 80])
gl.xlocator = mticker.FixedLocator([-180,-90, 0,90, 180])
#SSS
axes[0].imshow(np.tile(np.array([[[80, 80, 80]]], 
          dtype=np.uint8), [2, 2, 1]),
      origin='upper',
      transform=ccrs.PlateCarree(),
      extent=[-180, 180, -180, 180])
cs = axes[0].contourf(xt,yt,sss - sss_1d,cmap='BrBG_r',levels=np.arange(-5,5.1,0.1),extend='both')
axes[0].contour(xt,yt,sss - sss_1d,levels=np.arange(-5,5.1,1),colors='k',linewidths=0.5)
#axes[0].set_title('a) SSS difference (psu)', loc='left')
plt.colorbar(cs,ticks=[-5,-3,0,3,5],format=r"$%i$ psu",fraction=0.020, pad=0.03, ax=axes[0])


gl = axes[1].gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='gray', alpha=0.5, linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.ylabels_left = False

gl.ylocator = mticker.FixedLocator([-80, -60, -30, 0, 30, 60, 80])
gl.xlocator = mticker.FixedLocator([-180,-90, 0,90, 180])
#SSS
axes[1].imshow(np.tile(np.array([[[80, 80, 80]]], 
          dtype=np.uint8), [2, 2, 1]),
      origin='upper',
      transform=ccrs.PlateCarree(),
      extent=[-180, 180, -180, 180])
cs = axes[1].contourf(xt,yt,sst - sst_1d,cmap='RdBu_r',levels=np.arange(-8,8.1,0.1),extend='both')
axes[1].contour(xt,yt,sst - sst_1d,levels=np.arange(-8,8.1,1),colors='k',linewidths=0.5)
#axes[1].set_title('b) SST difference ($^{\circ}C$)', loc='left')
plt.colorbar(cs,ticks=np.arange(-8,8.1,2),format=r"$%i^{\circ}C$",fraction=0.020, pad=0.03, ax=axes[1])
plt.show()
