import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.colors as colors
import csv
from matplotlib import rc
import os
import re
import cartopy.crs as ccrs
import xarray as xr
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import animation
import matplotlib.ticker as ticker
import cartopy.util as cutil
from scipy.integrate import quad
rc('text', usetex=True)
pdf = PdfPages("streamfunction_May12.pdf")
dirname = os.path.dirname(__file__)

filesovert = ['Run0/run_0ma.0029.averages.nc',
        'Run5/run_5ma.0029.averages.nc', 'Run10/run_10ma.0029.averages.nc', 'Run15/run_15ma.0029.averages.nc', 'Run20/run_20ma.0029.averages.nc',
        'Run25/run_25ma.0029.averages.nc', 'Run30/run_30ma.0029.averages.nc', 'Run35/run_35ma.0029.averages.nc', 'Run40/run_40ma.0029.averages.nc','Run45/run_45ma.0029.averages.nc',  'Run50/run_50ma.0029.averages.nc', 'Run55/run_55ma.0029.averages.nc', 'Run60/run_60ma.0029.averages.nc', 'Run65/run_65ma.0029.averages.nc']

overt = [xr.open_dataset(dirname + '../actual_runs/runs_4_degree_final_forcing/' + filename) for filename in filesovert]




def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


cmap = plt.get_cmap('bwr')
new_cmap = truncate_colormap(cmap, 0.3, 0.7)

yt = overt[0]['yt'].values
xt = overt[0]['xt'].values


time = [0,5,10,15,20,25,30,35,40,45,50,55,60,65]
 

with xr.open_dataset('manual_baths_4deg_test.nc') as f:
    mask = f['mask'].values
    mask[mask != 1] = np.nan

    for i, t in enumerate(time):
        fig = plt.figure()
        ax = plt.subplot(projection=ccrs.PlateCarree(central_longitude=180))
        xt = overt[0]['xt'].values
        ov = -overt[i]['psi'][0].values
        ov, xt = cutil.add_cyclic_point(ov, coord=xt)
        plt.pcolormesh(xt,yt,ov / 1e6, cmap=new_cmap, vmin=-30, vmax=30, transform=ccrs.PlateCarree())
        plt.colorbar(format="%iSv",fraction=0.025, pad=0.08)
        plt.contour(xt,yt,ov / 1e6, colors='black', vmin=-30, vmax=30, levels=20, transform=ccrs.PlateCarree(),linewidths = 0.5)
        plt.pcolormesh(np.roll(xt,46,axis=0),yt,mask[i], cmap='gray')
        
        plt.title('%dMa'%(t))
        pdf.savefig( fig )
        print('done %s' % (t))
pdf.close()