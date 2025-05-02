"""
File used to combine seperate slices of the brightness temperature radiative transfer simulation into one file

"""

import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import numpy as np # import numpy for arrays, numerical array operations, ....
import netCDF4 as nc
import sys

NWP_data_path = "/NWP/data/path"
partitioned_file_path = "/intermediate/file/path"
merged_output_file_path = '/merged/file/path'

# Get user input
mode = sys.argv[1] # Mode describes how rimed the ice particles are and is either "Normal", "High", or "Low", more details in Ephraim et al 2025
month = int(sys.argv[2]) # Month of the NWP file
day = int(sys.argv[3]) # Day of the NWP file
hour = int(sys.argv[4]) # Hour of the NWP file


# Load in NWP data file
fWindData = nc.Dataset(NWP_data_path + 'wrfout_wind_d02_2020-'+str(month).zfill(2)+'-'+str(day).zfill(2)+'_'+str(hour).zfill(2)+'_00_00')
masterLon = fWindData["XLONG"][0,:,:].T
masterLat = fWindData["XLAT"][0,:,:].T
fWindData.close()

# Create empty array in with the full dimensions of your data set (x_grid in NWP, y_grid in NWP, height levels simulated, number of frequencies simulated)
masterTb = np.zeros((masterLat.shape[0],masterLat.shape[1],13,9))
masterTb[:] = np.nan


# Loop through all the seperate segments of the radiative transfer simulation (recall the simulation was done in slices 5 rows at a time in wrfToPamtra-3D.py
# This loop will combine all those slices into one array
for i in np.arange(0,masterLat.shape[1],5):
    f = nc.Dataset(partitioned_file_path + 'random_Mason' + mode + 'Rime_'+str(month)+'-'+str(day)+'-'+str(hour)+'_3D_cut'+str(i)+'-'+str(i+5)+'.nc')
    tb = f['tb'][:]
    masterTb[:,i:i+5,:,:] = tb
    print(i)
    f.close()

# Create netCDF for merged brightness temperature data
fn = merged_output_file_path + 'random_Mason'+mode+'Rime_'+str(month)+'-'+str(day)+'-'+str(hour)+'_3D_cutCombined.nc'
ds = nc.Dataset(fn, 'w', format='NETCDF4')

lon = ds.createDimension('lon', masterTb.shape[0])
lat = ds.createDimension('lat', masterTb.shape[1])
alt = ds.createDimension('alt', masterTb.shape[2])
freq = ds.createDimension('freq', masterTb.shape[3])

lons = ds.createVariable('lons','f4', ('lon','lat',))
lats = ds.createVariable('lats','f4', ('lon','lat',))
freqs = ds.createVariable('freqs','f4', ('freq',))
alts = ds.createVariable('alts','f4', ('alt',))
tb = ds.createVariable('tb','f4', ('lon','lat','alt','freq',))
    
lons[:] = masterLon
lats[:] = masterLat
freqs[:] = np.array([183.31-14,183.31-7,183.31-3,183.31-1,183.31,183.31+1,183.31+3,183.31+7,183.31+14])
alts[:] = np.array([5000,4500,4000,3500,3000,2600,2200,1800,1400,1000,700,400,152.4])
tb[:] = masterTb

ds.close()
