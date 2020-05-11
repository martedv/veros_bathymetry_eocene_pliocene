import h5netcdf
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import os
from matplotlib import rc
from mpl_toolkits.axes_grid1 import make_axes_locatable
import re
import cartopy.crs as ccrs
import cartopy.util as cutil
import xarray as xr
rc('text', usetex=True)


with h5netcdf.File('idealized_forcing_4deg.nc') as f:
    xt, yt, zt = (np.array(f['xt'][:]), np.array(f['yt'][:]), np.array(f['zt'][:]))
    
    #tau_x
    # tau_x = np.array(f['tau_x'][:])[0,:,0]
    # fig, ax = plt.subplots()
    # plt.plot(yt,tau_x,'black')
    # plt.ylim((-0.1,0.1))
    # ax.xaxis.set_major_locator(plt.MultipleLocator(20))
    # ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("$%d^{\circ}$"))
    # plt.title(r"$\tau_x$")
    # plt.show()

    # SSS, SST
    sss = np.array(f['sss'][:])[0,:,0]
    sst = np.array(f['sst'][:])[0,:,0]

    fig, ax1 = plt.subplots()

    color = 'black'
    ax1.set_xlabel(r'Latitude')
    ax1.set_ylabel('Sea Surface Salinity (SSS)', color=color)
    ax1.yaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax1.plot(yt, sss, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.xaxis.set_major_locator(plt.MultipleLocator(20))
    ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter("$%d^{\circ}$"))

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('Sea Surface Temperature (SST)', color=color)  # we already handled the x-label with ax1
    ax2.yaxis.set_major_locator(plt.MultipleLocator(5))
    ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter("$%d^{\circ}C$"))
    ax2.plot(yt, sst, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.title("SSS and SST")
    #fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


