import xarray as xr
import h5netcdf
import numpy as np
import os
import matplotlib.pyplot as plt

dirname = os.path.dirname(__file__)



with h5netcdf.File(dirname + '/forcing_1deg_global_interpolated.nc','r') as f:

    
    #Time yt xt
    q_net_m = np.transpose([np.mean(f['q_net'][:], axis=2)]*360,(1,2,0))
    sst_m = np.transpose([np.mean(f['sst'][:], axis=2)]*360,(1,2,0))
    swf_m = np.transpose([np.mean(f['swf'][:], axis=2)]*360,(1,2,0))
    sss_m = np.transpose([np.mean(f['sss'][:], axis=2)]*360,(1,2,0))
    tau_x_m = np.transpose([np.mean(f['tau_x'][:], axis=2)]*360,(1,2,0))
    tau_y_m = np.transpose([np.mean(f['tau_y'][:], axis=2)]*360,(1,2,0))
    dqdt_m = np.transpose([np.mean(f['dqdt'][:], axis=2)]*360,(1,2,0))

    

    #ytxt
    tidal_energy_m = np.transpose([np.mean(f['tidal_energy'][:], axis=1)]*360)
    wind_energy_m = np.transpose([np.mean(f['wind_energy'][:], axis=1)]*360)
    dz_m = f['dz'][:]
    #ztytxt
    temperature_m = np.transpose([np.mean(f['temperature'][:], axis=2)]*360,(1,2,0))
    salinity_m = np.transpose([np.mean(f['salinity'][:], axis=2)]*360,(1,2,0))

    
    h = np.array(temperature_m).shape

    with h5netcdf.File(dirname + '/idealized_forcing_1deg.nc', 'w') as oc:
        oc._create_dimension("xt", 360)
        oc._create_dimension("yt", 160)
        oc._create_dimension("zt", 115)
        oc._create_dimension("Time", 12)

        oc.create_variable("xt", ("xt",), data=f['xt'][:])
        oc.create_variable("yt", ("yt",), data=f['yt'][:])
        oc.create_variable("zt", ("zt",), data=f['zt'][:])
        
        oc.create_variable("q_net", ("Time","yt","xt",), data=q_net_m)
        oc.create_variable("sss", ("Time","yt","xt",), data=sss_m)
        oc.create_variable("sst", ("Time","yt","xt",), data=sst_m)
        oc.create_variable("swf", ("Time","yt","xt",), data=swf_m)
        oc.create_variable("dqdt", ("Time","yt","xt",), data=dqdt_m)
        oc.create_variable("tau_x", ("Time","yt","xt",), data=tau_x_m)
        oc.create_variable("tau_y", ("Time","yt","xt",), data=tau_y_m)

        oc.create_variable("tidal_energy", ("yt","xt",), data=tidal_energy_m)
        oc.create_variable("wind_energy", ("yt","xt",), data=wind_energy_m)

        oc.create_variable("temperature", ("zt","yt","xt",), data=temperature_m)
        oc.create_variable("salinity", ("zt","yt","xt",), data=salinity_m)

        oc.create_variable("dz", ("zt",), data=dz_m)
        
        

