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

with xr.open_dataset('../notebooks/Data/wind1_all_1400.nc') as f:
    T_1400 = f['temp'].values[-1]
    bsf_1400 = f['psi'].values[-1]
    xt_1400 = f['xt'].values

fig, axes = plt.subplots( 2,2, subplot_kw=dict(projection=ccrs.PlateCarree(central_longitude=180)),figsize=(2*9, 2*4))
fig.patch.set_alpha(0)

for i, t in enumerate([7,6,5,4]):
    gl = axes[int(i/2), i % 2].gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=0, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.ylabels_left = True
    gl.ylocator = mticker.FixedLocator([-80, -60, -30, 0, 30, 60, 80])
    gl.xlocator = mticker.FixedLocator([-180,-90, 0,90, 180])
    bs, xtfr = cutil.add_cyclic_point(np.roll(-BSF[t],45,axis=1), coord=xt)
    axes[int(i/2), i % 2].set_facecolor('#cccccc')
    axes[int(i/2), i % 2].contourf(xtfr,yt,bs/1e6,cmap='RdBu_r',transform=ccrs.PlateCarree(),corner_mask=False,extend='both',levels=np.arange(-60,60.1,0.1))
    axes[int(i/2), i % 2].contour(xtfr,yt,bs/1e6,colors='k', levels=np.arange(-60,60.1,5),
         transform=ccrs.PlateCarree(),
        linewidths = 0.2,corner_mask=False)

plt.show()