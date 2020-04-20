
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
def calctf(time, long, minlat, maxlat):
    zonalu = averages[time]['u'][199]

    def area(z0, z1, lat0, lat1):
        torad = np.pi/180.0
        rad0 = lat0*torad
        rad1 = lat1*torad

        # integrate from lat0 to lat1 (in radians)

        # integrate from r0 to r1 *r

        return quad(lambda r: r*(rad0 - rad1), z0, z1)

    zonarr = zonalu[:,minlat:maxlat,long]


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
    
    
    return np.sum(throughflow[~np.isnan(zonarr).values])

def showSelectedCells(time, long, minlat,maxlat):
    sel = averages[time]['u'][199]
    mapped = ~np.isnan(sel[14,:,:])
    cmape = np.zeros(mapped.shape) + 1
    cmape[mapped] = 0

    cmape[ minlat:maxlat, long] = 5
    plt.pcolor(cmape)
    plt.show()


t = [0,5,20,40,65]

showSelectedCells(4,35,4,11)

# Probably one of Tasman passage

#flow Under Australia
parr = np.array([calctf(0,35,4,11),calctf(1,35,4,11), calctf(2,35,4,11), 0,0])
plt.plot(t, parr / (10**6), label="Tasman Passage")


#Indonesian passage
parr = np.array([0,0, calctf(2,30,18,21), calctf(3,30,16,22), calctf(4,31,14,20)])
plt.plot(t, parr / (10**6), label="Indonesian Passage")

#Drake passage
tfarr = np.array([calctf(0,72,2,7), calctf(1,72,2,7),calctf(2,72,2,7), calctf(3,73,1,6), calctf(4,72,4,6)])
plt.plot(t, tfarr / (10**6), label="Drake Passage")

#Panama passage
parr = np.array([0,0, calctf(2,71,20,24), calctf(3,73,20,24), calctf(4,75,20,24)])
plt.plot(t, parr / (10**6), label="Pannema Passage")

plt.xlim(65,0)
plt.legend()
plt.xlabel('Years ago')
plt.ylabel('Sverdrups (Sv)')
plt.show()