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


with xr.open_dataset('../notebooks/Data/overturning.1400.nc') as f:
    moc_1400 = -(f['vsf_depth'].values[500] + f['bolus_depth'].values[500])
    xt_1400 = f['xt'].values

moc_1400[moc_1400 == 0.] = np.nan
moc = np.array(MOC[0])
moc[moc == 0.] = np.nan

fig, axes = plt.subplots( 2,1,figsize=(6, 8))
fig.patch.set_alpha(0)
axes[0].contourf(yt,zt, moc/1e6,np.arange(-20,20.1,1),cmap='RdBu_r',extend='both',corner_mask=False)
#axes[0].set_title('a) MOC simplified forcings',loc='left')
#contourticks = np.array([-16,-14,-12,-10,-8,-6,-4,-2,-1,0,1,2,4,6,8,10,12,14,16])
#axes[0].contour(yt,zt,moc/1e6, contourticks, colors='w',linewidths=0.7,corner_mask=False,extend='both')
cs = axes[1].contourf(yt,zt, moc_1400/1e6,np.arange(-20,20.1,1),cmap='RdBu_r',corner_mask=False,extend='both')
#axes[1].set_title('b) MOC realistic forcings',loc='left')
#axes[1].contour(yt,zt,moc_1400/1e6, contourticks, colors='w',linewidths=0.7,corner_mask=False,extend='both')

axes[0].set_xticks([-80,-60,-40,-20,0,20,40,60,80])
axes[1].set_xticks([-80,-60,-40,-20,0,20,40,60,80])
axes[0].xaxis.set_minor_locator(mticker.AutoMinorLocator())
axes[0].xaxis.set_major_formatter(mticker.FormatStrFormatter('$%i^{\circ}$'))
axes[1].xaxis.set_major_formatter(mticker.FormatStrFormatter('$%i^{\circ}$'))

axes[1].xaxis.set_minor_locator(mticker.AutoMinorLocator())
axes[0].xaxis.set_minor_locator(mticker.AutoMinorLocator())

axes[0].yaxis.set_major_formatter(mticker.FormatStrFormatter('%i m'))
axes[1].yaxis.set_major_formatter(mticker.FormatStrFormatter('%i m'))

axes[0].set_yticks([-5000,-4000,-3000,-2000,-1000,0])
axes[1].set_yticks([-5000,-4000,-3000,-2000,-1000,0])


axes[0].set_facecolor('#cccccc')
axes[1].set_facecolor('#cccccc')


fig = plt.figure(figsize=(1, 5))
fig.patch.set_alpha(0)
ax = plt.axes()

fig.colorbar(cs,ticks=[-30,-20,-10, 0, 10,20,30], cax=ax,format='%i Sv', orientation='vertical')
plt.tight_layout()


fig= plt.figure(figsize=(5, 3))
fig.patch.set_alpha(0)
ax = plt.axes()
ax.set_xbound(lower=-80, upper=80)
ax.set_ylim(-6000,0)
ax.xaxis.set_minor_locator(mticker.AutoMinorLocator())
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%i m'))
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('$%i^{\circ}$'))
plt.show()