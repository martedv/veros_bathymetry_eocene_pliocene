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
time = np.arange(0,70,5)

originals = [xr.open_dataset('../map_manipulation/bathymetrys/Originals/TopoBathyc%d.nc' % (t)) for t in time]


xt = originals[0]['longitude'].values
yt = originals[0]['latitude'].values

Z = np.array([f['Z'].values for f in originals])
Z[Z >=-10] = np.nan

fig = plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
ax.background_patch.set_facecolor('black')

cf = ax.pcolormesh(xt,yt,Z[13], transform=ccrs.PlateCarree(), cmap='ocean')
fig.colorbar(cf,format='%im', fraction=0.025, pad=0.04)
def animate(i):
    n= 13-i
    ax.clear()
    cf = ax.pcolormesh(
        xt,yt,Z[i], transform=ccrs.PlateCarree(), cmap='ocean')
    ax.set_title('%s Ma years ago' % time[n])
    ax.background_patch.set_facecolor('black')
    
anim = animation.FuncAnimation(fig, animate, frames=14, interval=800, blit=False)
Writer = animation.writers['ffmpeg']
writer = Writer(fps=2, metadata=dict(
     artist='Me'), bitrate=1800)
anim.save('bathy.gif', dpi=200, writer='imagemagick')

# #plt.show()

# fig = plt.figure()

# ax = plt.axes(projection=ccrs.PlateCarree(
#                             central_longitude=180))
# ax.background_patch.set_facecolor('black')

# cf = ax.pcolormesh(xt, yt, psidata[13], vmin=-70e6, vmax=70e6, transform=ccrs.PlateCarree(), cmap='RdBu')

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

# plt.show()
for file in originals:
    file.close()