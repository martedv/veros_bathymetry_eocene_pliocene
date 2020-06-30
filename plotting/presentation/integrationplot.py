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


years = np.arange(0,65.1,5)
rundir = '../../veros_setup/runs_4_degree_last/'
alltemps = []
j = 0
for year in years:
    #check if a run is done
    if os.path.exists(rundir + 'Run%i/run_%ima.current_run' % (year,year)):
        with open(rundir + 'Run%i/run_%ima.current_run' % (year,year)) as f:
            ranfor = int(f.readline())
        
        alltemps.append([])
        
        for i in range(100,ranfor,20):
            #open averages
            #get temprature
            # mean of surface
            with xr.open_dataset(rundir + 'Run%i/run_%ima.%04d.averages.nc'% (year,year,i)) as ds:
                alltemps[j].append(np.nanmean(ds['temp'][0].values))
        j = j + 1

fig = plt.figure()
fig.patch.set_alpha(0)
ax = plt.axes()

linestys = ['dotted','dashed','dashdot']
time=np.arange(0,65.1,5)
for i in range(14):
    ax.plot(range(100,ranfor,20),np.gradient(alltemps[i]),linestyle=linestys[i % 3],label="%i Ma" % time[i])
ax.set_xlim(100,500)
ax.set_ylim(-0.075,0.075)
#ax.xaxis.set_minor_locator(mticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(mticker.AutoMinorLocator())
ax.set_xlabel('Integration time (years)')
ax.set_ylabel('Temerature drift ($^{\circ}C a^{-1}$)')
ax.grid()
ax.legend(bbox_to_anchor=(1.03,0.86))
plt.tight_layout()
plt.show()