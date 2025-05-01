"""
File used to run PAMTRA radiative transfer model on randomly selected points from a NWP.

"""

from __future__ import division # defines natural divisions like 1./2. = 1/2 = 0.5 and not 1/2 = 0
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import pyPamtra  # import pyPamtra
import numpy as np # import numpy for arrays, numerical array operations, ....
import netCDF4 as nc
import sys



NWP_data_path = "/NWP/data/path"
random_file_path = "/random/selection/path"
output_file_path = "/intermediate/file/path"

### ----------------------------------------------------------
# Get user input
mode = sys.argv[1] # Mode describes how rimed the ice particles are and is either "Normal", "High", or "Low", more details in Ephraim et al 2025
month = int(sys.argv[2]) # Month of the NWP file
day = int(sys.argv[3]) # Day of the NWP file
hour = int(sys.argv[4]) # Hour of the NWP file
begin = int(sys.argv[5]) # Which row of the netCDF to start at (0 unless you have already partially completed a row)
end = int(sys.argv[6]) # Which row of the netCDF to end at (Nrows unless you want to split a run into several smaller runs)


### ----------------------------------------------------------
# Descriptor files prescribe the size distributions of different hydrometeor classes. More details provided here: https://pamtra.readthedocs.io/en/latest/descriptorFile.html

# Normal Rime
# Uses riming factor of 0.2 for swc and 0.7 for gwc (Mason et al 2018)
# Matches parameters in Table 1 of Ephraim et al 2018
descriptorFile = np.array([
        #['hydro_name' 'as_ratio' 'liq_ice' 'rho_ms' 'a_ms' 'b_ms' 'alpha_as' 'beta_as' 'moment_in' 'nbin' 'dist_name' 'p_1' 'p_2' 'p_3' 'p_4' 'd_1' 'd_2' 'scat_name' 'vel_size_mod' 'canting']
        ('cwc_q', 1.0,  1, -99.0,   -99.0, -99.0,  -99.0, -99.0, 23, 20, 'mgamma', -99.0, -99.0,   9.6,    1.0,   2.0e-6,   8.0e-5, 'mie-sphere', 'corPowerLaw_24388657.6_2.0', -99.0),
        ('iwc_q', 1.0, -1, -99.0, 1.58783,  2.56,  0.684,   2.0, 23, 20, 'mgamma', -99.0, -99.0, 1.564, 0.8547, 1.744e-5, 9.369e-3, 'ssrg-rt3',   'corPowerLaw_30.606_0.5533',  -99.0),
        ('swc_q', 0.6, -1, -99.0,   0.0908,   2.12, 0.0878,  1.774, 23, 20, 'mgamma', -99.0, -99.0,   -1.0,    1.0,  5.13e-5, 2.294e-2, 'ssrg-rt3',   'corPowerLaw_5.511054_0.25',  -99.0),
        ('gwc_q', 1.0, -1, -99.0,  14.01,  2.67,  -99.0, -99.0, 3, 20, 'mgamma', -99.0, 0.7e-3,  5.0,   1.0,  2.11e-4,   1.3e-2, 'mie-sphere', 'corPowerLaw_406.67_0.85',    -99.0),
        ('rwc_q', 1.0,  1, -99.0,   -99.0, -99.0,  -99.0, -99.0, 13, 20, 'mgamma', -99.0, -99.0,   2.0,    1.0,  0.00012,   8.2e-3, 'mie-sphere', 'corPowerLaw_494.74_0.7031',  -99.0)],
        dtype=[('hydro_name', 'S15'), ('as_ratio', '<f8'), ('liq_ice', '<i8'), ('rho_ms', '<f8'), ('a_ms', '<f8'), ('b_ms', '<f8'), ('alpha_as', '<f8'), ('beta_as', '<f8'), ('moment_in', '<i8'), ('nbin', '<i8'), ('dist_name', 'S15'), ('p_1', '<f8'), ('p_2', '<f8'), ('p_3', '<f8'), ('p_4', '<f8'), ('d_1', '<f8'), ('d_2', '<f8'), ('scat_name', 'S20'), ('vel_size_mod', 'S30'), ('canting', '<f8')] 
        )

