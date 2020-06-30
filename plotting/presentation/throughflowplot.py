import h5netcdf
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
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
from scipy.integrate import quad
import matplotlib.colors as mcolors
import matplotlib.backends.backend_pdf
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Computer Modern Roman'],'size'   : 9})
rc('text', usetex=True)
import matplotlib.backends.backend_pdf

time = np.arange(0,70,5)
print(time)
rundir = '../../veros_setup/runs_4_degree_last/'

yearsdone = []
ranfory = []
xt = []
yt = []
zt = [] 

xu = []
yu = []
dzt = []
dyt = []
dxt = []
dyu = []

BSF = []
u = []
area_u = []
v = []
area_v = []

for year in time:
    if os.path.exists(rundir + 'Run%i/run_%ima.current_run' % (year,year)):
        with open(rundir + 'Run%i/run_%ima.current_run' % (year,year)) as f:
            ranfor = int(f.readline())
        ranfory.append(ranfor)
        yearsdone.append(year)
        with xr.open_dataset(rundir + 'Run%i/run_%ima.%04d.averages.nc'% (year,year,ranfor -1)) as ds:
            BSF.append(ds['psi'][0].values)
            u.append(ds['u'].values) 
            v.append(ds['v'].values)
            if xt == []:
                xt = ds['xt'].values
                yt = ds['yt'].values
                zt = ds['zt'].values
                xu = ds['xu'].values
                yu = ds['yu'].values
        with xr.open_dataset(rundir + 'Run%i/run_%ima.%04d.snapshot.nc'% (year,year,ranfor -1)) as ds:
            area_u.append(ds['area_u'].values)
            area_v.append(ds['area_v'].values)
            if dzt == []:
                dzt = ds['dzt'].values
                dyt = ds['dyt'].values
                dxt = ds['dxt'].values
                dyu = ds['dyu'].values

radearth = 6371000
torad = np.pi/180.0

dzts = np.flip(radearth - np.append(0,np.cumsum(dzt[::-1])))
print(dzts)
zy_area = -np.repeat([[quad(lambda r: r*(4)*torad, dzts[i], dzts[i+1])[0] for i in range(dzt.shape[0])]],repeats=40, axis=0)


# zx area

area = np.array(area_u)[-1]
dxt_array = np.array([a / dyt[0]  for i, a in enumerate(area)])
dxt_array = np.array([np.nanmax(a) for a in dxt_array])/radearth


zx_area =-np.array([[quad(lambda r: r*theta*torad, dzts[i], dzts[i+1])[0] for i in range(dzt.shape[0])] for theta in dxt_array])
names = ['Tasman', 'Indonesian', 'Drake', 'Panama','Thetys','Aghulas']
values = [
    [('x',80,2,10),('x',74, 13, 19),('x', 26,1,6), 0, 0,('x', 49,1,18)], # 0Ma
    [('x',81,2,9),('x',73, 13, 19),('x',27,2,6), 0, 0,('x', 49,1,18)], # 5 Ma
    [('x',81,3,9),('x',74, 14, 20),('x',27,2,6), ('x',  28, 18,30), 0,('x', 49,1,18)], # 10 Ma open panama
    [('x',81,3,9),('x',74, 13, 18),('x',27,2,6), ('x',  25, 18,27), 0,('x', 50,1,18)], # 15 Ma open panama
    [('x',81,3,9),('x',74, 14, 20),('x',28,2,6), ('x',  27, 20,27), ('x',43,20,30),('x', 50,1,18)], # 20 Ma 
    [('x',81,3,9),('x',74, 10, 20),('x',27,2,6), ('x',  26, 18,27), ('x',43,20,30),('x', 49,1,18)], # 25 Ma 
    [('x',81,3,9),('x',74, 10, 19),('x',28,2,6), ('x',  27, 19,27), ('x',44,20,30),('x', 49,1,18)], # 30 Ma
    [('x',81,3,9),('x',73, 10, 21),0, ('x',  27, 19,27), ('x',45,20,30),('x', 50,1,18)], # 35 Ma drake closure
    [0,('x',74, 11, 20),0, ('x',  28, 19,27), ('x',46,20,30),('x', 49,0,18)], # 40 Ma Tasman closure
    [0,('x',75, 12, 20),0, ('x',  29,19,27), ('x',46,20,30),('x', 49,0,18)], # 45 Ma
    [0,('x',75, 11, 20),0, ('x',  29, 18,27), ('x',46,20,30),('x', 49,0,18)], # 50 Ma
    [0,('x',76, 11, 20),0, ('x',  30, 18,26), ('x',45,20,30),('x', 49,0,18)], # 55 Ma
    [0,('x',76, 10, 19),0, ('x',  31, 19,27), ('x',48,20,30),('x', 49,0,18)], # 60 Ma
    [0,('x',76, 10, 20),0, ('x',  31, 20,27), ('x',45,20,30),('x', 49,0,18)], # 65 Ma
]

year = 4
bs = BSF[year]
print(bs.shape)
bath = np.zeros((40,90))

def showBathycells(time, long, minlat,maxlat):
    bath[ minlat:maxlat, long] = 5
def showBathycells_Y(time, lat, minlong,maxlong):
    bath[ lat,  minlong:maxlong] = 5

for t in values[year]:
    if type(t) is tuple:
        if t[0] == 'y':
            showBathycells_Y(year,t[1],t[2],t[3])
        else:
            showBathycells(year,t[1],t[2],t[3])

tf_values = np.zeros(np.shape(values))
import matplotlib as mpl
for y, year in enumerate(values):
    for p, passage in enumerate(year):
        if not isinstance(passage,tuple):
            continue
        tf_values[y,p] = np.nansum(-BSF[y][passage[2]:passage[3],passage[1]]) /1e6
fig=plt.figure()

mpl.rcParams['savefig.facecolor'] = 'blue' 
fig.patch.set_alpha(0)
plottypes = ['o--','v--','^--','s--','X--','d--']
for i,tf_val in enumerate(np.transpose(tf_values)):
    plt.plot(time[::-1],tf_val[::-1],plottypes[i],label=names[i])
plt.legend()
#plt.title(r"Volumetransport in Sverdrups")
plt.xlabel(r"Ma years ago")
plt.ylabel(r"Sv")
plt.xlim(65,0)
plt.xticks([65,60,50,40,30,20,10,0])
plt.grid()
#plt.savefig("../figures/throughflow_bsf.jpg",dpi=400,facecolor=fig.get_facecolor())
plt.show()