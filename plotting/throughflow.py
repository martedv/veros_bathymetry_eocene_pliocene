
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
from scipy.integrate import quad

dirname = os.path.dirname(__file__)
filesavg = ['Run0/4deg-0ma-200y.averages.nc',
        'Run5/4deg-5ma-200y.averages.nc', 'Run20/4deg-20ma-200y.averages.nc', 'Run40/4deg-40ma-200y.averages.nc','Run65/4deg-65ma-200y.averages.nc']

averages = [xr.open_dataset(dirname + '../actual_runs/runs_4_degree/' + s) for s in filesavg]

xt = averages[0]['xt']
yt = averages[0]['yt']
zt = averages[0]['zt']
def calctf(time, loc):
    zonalu = averages[time]['u'][199]

    def area(z0, z1, lat0, lat1):
        torad = np.pi/180.0
        rad0 = lat0*torad
        rad1 = lat1*torad

        # integrate from lat0 to lat1 (in radians)

        # integrate from r0 to r1 *r

        return quad(lambda r: r*(rad0 - rad1), z0, z1)

    zonarr = zonalu[:,:10,-18]


    radearth = 6371000

    areaarr = np.zeros(zonarr.shape)

    throughflow = np.zeros(zonarr.shape)

    maxz = 0
    for zi, z in enumerate(zonarr):
        for yi, y in enumerate(z):
            if zi == 14:
                maxz = radearth
            else:
                maxz = radearth + zt[zi+1]

            areaarr[zi,yi], _ = area(radearth + zt[zi], maxz, 4,0)
            throughflow[zi,yi] = areaarr[zi,yi] * y
    plt.contourf(throughflow)
    plt.show()
    
    return np.sum(throughflow[~np.isnan(zonarr).values])
l = [(0,72),(1,72),(2,73),(3,74),(4,75)]
tfarr = [calctf(i,j) for i,j in l]

t = [0,5,20,40,65]

plt.plot(t, tfarr)
plt.show()