# High Rime
# Uses riming factor of 0.3 for swc and 0.8 for gwc (Mason et al 2018)
if mode == "High":
    descriptorFile = np.array([
        #['hydro_name' 'as_ratio' 'liq_ice' 'rho_ms' 'a_ms' 'b_ms' 'alpha_as' 'beta_as' 'moment_in' 'nbin' 'dist_name' 'p_1' 'p_2' 'p_3' 'p_4' 'd_1' 'd_2' 'scat_name' 'vel_size_mod' 'canting']
        ('cwc_q', 1.0,  1, -99.0,   -99.0, -99.0,  -99.0, -99.0, 23, 20, 'mgamma', -99.0, -99.0,   9.6,    1.0,   2.0e-6,   8.0e-5, 'mie-sphere', 'corPowerLaw_24388657.6_2.0', -99.0),
        ('iwc_q', 1.0, -1, -99.0, 1.58783,  2.56,  0.684,   2.0, 23, 20, 'mgamma', -99.0, -99.0, 1.564, 0.8547, 1.744e-5, 9.369e-3, 'ssrg-rt3',   'corPowerLaw_30.606_0.5533',  -99.0),
        ('swc_q', 0.6, -1, -99.0,   0.2488,   2.23, 0.182,  1.850, 23, 20, 'mgamma', -99.0, -99.0,   -1.0,    1.0,  5.13e-5, 2.294e-2, 'ssrg-rt3',   'corPowerLaw_5.511054_0.25',  -99.0),
        ('gwc_q', 1.0, -1, -99.0,  38.38,  2.78,  -99.0, -99.0, 3, 20, 'mgamma', -99.0, 0.7e-3,  5.0,   1.0,  2.11e-4,   1.3e-2, 'mie-sphere', 'corPowerLaw_406.67_0.85',    -99.0),
        ('rwc_q', 1.0,  1, -99.0,   -99.0, -99.0,  -99.0, -99.0, 13, 20, 'mgamma', -99.0, -99.0,   2.0,    1.0,  0.00012,   8.2e-3, 'mie-sphere', 'corPowerLaw_494.74_0.7031',  -99.0)],
        dtype=[('hydro_name', 'S15'), ('as_ratio', '<f8'), ('liq_ice', '<i8'), ('rho_ms', '<f8'), ('a_ms', '<f8'), ('b_ms', '<f8'), ('alpha_as', '<f8'), ('beta_as', '<f8'), ('moment_in', '<i8'), ('nbin', '<i8'), ('dist_name', 'S15'), ('p_1', '<f8'), ('p_2', '<f8'), ('p_3', '<f8'), ('p_4', '<f8'), ('d_1', '<f8'), ('d_2', '<f8'), ('scat_name', 'S20'), ('vel_size_mod', 'S30'), ('canting', '<f8')] 
        )

# Low Rime
# Uses riming factor of 0.1 for swc and 0.6 for gwc (Mason et al 2018)
if mode == "Low":
    descriptorFile = np.array([
        #['hydro_name' 'as_ratio' 'liq_ice' 'rho_ms' 'a_ms' 'b_ms' 'alpha_as' 'beta_as' 'moment_in' 'nbin' 'dist_name' 'p_1' 'p_2' 'p_3' 'p_4' 'd_1' 'd_2' 'scat_name' 'vel_size_mod' 'canting']
        ('cwc_q', 1.0,  1, -99.0,   -99.0, -99.0,  -99.0, -99.0, 23, 20, 'mgamma', -99.0, -99.0,   9.6,    1.0,   2.0e-6,   8.0e-5, 'mie-sphere', 'corPowerLaw_24388657.6_2.0', -99.0),
        ('iwc_q', 1.0, -1, -99.0, 1.58783,  2.56,  0.684,   2.0, 23, 20, 'mgamma', -99.0, -99.0, 1.564, 0.8547, 1.744e-5, 9.369e-3, 'ssrg-rt3',   'corPowerLaw_30.606_0.5533',  -99.0),
        ('swc_q', 0.6, -1, -99.0,   0.0332,   2.01, 0.0423,  1.699, 23, 20, 'mgamma', -99.0, -99.0,   -1.0,    1.0,  5.13e-5, 2.294e-2, 'ssrg-rt3',   'corPowerLaw_5.511054_0.25',  -99.0),
        ('gwc_q', 1.0, -1, -99.0,  5.114,  2.56,  -99.0, -99.0, 3, 20, 'mgamma', -99.0, 0.7e-3,  5.0,   1.0,  2.11e-4,   1.3e-2, 'mie-sphere', 'corPowerLaw_406.67_0.85',    -99.0),
        ('rwc_q', 1.0,  1, -99.0,   -99.0, -99.0,  -99.0, -99.0, 13, 20, 'mgamma', -99.0, -99.0,   2.0,    1.0,  0.00012,   8.2e-3, 'mie-sphere', 'corPowerLaw_494.74_0.7031',  -99.0)],
        dtype=[('hydro_name', 'S15'), ('as_ratio', '<f8'), ('liq_ice', '<i8'), ('rho_ms', '<f8'), ('a_ms', '<f8'), ('b_ms', '<f8'), ('alpha_as', '<f8'), ('beta_as', '<f8'), ('moment_in', '<i8'), ('nbin', '<i8'), ('dist_name', 'S15'), ('p_1', '<f8'), ('p_2', '<f8'), ('p_3', '<f8'), ('p_4', '<f8'), ('d_1', '<f8'), ('d_2', '<f8'), ('scat_name', 'S20'), ('vel_size_mod', 'S30'), ('canting', '<f8')] 
        )

### ----------------------------------------------------------------
# Read in NWP file. In our case, different outputs are split across different output files
fCloud = NWP_data_path+'wrfout_cloud_d02_2020-' + str(month).zfill(2) + '-' + str(day).zfill(2) +'_' + str(hour).zfill(2) + '_00_00'
fWind = NWP_data_path+'wrfout_wind_d02_2020-' + str(month).zfill(2) + '-' + str(day).zfill(2) +'_' + str(hour).zfill(2) + '_00_00'
fRad = NWP_data_path+'wrfout_rad_d02_2020-' + str(month).zfill(2) + '-' + str(day).zfill(2) +'_' + str(hour).zfill(2) + '_00_00'

