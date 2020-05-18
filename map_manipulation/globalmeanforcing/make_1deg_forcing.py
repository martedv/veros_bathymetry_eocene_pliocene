import xarray as xr
import h5netcdf
import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image


def resize_array(toresize):
    

    asimg = Image.fromarray(toresize)
    
    _resize = np.array(asimg.resize((90, 40), resample=3))

    return _resize

simplified = h5netcdf.File('simplified_forcings.nc')

yt = np.array(simplified['yt'][:])
xt = np.array(simplified['xt'][:])
zt = np.array(simplified['zt'][:])
simplified.close()
with h5netcdf.File('idealized_forcing_1deg.nc') as f:
    #Q_net
    ddz = np.array([50., 70., 100., 140., 190., 240., 290., 340.,
                        390., 440., 490., 540., 590., 640., 690.])
    zt_1 = np.array(f['zt'][:])
    lower = []
    upper = []

    for i, z in enumerate(zt):
        
        lower = lower + [zt_1.size - np.searchsorted(zt_1[::-1], z - (ddz[i]/2),side='right')]
        upper = upper + [zt_1.size - np.searchsorted(zt_1[::-1], z + (ddz[i]/2),side='right')]
    
    temp = np.array([resize_array(f['temperature'][:][i]) for i in range(0,115)])
    tempscaled = [np.mean(temp[upper[i]:lower[i]],axis=0) for i in range(0,15)]
    tempy = []
    for i, s in enumerate(tempscaled):
        tempy = tempy + [np.transpose([np.append((np.flip(s[:,0][20:40]) + s[:,0][0:20]) / 2,(np.flip(s[:,0][0:20]) + s[:,0][20:40]) / 2)]*90)]
    

    salt = np.array([resize_array(f['salinity'][:][i]) for i in range(0,115)])
    saltscaled = np.array([np.mean(salt[upper[i]:lower[i]],axis=0) for i in range(0,15)])
    salty = []
    for i, s in enumerate(saltscaled):
        salty = salty + [np.transpose([np.append((np.flip(s[:,0][20:40]) + s[:,0][0:20]) / 2,(np.flip(s[:,0][0:20]) + s[:,0][20:40]) / 2)]*90)]
    
    #sst as in paper
    #sss as in paper
    #tau_x profile With analytical
    #salinity
    #temprature
    #tidal_energy
    #wind_energy
    #tau_y = 0
    
    #xt
    #yt
    #zt
    
    q_net_m = [resize_array(f['q_net'][:][i]) for i in range(0,12)]
    q_nec_m = [resize_array(f['dqdt'][:][i]) for i in range(0,12)]
    tau_y_m = np.zeros((12,40,90))
    
    tau_x_m = np.array([resize_array(f['tau_x'][:][i]) for i in range(0,12)])
    taptoe = np.mean(tau_x_m,axis=0)
    new_tau = np.append((np.flip(taptoe[:,0][20:40]) + taptoe[:,0][0:20]) / 2, (np.flip(taptoe[:,0][0:20]) + taptoe[:,0][20:40]) / 2)
    new_tau = np.array([np.transpose(np.array([new_tau] * 90))]*12)
    
    sst_m = np.array([np.transpose([12.5 + 12.5*np.cos(np.pi * yt/80)]*90)]*12)
    
    sst_m = np.array([resize_array(f['sst'][:][i]) for i in range(0,12)])
    sss_m = np.array([resize_array(f['sss'][:][i]) for i in range(0,12)])

    
    new_sss = np.array([np.append((np.flip(y[20:40,:]) + y[0:20,:])/2,(y[20:40,:] + np.flip(y[0:20,:]))/2,axis=0) for y in sss_m])
    
    
    

    with h5netcdf.File('idealized_forcing_4deg.nc', 'w') as oc:
        oc._create_dimension("xt", 90)
        oc._create_dimension("yt", 40)
        oc._create_dimension("zt", 15)
        oc._create_dimension("Time", 12)
        oc.create_variable("xt", ("xt",), data=xt)
        oc.create_variable("yt", ("yt",), data=yt)
        oc.create_variable("zt", ("zt",), data=zt)

        #probly look at q_net
        oc.create_variable("q_net", ("Time","yt","xt",), data=q_net_m)
        oc.create_variable("tau_y", ("Time","yt","xt",), data=tau_y_m)
        oc.create_variable("tau_x", ("Time","yt","xt",), data=new_tau)
        oc.create_variable("sst", ("Time","yt","xt",), data=sst_m)
        oc.create_variable("sss", ("Time","yt","xt",), data=new_sss)
        oc.create_variable("temperature", ("zt","yt","xt",), data=tempscaled)
        oc.create_variable("salinity", ("zt","yt","xt",), data=salty)
        oc.create_variable("q_nec", ("Time","yt","xt",), data=q_nec_m)


