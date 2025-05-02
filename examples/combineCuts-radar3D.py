"""
File used to combine seperate slices of the reflectivity radiative transfer simulation into one file and vertically integrate reflectivities

"""


import os
import numpy as np # import numpy for arrays, numerical array operations, ....
import netCDF4 as nc
import math
import sys

NWP_data_path = "NWP/data/path"
partitioned_file_path = "/intermediate/file/path"
random_file_path = "random/selection/path"
merged_output_file_path = 'merged/file/path'

# Get user input
mode = sys.argv[1] # Mode describes how rimed the ice particles are and is either "Normal", "High", or "Low", more details in Ephraim et al 2025
month = int(sys.argv[2]) # Month of the NWP file
day = int(sys.argv[3]) # Day of the NWP file
hour = int(sys.argv[4]) # Hour of the NWP file

# Load in NWP data file
fWindData = nc.Dataset(NWP_data_path+'wrfout_wind_d02_2020-'+str(month).zfill(2)+'-'+str(day).zfill(2)+'_'+str(hour).zfill(2)+'_00_00')
masterLon = fWindData["XLONG"][0,:,:].T
masterLat = fWindData["XLAT"][0,:,:].T
h = (fWindData["PH"][0,:,0,0].T + fWindData["PHB"][0,:,0,0].T)/9.81
hdiff = h[1:136]-h[0:135]
fWindData.close()

# Create empty array in with the full dimensions of your data set (x_grid in NWP, y_grid in NWP, height levels in NWP)
masterZ = np.zeros((masterLat.shape[0],masterLat.shape[1],135))
masterZ[:] = np.nan

# Loop through all the seperate segments of the radiative transfer simulation (recall the simulation was done in slices 5 rows at a time in wrfToPamtra-3D.py
# This loop will combine all those slices into one array
for i in np.arange(0,masterLat.shape[1],5):
    f = nc.Dataset(partitioned_file_path+'random_95GHz_Mason'+mode+'Rime_'+str(month)+'-'+str(day)+'-'+str(hour)+'_3D_cut'+str(i)+'-'+str(i+5)+'.nc')
    
    Ze = f['Ze'][:]
    masterZ[:,i:i+5,:] = Ze
    print(i)
    f.close()


# Vertically integrate radar reflectivity, details are described in Ephraim et al 2025
# This chunk of code calculates the non normalized reflectivity, but does not yet do the integration
masterZ[masterZ<-30] = -200
masterZ[~np.isnan(masterZ)] = np.power(10,masterZ[~np.isnan(masterZ)]/10)
masterZ[np.isnan(masterZ)]=0.00000001
for i in np.arange(0,masterZ.shape[0]):
    print(i)
    for j in np.arange(0,masterZ.shape[1]):
        masterZ[i,j,:] = np.multiply(masterZ[i,j,:],hdiff)

# Helper function to find the index in an array that has a value closest to the target value        
def find_nearest_idx(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx        

# List of altitude levels (slimulated flight levels) that reflectivity will be integrated relative to
alts = np.array([5000,4500,4000,3500,3000,2600,2200,1800,1400,1000,700,400,152.4])

# Initialize empty data structure to store integrated reflectivities
masterZRawIntegrated = np.zeros((masterLat.shape[0],masterLat.shape[1],13))
masterZRawIntegrated[:] = 0.00000001

# This chunk of code integrated the raw reflecitity values above the prescribed height level
i=0
for alt in alts:
    idx = find_nearest_idx(h,alt)
    print(idx)
    print(h[idx])
    
    masterZRawIntegrated[:,:,i] = np.sum(masterZ[:,:,idx:120], axis=2) # index 120 is high enough that there are no reflectivities above that level
    i = i+1
        
# Convert integrated raw reflectivities back into a log scale
masterZIntegrated = 10*np.log10(masterZRawIntegrated)
masterZIntegrated[masterZIntegrated<-20] = -20

# Read in the randomly selected points chose in randomSelection.py
f = nc.Dataset(random_file_path+'randomSelect'+str(month)+'-'+str(day)+'.nc')
selected = f['select'][:]
f.close()


# Stack randomly selected points to match the dimensionality of the integrated reflectivities with respect to 13 different altitudes
select = np.stack((selected.T,selected.T,selected.T,selected.T,selected.T,selected.T,selected.T,selected.T,selected.T,selected.T,selected.T,selected.T,selected.T),axis=2)
# Set non-selected points to nan
masterZIntegrated[select==False] = np.nan


# Create netCDF for merged and vertically integrated reflectivity data
fn = merged_output_file_path+'random_95GHz_Mason'+mode+'Rime_'+str(month)+'-'+str(day)+'-'+str(hour)+'_3D_cutCombined_test.nc'
ds = nc.Dataset(fn, 'w', format='NETCDF4')
lon = ds.createDimension('lon', masterZ.shape[0])
lat = ds.createDimension('lat', masterZ.shape[1])
alt = ds.createDimension('alt', masterZIntegrated.shape[2])

lons = ds.createVariable('lons','f4', ('lon','lat',))
lats = ds.createVariable('lats','f4', ('lon','lat',))
alts = ds.createVariable('alts','f4', ('alt',))
Ze = ds.createVariable('Ze','f4', ('lon','lat','alt'))
lons[:] = masterLon
lats[:] = masterLat
alts[:] = np.array([5000,4500,4000,3500,3000,2600,2200,1800,1400,1000,700,400,152.4])
Ze[:] = masterZIntegrated
ds.close()
