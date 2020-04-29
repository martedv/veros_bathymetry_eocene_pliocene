
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import os
from matplotlib import rc
import re
import cartopy.crs as ccrs
import xarray as xr
from matplotlib import animation
from scipy.integrate import quad
rc('text', usetex=True)
dirname = os.path.dirname(__file__)
filesavg = ['Run0/4deg-0ma-200y.averages.nc',
        'Run5/4deg-5ma-200y.averages.nc', 'Run10/4deg-10ma-200y.averages.nc', 'Run15/4deg-15ma-200y.averages.nc', 'Run20/4deg-20ma-200y.averages.nc',
        'Run25/4deg-25ma-200y.averages.nc', 'Run30/4deg-30ma-200y.averages.nc', 'Run35/4deg-35ma-200y.averages.nc', 'Run40/4deg-40ma-200y.averages.nc', 
        'Run45/4deg-45ma-200y.averages.nc', 'Run50/4deg-50ma-200y.averages.nc', 'Run55/4deg-55ma-200y.averages.nc', 'Run60/4deg-60ma-200y.averages.nc','Run65/4deg-65ma-200y.averages.nc']

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


t = [0,5,10,15,20,25,30,35,40,45,50,55,60,65]

# Probably one of Tasman passage

# #flow Under Australia
# parr = np.array([calctf(0,35,4,11),calctf(1,35,4,11),calctf(2,35,4,11), calctf(3,35,4,11),calctf(4,35,4,11),calctf(5,35,4,11),calctf(6,35,4,11),calctf(7,35,4,11),calctf(8,35,4,11),0,0,0,0,0])
# plt.plot(t, parr / (10**6), label="Tasman Passage")


# # #Indonesian passage
parr = np.array([calctf(0,29,16,20),0, calctf(2,29,16,21), calctf(3,29,16,21), calctf(4,30,16,21), calctf(5,29,15,21),calctf(6,29,14,21),calctf(7,29,14,21),calctf(8,30,16,22),calctf(9,30,17,21),calctf(10,30,16,21), calctf(11,31,16,21),
 calctf(12,31,15,21), calctf(13,31,15,21)])
plt.plot(t, parr / (10**6), label="Indonesian Passage")

# # #Drake passage
# tfarr = np.array([calctf(0,72,2,7),calctf(1,72,2,7), calctf(2,72,2,7), calctf(3,72,2,7), calctf(4,72,2,7), calctf(5,73,2,5),calctf(6,73,2,5),calctf(7,73,2,5),calctf(8,73,3,4),calctf(9,73,3,4),calctf(10,71,3,4), calctf(11,72,4,5),
#   calctf(12,72,4,5), calctf(13,72,4,5)])
# plt.plot(t, tfarr / (10**6), label="Drake Passage")

#Panama passage
parr = np.array([0,0, calctf(2,71,20,24), calctf(3,69,21,22), calctf(4,72,22,23), 0, calctf(6,71,20,21), calctf(7,71,20,21),
 calctf(8,71,19,21),calctf(9,71,18,21),calctf(10,71,18,23),calctf(11,72,18,24),calctf(12,72,19,24),calctf(13,73,19,24),])
plt.plot(t, parr / (10**6), label="Pannema Passage")

plt.xlim(65,0)
plt.legend()
plt.grid()
plt.xlabel('Years ago (Ma)')
plt.ylabel('Sverdrups (Sv)')
plt.show()