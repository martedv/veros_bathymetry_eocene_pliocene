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

with xr.open_dataset('../../map_manipulation/bathymetrys/Originals/TopoBathyc30.nc') as trueset:
    lat = trueset['latitude'].values
    longt = trueset['longitude'].values
    Z = trueset['Z'].values

fig = plt.figure(figsize=(10, 5))
fig.patch.set_alpha(0)
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson(),frameon=False)

mask = np.zeros(Z.shape)
mask[Z >= 0] = 1.
mask[Z < 0] = 0.
Z[mask == 1.] = np.nan
print(Z)

ax.imshow(np.tile(np.array([[[165, 214, 121]]], 
          dtype=np.uint8), [2, 2, 1]),
      origin='upper',
      transform=ccrs.PlateCarree(),
      extent=[-180, 180, -180, 180])

plt.contourf(longt, lat, Z,cmap='Blues', vmin=-6000,vmax=0,transform=ccrs.PlateCarree())
plt.contour(longt, lat, mask, colors='k', linewidths = 0.5,transform=ccrs.PlateCarree())

ax.background_patch.set_alpha(0)
plt.show()

