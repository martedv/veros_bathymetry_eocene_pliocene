import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
from matplotlib import rc
import os
import re
import cartopy.crs as ccrs
import xarray as xr
from matplotlib import animation
import matplotlib.ticker as ticker

from scipy.integrate import quad
rc('text', usetex=True)

dirname = os.path.dirname(__file__)

filesovert = ['Run0/4deg-0ma-200y.overturning.nc',
        'Run5/4deg-5ma-200y.overturning.nc', 'Run10/4deg-10ma-200y.overturning.nc', 'Run15/4deg-15ma-200y.overturning.nc', 'Run20/4deg-20ma-200y.overturning.nc',
        'Run25/4deg-25ma-200y.overturning.nc', 'Run30/4deg-30ma-200y.overturning.nc', 'Run35/4deg-35ma-200y.overturning.nc', 'Run40/4deg-40ma-200y.overturning.nc', 
        'Run45/4deg-45ma-200y.overturning.nc', 'Run50/4deg-50ma-200y.overturning.nc', 'Run55/4deg-55ma-200y.overturning.nc', 'Run60/4deg-60ma-200y.overturning.nc','Run65/4deg-65ma-200y.overturning.nc']

overt = [xr.open_dataset(dirname + '../actual_runs/runs_4_degree/' + filename) for filename in filesovert]

yt = overt[0]['yt'].values
zt = overt[0]['zt'].values


fig,ax = plt.subplots(5,3, sharex=True, sharey=True)

i = 0

t = [0,5,10,15,20,25,30,35,40,45,50,55,60,65]
for row in ax:
    for col in row:
        if i > 13:
                continue
        cbar_ = col.pcolormesh(yt,zt, (overt[13 - i]['vsf_depth'][199].values + overt[13 - i]['bolus_depth'][199].values) / (10**6) , vmin=-25, vmax=25, cmap='coolwarm')
        col.yaxis.set_major_formatter(ticker.FormatStrFormatter("$%i$ m"))
        col.xaxis.set_major_formatter(ticker.FormatStrFormatter("$%i^{\circ}$"))
        col.set_title('%i Ma' % t[13 - i])
        i = i + 1

fig.colorbar(cbar_, ax=ax.ravel().tolist(),format='%i Sv')
plt.show()

# for row in ax:
#         for col in row:
#                 contourf_ = col.pcolormesh(yt,zt, overt[0]['vsf_depth'][199].values / (10**6), vmin=-25, vmax=25, cmap='coolwarm')
                
# cbar = fig.colorbar(contourf_,format='%i Sv')
# ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("$%i$ m"))
# ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("$%i^{\circ}$"))
# plt.show()