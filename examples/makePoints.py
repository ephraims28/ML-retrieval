"""
File used to create a list of training/test values and points using the merged brightness temperature and integrasted refelctivity files
"""

import pandas as pd
import numpy as np
import netCDF4 as nc
import sys


NWP_data_path = "/glade/derecho/scratch/ephraims/FROM_CHEYENNE/WRFout_revision/"
merged_output_file_path = '/glade/derecho/scratch/ephraims/FROM_CHEYENNE/pamtra_combined_cuts/'
points_output_file_path = '/glade/derecho/scratch/ephraims/FROM_CHEYENNE/pamtra_points_revision/'

# Helper function to find the index in an array that has a value closest to the target value  
def find_nearest_idx(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx        


## Get user input
mode = sys.argv[1] # Mode describes how rimed the ice particles are and is either "Normal", "High", or "Low", more details in Ephraim et al 2025
month = int(sys.argv[2])
day = int(sys.argv[3])
hour = int(sys.argv[4])
makePoints = int(sys.argv[5]) # Whether points LWP/WVP etc relative to simulated flight level need to be created (0/1)

# Load merged data file of brightness temperatures
f = nc.Dataset(merged_output_file_path+"random_Mason"+ mode +"Rime_" + str(month)+"-"+str(day)+"-"+str(hour)+"_3D_cutCombined.nc")

# Calculate the 4 channels that the GVR measures (+/-14GHz, +/-7GHz, +/-3GHz, +/-1GHz)
wing14 = (f['tb'][:,:,:,0] + f['tb'][:,:,:,8])/2
wing7 = (f['tb'][:,:,:,1] + f['tb'][:,:,:,7])/2
wing3 = (f['tb'][:,:,:,2] + f['tb'][:,:,:,6])/2
wing1 = (f['tb'][:,:,:,3] + f['tb'][:,:,:,5])/2

# Load merged and vertically integrated reflectivity data file
f = nc.Dataset(merged_output_file_path+"random_95GHz_Mason"+ mode +"Rime_" + str(month)+"-"+str(day)+"-"+str(hour)+"_3D_cutCombined.nc")
radar = f['Ze'][:,:,:]*1
radar
f.close()


Grav = 9.80665  # m/s^2 der Wert fuer mittlere Breiten
Rair = 287.04  # J/kg/K
Rvapor = 461.5  # J/kg/K
Cp = 1005.0  # J/kg/K specific heat capacity
Gamma = -Grav/Cp  # =-0.0097..K/m  adiabatic temperature gradient
Lv = 2.5e6  # J/kg  bei 0C Lv heat of vaporization
Mwml = 0.622  # dimlos, Molmassenverhaeltnis
Tnull = -273.15  # degC absolute zero
Kadiab = Rair/Cp  # dimensionless adiabatic exponenet
g = 9.80665  # gravitational acceleration

p0 = 100000
Cp = 7.*Rair/2.
RdCp =  Rair/Cp
#---------


# Create empty data structures to store list of points and values
points = np.zeros(((radar>=-40).sum(),5)) # dimensions of (# of points selected, (lwp,swp,wvp,gwp,iwp))
values = np.zeros(((radar>=-40).sum(),6))  # dimensions of (# of points selected, (TB14,TB7,TB3,TB1,refl,reference alt))

# Load in NWP files
fCloud = nc.Dataset(NWP_data_path+'wrfout_cloud_d02_2020-'+str(month).zfill(2)+"-"+str(day).zfill(2)+"_"+str(hour).zfill(2)+'_00_00')
fWind = nc.Dataset(NWP_data_path+'wrfout_wind_d02_2020-'+str(month).zfill(2)+"-"+str(day).zfill(2)+"_"+str(hour).zfill(2)+'_00_00')

# List of altitudes
alts = np.array([5000,4500,4000,3500,3000,2600,2200,1800,1400,1000,700,400,152.4])

# Calculate altitude in NWP model
h = (fWind["PH"][0,:,0,0].T +fWind["PHB"][0,:,0,0].T)/9.81

# Find the index in the NWP model that each altitude in alts occurs at, since we only use sea level points, these are approximately the same across the model domain
hInd = []
for alt in alts:
    hInd.append(find_nearest_idx(h,alt))



count = 0
ind = 0
# Iterate through all rows
for i in np.arange(0,radar.shape[0]):
    # Grab chunks of microphysical data every 100 rows if makePoints==1, this speeds up computation
    if i%100 == 0:
        ind = i
        maxInd = np.min([i+100,radar.shape[0]])
        if makePoints:
            gwc = fCloud["QGRAUP"][0,:,:,i:maxInd]
            lwc = fCloud["QCLOUD"][0,:,:,i:maxInd]
            swc = fCloud["QSNOW"][0,:,:,i:maxInd]
            iwc = fCloud["QICE"][0,:,:,i:maxInd]
            q = fCloud["QVAPOR"][0,:,:,i:maxInd]
            height = (fWind["PH"][0,:,:,i:maxInd]+fWind["PHB"][0,:,:,i:maxInd])/9.81
            rho_global = (fWind["RHO"][0,:,:,i:maxInd])
            
    # Iterate through all columns   
    for j in np.arange(0,radar.shape[1]):
        # Only do calculations at selected points
        if not np.isnan(radar[i][j][0]):
            # Create a point/value for each reference height
            for zInd,z in enumerate(hInd):
                if makePoints:
                    gwp = 0
                    swp = 0
                    lwp = 0
                    wvp = 0
                    iwp = 0
                    # Iteratively sum hydrometeor paths starting from reference altitude until TOA
                    # ie, for each layer: LWP = rho*dz*LWC
                    for k in np.arange(z,height.shape[0]-1):
                
                        rho = rho_global[k][j][i-ind]
                        dz = height[k+1][j][i-ind]- height[k][j][i-ind]
                        gwp = gwp+rho*dz*gwc[k][j][i-ind]
                        swp = swp+rho*dz*swc[k][j][i-ind]
                        lwp = lwp+rho*dz*lwc[k][j][i-ind]
                        wvp = wvp+rho*dz*q[k][j][i-ind]
                        iwp = iwp+rho*dz*iwc[k][j][i-ind]

                    # Convert from kg/m2 to g/m2 and add hydrometeor path to list of points
                    points[count,0] = lwp*1000
                    points[count,1] = swp*1000
                    points[count,2] = wvp*1000
                    points[count,3] = gwp*1000
                    points[count,4] = iwp*1000
                # Add radiative transfer simulation output into list of points
                values[count,0] = wing14[i][j][zInd]
                values[count,1] = wing7[i][j][zInd]
                values[count,2] = wing3[i][j][zInd]
                values[count,3] = wing1[i][j][zInd]
            
                values[count,4] = radar[i][j][zInd]
                values[count,5] = alts[zInd]
            
                count = count+1
fWind.close()
fCloud.close()

# Save list of points into numpy array to use for training
if makePoints:
    np.save(points_output_file_path+str(month)+"-"+str(day)+"-"+str(hour)+"z_3D_95GHz_Points_test",points)
    
np.save(points_output_file_path+'Mason'+mode+"Rime_"+str(month)+"-"+str(day)+"-"+str(hour)+"z_3D_95GHz_Values_test",values)

