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


filesovert = ['Run0/run_0ma.0009.overturning.nc',
        'Run5/run_5ma.0009.overturning.nc', 'Run10/run_10ma.0009.overturning.nc', 'Run15/run_15ma.0009.overturning.nc', 'Run20/run_20ma.0009.overturning.nc',
        'Run25/run_25ma.0009.overturning.nc', 'Run30/run_30ma.0009.overturning.nc', 'Run35/run_35ma.0009.overturning.nc', 'Run40/run_40ma.0009.overturning.nc', 
        'Run45/run_45ma.0009.overturning.nc', 'Run50/run_50ma.0009.overturning.nc', 'Run55/run_55ma.0009.overturning.nc', 'Run60/run_60ma.0009.overturning.nc','Run65/run_65ma.0009.overturning.nc']

overt = [xr.open_dataset('../actual_runs/runs_4_degree_final_forcing/' + filename) for filename in filesovert]

yt = overt[0]['yt'].values
zt = overt[0]['zt'].values


fig,ax = plt.subplots(5,3, sharex=True, sharey=True)

i = 0

t = [0,5,10,15,20,25,30,35,40,45,50,55,60,65]
for row in ax:
    for col in row:
        if i > 13:
                continue
        cbar_ = col.pcolormesh(yt,zt, (overt[13 - i]['vsf_depth'][0].values + overt[13 - i]['bolus_depth'][0].values) / (-10**6) , vmin=-25, vmax=25, cmap='coolwarm')
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