# with h5netcdf.File(dirname + '/forcing_1deg_global_interpolated.nc','r') as f:

    
#     #Time yt xt
#     q_net_m = np.transpose([np.mean(f['q_net'][:], axis=2)]*360,(1,2,0))
#     sst_m = np.transpose([np.mean(f['sst'][:], axis=2)]*360,(1,2,0))
#     swf_m = np.transpose([np.mean(f['swf'][:], axis=2)]*360,(1,2,0))
#     sss_m = np.transpose([np.mean(f['sss'][:], axis=2)]*360,(1,2,0))
#     tau_x_m = np.transpose([np.mean(f['tau_x'][:], axis=2)]*360,(1,2,0))
#     tau_y_m = np.transpose([np.mean(f['tau_y'][:], axis=2)]*360,(1,2,0))
#     dqdt_m = np.transpose([np.mean(f['dqdt'][:], axis=2)]*360,(1,2,0))

    

#     #ytxt
#     tidal_energy_m = np.transpose([np.mean(f['tidal_energy'][:], axis=1)]*360)
#     wind_energy_m = np.transpose([np.mean(f['wind_energy'][:], axis=1)]*360)
#     dz_m = f['dz'][:]
#     #ztytxt
#     temperature_m = np.transpose([np.mean(f['temperature'][:], axis=2)]*360,(1,2,0))
#     salinity_m = np.transpose([np.mean(f['salinity'][:], axis=2)]*360,(1,2,0))

    
#     h = np.array(temperature_m).shape

#     with h5netcdf.File(dirname + '/idealized_forcing_1deg.nc', 'w') as oc:
#         oc._create_dimension("xt", 360)
#         oc._create_dimension("yt", 160)
#         oc._create_dimension("zt", 115)
#         oc._create_dimension("Time", 12)

#         oc.create_variable("xt", ("xt",), data=f['xt'][:])
#         oc.create_variable("yt", ("yt",), data=f['yt'][:])
#         oc.create_variable("zt", ("zt",), data=f['zt'][:])
        
#         oc.create_variable("q_net", ("Time","yt","xt",), data=q_net_m)
#         oc.create_variable("sss", ("Time","yt","xt",), data=sss_m)
#         oc.create_variable("sst", ("Time","yt","xt",), data=sst_m)
#         oc.create_variable("swf", ("Time","yt","xt",), data=swf_m)
#         oc.create_variable("dqdt", ("Time","yt","xt",), data=dqdt_m)
#         oc.create_variable("tau_x", ("Time","yt","xt",), data=tau_x_m)
#         oc.create_variable("tau_y", ("Time","yt","xt",), data=tau_y_m)

#         oc.create_variable("tidal_energy", ("yt","xt",), data=tidal_energy_m)
#         oc.create_variable("wind_energy", ("yt","xt",), data=wind_energy_m)

#         oc.create_variable("temperature", ("zt","yt","xt",), data=temperature_m)
#         oc.create_variable("salinity", ("zt","yt","xt",), data=salinity_m)

#         oc.create_variable("dz", ("zt",), data=dz_m)
        
        

