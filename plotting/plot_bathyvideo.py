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
time = np.arange(0,70,5)

baths = xr.open_dataset('notebooks/Data/manual_baths_4deg_final.nc')
originals = [xr.open_dataset('../map_manipulation/bathymetrys/Originals/TopoBathyc%d.nc' % (t)) for t in time]

xt_o = originals[0]['longitude'].values
yt_o = originals[0]['latitude'].values

Z_o = np.array([f['Z'].values for f in originals])

Z_o[Z_o > -10] = 1
Z_o[Z_o <= -10] = 0

xt = baths['xt'].values
yt = baths['yt'].values

Z = baths['mask'].values
d_Z = baths['bathymetry'].values


fig = plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))



mask, xtf = cutil.add_cyclic_point(np.roll(Z[13],45,axis=1), coord=xt)
mask_o, xtf_o = cutil.add_cyclic_point(Z_o[13], coord=xt_o)
depth, _ = cutil.add_cyclic_point(np.roll(d_Z[13],45,axis=1), coord=xt)
ax.contour(xtf_o,yt_o, mask_o, colors='k')

ax.pcolormesh(xtf,yt,mask, cmap='Blues',vmin=0, vmax=2,)
cf = ax.pcolormesh(xtf,yt, depth, cmap='ocean',vmin=-5000,vmax=0)

fig.colorbar(cf,format='%im', fraction=0.025, pad=0.04)
def animate(i):
    n= 13-i
    ax.clear()
    mask, xtf = cutil.add_cyclic_point(np.roll(Z[n],45,axis=1), coord=xt)
    depth, _ = cutil.add_cyclic_point(np.roll(d_Z[n],45,axis=1), coord=xt)
    mask_o, xtf_o = cutil.add_cyclic_point(Z_o[n], coord=xt_o)
    ax.contour(xtf_o,yt_o, mask_o, colors='k', linewidths=0.5)
    ax.pcolormesh(xtf,yt,mask, cmap='Blues',vmin=0, vmax=2)
    ax.pcolormesh(xtf,yt, depth, cmap='ocean',vmin=-5000,vmax=0)

    ax.set_title('Scaled bathymetry: %s Ma years ago' % time[n])

anim = animation.FuncAnimation(fig, animate, frames=14, interval=800, blit=False)
Writer = animation.writers['ffmpeg']
writer = Writer(fps=2, metadata=dict(
     artist='Me'), bitrate=1800)
anim.save('bathy_2.gif', dpi=200, writer='imagemagick')
for file in originals:
    file.close()
baths.close()