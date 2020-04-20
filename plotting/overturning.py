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
filesavg = ['Run0/4deg-0ma-200y.overturning.nc']

overt = [xr.open_dataset(dirname + '../actual_runs/runs_4_degree/' + s) for s in filesavg]

print(overt[0])