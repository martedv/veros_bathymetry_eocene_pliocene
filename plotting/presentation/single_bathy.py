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

rc('font',**{'family':'serif','serif':['Computer Modern Roman'],'size'   : 10})
rc('text', usetex=True)

baths = xr.open_dataset('../notebooks/Data/manual_baths_4deg_final.nc')
windall = xr.open_dataset('../notebooks/Data/wind1_all_1400.nc')

fig = plt.figure()
fig.patch.set_alpha(0)
ax = plt.axes(projection=ccrs.PlateCarree())

xt = baths['xt'].values
yt = baths['yt'].values
zt = windall['zt'].values
Z = baths['mask'].values
d_Z = baths['bathymetry'].values

Z0 = d_Z[0]
Z0[Z[0] == 1.] = np.nan

depth, xtf = cutil.add_cyclic_point(np.roll(Z0,45,axis=1), coord=xt)

ax.imshow(np.tile(np.array([[[165, 214, 121]]], 
          dtype=np.uint8), [2, 2, 1]),
      origin='upper',
      transform=ccrs.PlateCarree(),
      extent=[-180, 180, -180, 180])

plt.pcolormesh(xtf,yt,depth,cmap='Blues',transform=ccrs.PlateCarree())

ax.set_frame_on(False)
#plt.show()

fig = plt.figure(figsize=(1.3, 5))
fig.patch.set_alpha(0)
ax = fig.add_subplot(1,1,1)
ax.pcolormesh([0,1],zt,np.transpose([zt,zt]),cmap='Blues')
# ax.set_xlim(0,0.5)
ax.set_ylim(-5000,0)
ax.hlines(zt,0,np.ones(zt.shape))
ax.get_xaxis().set_visible(False)
#ax.set_frame_on(False)
# import matplotlib as mpl
# norm = mpl.colors.Normalize(vmin=-5000, vmax=0)

ax.yaxis.set_minor_locator(mticker.AutoMinorLocator())
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%i m'))
fig.tight_layout()
plt.show()


with h5netcdf.File('Data/idealized_forcing_4deg.nc') as f:
    yt = f['yt'][:]
    sss = f['sss'][:]
    sst = f['sst'][:]
    tau_x = f['tau_x'][:]
    q_net = f['q_net'][:]
    q_nec = f['q_nec'][:]
