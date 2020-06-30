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

rundir = '../../actual_runs/runs_4_degree_last/'
time = np.arange(0,70,5)
print(rundir)

time = np.arange(0,70,5)

baths = xr.open_dataset('../notebooks/Data/manual_baths_4deg_final.nc')
originals = [xr.open_dataset('../../map_manipulation/bathymetrys/Originals/TopoBathyc%d.nc' % (t)) for t in time]

xt_o = originals[0]['longitude'].values
yt_o = originals[0]['latitude'].values

Z_o = np.array([f['Z'].values for f in originals])

Z_o[Z_o > -10] = 1
Z_o[Z_o <= -10] = 0

xt = baths['xt'].values
yt = baths['yt'].values

Z = baths['mask'].values
d_Z = baths['bathymetry'].values

#fig, (ax1,ax2) = plt.subplots(2,1,subplot_kw=dict(projection=ccrs.PlateCarree()),gridspec_kw={'height_ratios': [4, 2]},constrained_layout=True)
from matplotlib import gridspec
fig = plt.figure(figsize=[10, 5],facecolor=(.18, .31, .31))
gs = gridspec.GridSpec(2, 1, height_ratios=[6, 1]) 
ax1 = fig.add_subplot(gs[0], projection=ccrs.Robinson(),facecolor=(.18, .31, .31))
ax2 = fig.add_subplot(gs[1])

def add_timeline(ax,valshow):
    timper = [65,50,30,20,5,0]
    periods = ['Eocene','Paleocene','Oligocene','Miocene','Pliocene']
    levels = np.array([1,1,1,1,1,1])
    markerline, stemline, baseline = ax.stem(timper,levels,linefmt="C3-", basefmt="k-",use_line_collection=True)
    vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]

    ax.annotate('Eocene', xy=(60,1), xytext=(3,3),
                    textcoords="offset points", ha="right",size=12)
    ax.annotate('Paleocene', xy=(43,1), xytext=(3,3),
                    textcoords="offset points", ha="right",size=12)
    ax.annotate('Oligocene', xy=(23,1), xytext=(3,3),
                    textcoords="offset points", ha="right",size=12)
    ax.annotate('Miocene', xy=(14,1), xytext=(3,3),
                    textcoords="offset points", ha="right",size=12)
    ax.annotate('Pliocene', xy=(0,1), xytext=(3,3),
                    textcoords="offset points", ha="right",size=12)

    plt.setp(markerline, mec="k", mfc="w", zorder=3)
    markerline.set_ydata(np.zeros(len(timper)))
    ax.get_yaxis().set_visible(False)

    ax.set_xlim(65,0)
    ax.set_ylim(-0.1,1)
    ax.set_xticks(np.arange(0,65.1,5))

    markerline_o, stemline_o, baseline_o = ax.stem([valshow],[1],linefmt="C2-", basefmt="k-",use_line_collection=True)
    plt.setp(markerline_o, mec="k", mfc="g", zorder=3)
    plt.setp(stemline_o,'linewidth', 6)
    markerline_o.set_ydata(np.zeros(len(timper)))
    ax.set_xlabel('Million years ago')


add_timeline(ax2,3)

mask, xtf = cutil.add_cyclic_point(np.roll(Z[13],45,axis=1), coord=xt)
mask_o, xtf_o = cutil.add_cyclic_point(Z_o[13], coord=xt_o)
depth, _ = cutil.add_cyclic_point(np.roll(d_Z[13],45,axis=1), coord=xt)
#ax1.contour(xtf_o,yt_o, mask_o, colors='k')

#ax1.pcolormesh(xtf,yt,mask, cmap='Blues',vmin=0, vmax=2,)
cf = ax1.pcolormesh(xtf,yt, depth, cmap='Blues',vmin=-6000,vmax=0)


def animate(i):
    n= 13-i
    ax1.clear()
    ax2.clear()
    ax1.set_frame_on(False)
    
    mask, xtf = cutil.add_cyclic_point(np.roll(Z[n],45,axis=1), coord=xt)
    depth, _ = cutil.add_cyclic_point(np.roll(d_Z[n],45,axis=1), coord=xt)
    depth[depth >=0] = np.nan
    mask_o, xtf_o = cutil.add_cyclic_point(Z_o[n], coord=xt_o)
    ax1.imshow(np.tile(np.array([[[165, 214, 121]]], 
          dtype=np.uint8), [2, 2, 1]),
      origin='upper',
      transform=ccrs.PlateCarree(),
      extent=[-180, 180, -180, 180])

    ax1.contour(xtf_o,yt_o, mask_o, colors='k', linewidths=0.3, transform=ccrs.PlateCarree())
    #ax1.pcolormesh(xtf,yt,mask, cmap='Blues',vmin=0, vmax=2)
    ax1.pcolormesh(xtf,yt, depth, cmap='Blues',vmin=-6000,vmax=0, transform=ccrs.PlateCarree())
    add_timeline(ax2,time[n])

    
    ax1.set_title('Scaled bathymetry: %s Ma years ago' % time[n])
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.03, 0.7])
fig.colorbar(cf,cax=cbar_ax)
anim = animation.FuncAnimation(fig, animate, frames=14, interval=1000, blit=False)
#plt.show()
Writer = animation.writers['ffmpeg']
writer = Writer(fps=2, metadata=dict(
     artist='Me'), bitrate=1800)
anim.save('bathy_2.gif', dpi=200, writer='imagemagick', savefig_kwargs=dict(facecolor='#f3f3f3'))
for file in originals:
    file.close()
baths.close()
