import h5netcdf
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import os
import re
import cartopy.crs as ccrs
import xarray as xr
from matplotlib import animation

dirname = os.path.dirname(__file__)

filesavg = ['Run0/4deg-0ma-200y.averages.nc',
        'Run5/4deg-5ma-200y.averages.nc', 'Run10/4deg-10ma-200y.averages.nc', 'Run15/4deg-15ma-200y.averages.nc', 'Run20/4deg-20ma-200y.averages.nc',
        'Run25/4deg-25ma-200y.averages.nc', 'Run30/4deg-30ma-200y.averages.nc', 'Run35/4deg-35ma-200y.averages.nc', 'Run40/4deg-40ma-200y.averages.nc', 
        'Run45/4deg-45ma-200y.averages.nc', 'Run50/4deg-50ma-200y.averages.nc', 'Run55/4deg-55ma-200y.averages.nc', 'Run60/4deg-60ma-200y.averages.nc','Run65/4deg-65ma-200y.averages.nc']

filesovert = ['Run0/4deg-0ma-200y.overturning.nc',
        'Run5/4deg-5ma-200y.overturning.nc', 'Run10/4deg-10ma-200y.overturning.nc', 'Run15/4deg-15ma-200y.overturning.nc', 'Run20/4deg-20ma-200y.overturning.nc',
        'Run25/4deg-25ma-200y.overturning.nc', 'Run30/4deg-30ma-200y.overturning.nc', 'Run35/4deg-35ma-200y.overturning.nc', 'Run40/4deg-40ma-200y.overturning.nc', 
        'Run45/4deg-45ma-200y.overturning.nc', 'Run50/4deg-50ma-200y.overturning.nc', 'Run55/4deg-55ma-200y.overturning.nc', 'Run60/4deg-60ma-200y.overturning.nc','Run65/4deg-65ma-200y.overturning.nc']
timeAgo = np.arange(0,70,5)


averagesdata = [xr.open_dataset(dirname + '../actual_runs/runs_4_degree/' + filename) for filename in filesavg]
overturningdata = [xr.open_dataset(dirname + '../actual_runs/runs_4_degree/' + filename) for filename in filesovert]




zt = averagesdata[0]['zt'][:]
xt = averagesdata[0]['xt'][:]
yt = averagesdata[0]['yt'][:]



def transport(bdepth = 9, bypos = 6):
    bolus_data = [f['bolus_iso'][199][bdepth][bypos] for f in overturningdata]
    fig, ax = plt.subplots()

    scale_y = 1e6
    ticks_y = ticker.FuncFormatter(lambda y, pos: '{0:g}'.format(y/scale_y))
    ax.yaxis.set_major_formatter(ticks_y)


    ax.plot(timeAgo, bolus_data)
    ax.set_xlim(65, 0)
    ax.set(xlabel='time (Ma)', ylabel='strength (10^6 m^3 / s)',title="Meridional transport at z=%sm y=%sdeg" % (zt[bdepth],yt[bypos]))
    ax.grid()
    plt.show()




def streamfunc():
    psidata = np.array([f['psi'][199] for f in averagesdata])

    psidata[psidata < -1e17] = np.nan
    fig = plt.figure()

    ax = plt.axes(projection=ccrs.PlateCarree(
                                central_longitude=180))
    ax.background_patch.set_facecolor('black')

    cf = ax.pcolormesh(xt, yt, psidata[13], vmin=-70e6, vmax=70e6, transform=ccrs.PlateCarree(), cmap='RdBu')

    shapearr = [-250, -80, -50, 90]
    ax.set_extent(shapearr, crs=ccrs.PlateCarree())
    def animate(i):
        n= 13-i
        ax.clear()
        cf = ax.pcolormesh(
            xt, yt, psidata[n], vmin=-15e6, vmax=15e6, transform=ccrs.PlateCarree(), cmap='RdBu')
        ax.set_extent(shapearr, crs=ccrs.PlateCarree())
        ax.set_title('%s Ma years ago' % timeAgo[n])
        ax.background_patch.set_facecolor('black')

def vsfdepth():
    vsfdh= np.array([f['vsf_depth'][199] for f in overturningdata])
    plt.contourf(vsfdh[0])
    plt.show()

    # fig = plt.figure()
    # ax = plt.axes()
    # cf = ax.pcolormesh(xt, yt, vsfdh[13], vmin=-70e6, vmax=70e6, transform=ccrs.PlateCarree(), cmap='RdBu')

    # shapearr = [-250, -80, -50, 90]
    # ax.set_extent(shapearr, crs=ccrs.PlateCarree())
    # def animate(i):
    #     n= 13-i
    #     ax.clear()
    #     cf = ax.pcolormesh(
    #         xt, yt, psidata[n], vmin=-15e6, vmax=15e6, transform=ccrs.PlateCarree(), cmap='RdBu')
    #     ax.set_extent(shapearr, crs=ccrs.PlateCarree())
    #     ax.set_title('%s Ma years ago' % timeAgo[n])
    #     ax.background_patch.set_facecolor('black')


    # anim = animation.FuncAnimation(fig, animate, frames=14, interval=100, blit=False)
    # Writer = animation.writers['ffmpeg']
    # writer = Writer(fps=2, metadata=dict(
    #     artist='Me'), bitrate=1800)
    # anim.save('Plots/iso_change.mp4', writer=writer)

    plt.show()

vsfdepth()

for file in averagesdata:
    file.close()
for file in overturningdata:
    file.close()