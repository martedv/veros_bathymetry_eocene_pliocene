import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.colors as colors
import csv
from matplotlib import rc
import os
import re
import cartopy.crs as ccrs
import xarray as xr
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import animation
import matplotlib.ticker as ticker
import cartopy.util as cutil
from scipy.integrate import quad
rc('text', usetex=True)

years = [35, 45]
rundir = '../actual_runs/runs_4_degree_final_forcing/'
for year in years:
    #check if a run is done
    if os.path.exists(rundir + 'Run%i/run_%ima.current_run' % (year,year)):
        with open(rundir + 'Run%i/run_%ima.current_run' % (year,year)) as f:
            ranfor = int(f.readline())
        meantempratures = []
        for i in range(ranfor):
            #open averages
            #get temprature
            # mean of surface
            with xr.open_dataset(rundir + 'Run%i/run_%ima.%04d.averages.nc'% (year,year,i)) as ds:
                temps = np.array(ds['temp'].values)[0,:,:,:]
                meantempratures.append(np.nanmean(temps))
        plt.plot(np.gradient(meantempratures), label=np.gradient(meantempratures)[-1])
plt.legend()
plt.show()
        
#overt = [xr.open_dataset('../actual_runs/runs_4_degree_final_forcing/' + filename) for filename in filesovert]



