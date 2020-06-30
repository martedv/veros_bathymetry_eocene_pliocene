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
import h5netcdf
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import os
import cartopy.util as cutil
import re
import cartopy.crs as ccrs
import xarray as xr
from matplotlib import animation
rc('text', usetex=True)
rc('font',**{'family':'Dosis','serif':['Dosis'],'size'   : 10})


with h5netcdf.File('../notebooks/Data/idealized_forcing_4deg.nc') as f:
    yt = f['yt'][:]
    xt = f['xt'][:]
    sss = f['sss'][:]
    sst = f['sst'][:]
    tau_x = f['tau_x'][:]
    q_net = f['q_net'][:]
    q_nec = f['q_nec'][:]

with xr.open_dataset('../notebooks/Data/forcing_1deg_global.nc') as f:
    tau_x_1d = f['tau_x'].values
    yt_1d = f['yt'].values

fig = plt.figure()
fig.patch.set_alpha(0)
ax = plt.axes()


tau_x_1d[tau_x_1d == 0.] = np.nan
#plt.plot(xnew,power_smooth)
ax.plot(yt_1d,np.nanmean(np.nanmean(tau_x_1d,axis=0),axis=1),'r-',label=r"$\tau_x$ ECMWF-$1^{\circ}$ 2020")
#plt.plot(yt,tau_x[0,:,0],'ks--',label=r"$\mu(\tau_x)_{eq}$")


bryanori = np.array([-1,-3,-4.5,-6,-6,-3,0,3,6,9,10,9,3,-0.5,-4.5,-6,-6,-3,-3])
bryan = np.append(np.flip(bryanori),bryanori)


xold = np.linspace(-90,90,38)
xnew = np.linspace(-80,80,40)

newspl = ip.make_interp_spline(xold, bryan, k=3)
smoothed = newspl(xnew)
ax.plot(xnew,smoothed/1e2,'ks--',label=r"$\tau_x$ Bryan 1987")
ax.legend()

ax.set_ylabel(r'Wind-stress $N m^{-2}$')
ax.set_xlabel('Latitude')
ax.set_xlim(-80,80)
ax.set_ylim(-0.16,0.16)
ax.xaxis.set_minor_locator(mticker.AutoMinorLocator())
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%i'))
ax.grid()
plt.tight_layout()


fig = plt.figure()
fig.patch.set_alpha(0)
ax = plt.axes()


#plt.pcolormesh(np.arange(1,13,1),yt,np.transpose(sst[:,:,0]),cmap='coolwarm')
tom = ax.contourf(np.arange(1,13,1),yt,np.transpose(sst[:,:,0]),np.arange(-30,30.1,1),cmap='RdBu_r',extend='both')
# plt.contour(np.arange(1,13,1),yt,np.transpose(sst[:,:,0]),np.arange(-30,30.1,5),colors='k',linewidths=0.7)
plt.colorbar(tom,orientation='horizontal',ticks=np.arange(-30,31,10),aspect=40,format=r'%i$^{\circ}C$')
plt.yticks([-80,-60,-30,0,30,60,80])
plt.xticks(np.arange(1,13), calendar.month_abbr[1:13], rotation=45)
ax.yaxis.set_minor_locator(mticker.AutoMinorLocator())
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('$%i^{\circ}$'))
plt.show()

fig = plt.figure()
fig.patch.set_alpha(0)
ax = plt.axes()


#plt.pcolormesh(np.arange(1,13,1),yt,np.transpose(sst[:,:,0]),cmap='coolwarm')
tom = ax.contourf(np.arange(1,13,1),yt,np.transpose(sss[:,:,0]),np.arange(32,36.1,0.1),cmap='BrBG_r',extend='both')
# plt.contour(np.arange(1,13,1),yt,np.transpose(sst[:,:,0]),np.arange(-30,30.1,5),colors='k',linewidths=0.7)
plt.colorbar(tom,orientation='horizontal',ticks=np.arange(32,36.1,0.5),aspect=40,format=r'%i psu')
plt.yticks([-80,-60,-30,0,30,60,80])
plt.xticks(np.arange(1,13), calendar.month_abbr[1:13], rotation=45)
ax.yaxis.set_minor_locator(mticker.AutoMinorLocator())
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('$%i^{\circ}$'))
plt.show()