### ----------------------------------------------------------------
# Read in randomly selected points
f = nc.Dataset(random_file_path+'randomSelect'+str(month)+'-'+str(day)+'.nc')
selected = f['select'][:]


# Define GVR frequencies
freqs = np.array([183.31-14,183.31-7,183.31-3,183.31-1,183.31,183.31+1,183.31+3,183.31+7,183.31+14])

# Number of rows to simulate at a time
interval = 5

### ----------------------------------------------------------------
# Loop that iterates through all rows of NWP (starting from "begin" and until "end" and does a radiative transfer simulation on "interval" rows at a time
for i in np.arange(begin,min(selected.shape[0],end),interval):

    # Function located in $HOME/lib/python/pyPamtra/importer.py that extracts neccesary info from NWP and transforms it into a data structure PAMTRA can use 
    pam = pyPamtra.importer.readWrfCOMBLERandom3D(fWind, fCloud, descriptorFile,i,i+interval)
    
    # First we want to run the passive radiative transfer simulation
    pam.nmlSet['passive'] = True
    pam.nmlSet['active'] = False

    # Function located in $HOME/lib/python/pyPamtra/core.py that runs PAMTRA simulation for all randomly selected points
    pam.runParallelPamtraRandom(freqs,selected[i:i+interval,:],pp_deltaX=1,pp_deltaY=1,pp_deltaF=1,pp_local_workers="auto")

    # Save frequencies used for output netCDF
    freqs_out = freqs

    # Save brightness temperatures for all x coordinates, all y coordinates, all but the upper most (6000 m) height level, only upward looking, and average both polarizations
    tb_out = pam.r["tb"][:,:,1:,31,:].mean(axis=-1)
    # Set any invalid TB to nan
    tb_out[tb_out<0] = np.nan

    # Open one of the NWP files to extract lat/lon info for the outpurt file
    fWindData = nc.Dataset(fWind)
    lon_in = fWindData["XLONG"][0,i:i+interval,:].T
    lat_in = fWindData["XLAT"][0,i:i+interval,:].T
    
    # Set output file name
    fn = output_file_path+'random_Mason' + mode +'Rime_'+str(month)+'-'+str(day)+'-'+str(hour)+'_3D_cut'+str(i)+'-'+str(i+interval)+'.nc'

    # Save to netCDF
    ds = nc.Dataset(fn, 'w', format='NETCDF4')

    lon = ds.createDimension('lon', tb_out.shape[0])
    lat = ds.createDimension('lat', tb_out.shape[1])
    freq = ds.createDimension('freq', tb_out.shape[3])
    alt = ds.createDimension('alt', tb_out.shape[2])

    lons = ds.createVariable('lons','f4', ('lon','lat',))
    lats = ds.createVariable('lats','f4', ('lon','lat',))
    freqs = ds.createVariable('freqs','f4', ('freq',))
    alts = ds.createVariable('alts','f4', ('alt',))
    tb = ds.createVariable('tb','f4', ('lon','lat','alt','freq',))
    
    lons[:] = lon_in
    lats[:] = lat_in
    freqs = freqs_out
    alts = np.array([5000,4500,4000,3500,3000,2600,2200,1800,1400,1000,700,400,152.4])
    tb[:] = tb_out
    ds.close()

    ### -----------------------------------------------------------------------
    # Change mode to do an active radiative transfer simulation at 95 GHz
    pam.nmlSet['passive'] = False
    pam.nmlSet['active'] = True
    # Function located in $HOME/lib/python/pyPamtra/core.py that runs PAMTRA simulation for all randomly selected points
    pam.runParallelPamtraRandom(95,selected[i:i+interval,:],pp_deltaX=1,pp_deltaY=1,pp_deltaF=1,pp_local_workers="auto")

    # Extract all reflectivities in 3D space
    ZeOut = pam.r["Ze"][:,:,:,0,0,0]
    ZeOut[ZeOut<=-40] = np.nan

    # Set output file name
    fn = output_file_path+'random_95GHz_Mason' + mode +'Rime_'+str(month)+'-'+str(day)+'-'+str(hour)+'_3D_cut'+str(i)+'-'+str(i+interval)+'.nc'
    ds = nc.Dataset(fn, 'w', format='NETCDF4')

    lon = ds.createDimension('lon', ZeOut.shape[0])
    lat = ds.createDimension('lat', ZeOut.shape[1])
    hgt = ds.createDimension('hgt', ZeOut.shape[2])

    lons = ds.createVariable('lons','f4', ('lon','lat',))
    lats = ds.createVariable('lats','f4', ('lon','lat',))
    hgts = ds.createVariable('hgts','f4', ('lon','lat','hgt',))
    Ze = ds.createVariable('Ze','f4', ('lon','lat','hgt',))

    lons[:] = pam.p['lon'][:]
    lats[:] = pam.p['lat'][:]
    hgts[:] = pam.p['hgt'][:]
    Ze[:] = ZeOut

    ds.close()


    
