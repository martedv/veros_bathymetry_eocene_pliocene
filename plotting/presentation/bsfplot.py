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
            BSF.append(-(ds['psi'].values)[0])
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

with xr.open_dataset('../notebooks/Data/wind1_all_1400.nc') as f:
    T_1400 = f['temp'].values[-1]
    bsf_1400 = f['psi'].values[-1]
    xt_1400 = f['xt'].values

fig, axes = plt.subplots( 1,2, subplot_kw=dict(projection=ccrs.PlateCarree(central_longitude=180)),figsize=(2*9, 2*4))
fig.patch.set_alpha(0)
gl = axes[0].gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=0, color='gray', alpha=0.5, linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.ylabels_left = True
gl.ylocator = mticker.FixedLocator([-80, -60, -30, 0, 30, 60, 80])
gl.xlocator = mticker.FixedLocator([-180,-90, 0,90, 180])
#SSS
axes[0].imshow(np.tile(np.array([[[140, 140, 140]]], 
          dtype=np.uint8), [2, 2, 1]),
      origin='upper',
      transform=ccrs.PlateCarree(),
      extent=[-180, 180, -180, 180])
bs, xtf = cutil.add_cyclic_point(np.roll(BSF[0],45,axis=1), coord=xt)
axes[0].contourf(xtf,yt,-bs/1e6,levels=np.arange(-60,60.1,0.1),cmap='RdBu_r',extend='both',transform=ccrs.PlateCarree(),corner_mask=False)
axes[0].contour(xtf,yt,-bs / 1e6, colors='k', levels=np.arange(-60,60.1,5), transform=ccrs.PlateCarree(),
linewidths = 0.2,corner_mask=False)


gl = axes[1].gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=0, color='gray', alpha=0.5, linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.ylabels_left = False
gl.ylocator = mticker.FixedLocator([-80, -60, -30, 0, 30, 60, 80])
gl.xlocator = mticker.FixedLocator([-180,-90, 0,90, 180])
#SSS
axes[1].imshow(np.tile(np.array([[[140, 140, 140]]], 
          dtype=np.uint8), [2, 2, 1]),
      origin='upper',
      transform=ccrs.PlateCarree(),
      extent=[-180, 180, -180, 180])

bsf, xtfr = cutil.add_cyclic_point(np.roll(bsf_1400,45,axis=1), coord=xt_1400)
cs = axes[1].contourf(xtfr,yt,bsf/1e6,levels=np.arange(-60,60.1,0.1),cmap='RdBu_r',extend='both',corner_mask=False,transform=ccrs.PlateCarree())
axes[1].contour(xtfr,yt,bsf/1e6, colors='k', levels=np.arange(-60,60.1,5), transform=ccrs.PlateCarree(),
linewidths = 0.2,corner_mask=False)

fig.subplots_adjust(bottom=-0.05)
cbar_ax = fig.add_axes([0.12, 0.10, 0.78, 0.035])
fig.colorbar(cs,ticks=[-60,-40,-20, 0, 20,40,60], cax=cbar_ax,format='%i Sv', orientation='horizontal')

plt.show()