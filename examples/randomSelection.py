"""
File used to psuedo-randomly select points to do radiative transfer simulations

"""

from scipy import stats
import numpy as np
import netCDF4 as nc

LES_data_path = "/path/to/LES"
LAM_data_path = "/path/to/LAM"
random_file_path = "/random/file/path"


### ---------- LES Model Random Selection --------------------------------------------------------------
# Import NWP file with info on LWP and SWP
fRad = nc.Dataset(LES_data_path+'wrfout_rad_d02_2020-03-13_12_00_00')
LWP = fRad["LWP"][0,:,:]*1000
SWP = fRad["SWP"][0,:,:]*1000
fRad.close()

# Create bins of LWP/SWP and determine counts for each bin
statistic, xbin, ybin, bins = stats.binned_statistic_2d(LWP.flatten(), SWP.flatten(), values=np.ones(LWP.flatten().shape),statistic ='count', bins = [100, 100],expand_binnumbers=True)


selected = np.zeros(LWP.shape)
# for each candidate point
for i in np.arange(0,LWP.shape[0]):
    print(i)
    for j in np.arange(0,LWP.shape[1]):
        # find which bin point is in
        LWP_val = LWP[i,j]
        SWP_val = SWP[i,j]
        LWP_bin_num = 0
        for val in xbin[1:]:
            if LWP_val > val:
                LWP_bin_num = LWP_bin_num + 1
        SWP_bin_num = 0         
        for val in ybin[1:]:
            if SWP_val > val:
                SWP_bin_num = SWP_bin_num + 1  

        # find number of points in that bin
        n = statistic[LWP_bin_num,SWP_bin_num]
        
        # probability of selection, formula determined through trial and error
        prob = ((np.exp(-n*0.005)+0.01))/40
        boolean = np.random.choice([1,0],p=[prob,1-prob])
        if boolean:
            selected[i][j]=1


# Read in NWP file to get location information
fWind = nc.Dataset(LES_data_path+'wrfout_wind_d02_2020-03-13_12_00_00')
hgt = fWind["HGT"][0,:,:]
lon_in = fWind["XLONG"][0,:,:]
lat_in = fWind["XLAT"][0,:,:]
fWind.close()

# Don't select any points above sea level
selected[hgt>0] = 0

# Create output file
fn = random_file_path + 'randomSelect3-13.nc'
ds = nc.Dataset(fn, 'w', format='NETCDF4')
lon = ds.createDimension('lon', lon_in.shape[0])
lat = ds.createDimension('lat', lon_in.shape[1])
lons = ds.createVariable('lons','f4', ('lon','lat',))
lats = ds.createVariable('lats','f4', ('lon','lat',))
select = ds.createVariable('select','f4', ('lon','lat',))
lons[:] = lon_in
lats[:] = lat_in
select[:] = selected
ds.close()

### ---------- LAM Model Random Selection File 1 --------------------------------------------------------------
# Import NWP file with info on LWP and SWP
from scipy import stats
fRad = nc.Dataset(LAM_data_path+'wrfout_rad_d02_2020-03-28_12_00_00')
LWP = fRad["LWP"][0,:,:]*1000
SWP = fRad["SWP"][0,:,:]*1000
fRad.close()

# Create bins of LWP/SWP and determine counts for each bin
statistic, xbin, ybin, bins = stats.binned_statistic_2d(LWP.flatten(), SWP.flatten(), values=np.ones(LWP.flatten().shape),statistic ='count', bins = [100,100],expand_binnumbers=True)


selected = np.zeros(LWP.shape)
# for each candidate point
for i in np.arange(0,LWP.shape[0]):
    for j in np.arange(0,LWP.shape[1]):
        # find which bin point is in
        LWP_val = LWP[i,j]
        SWP_val = SWP[i,j]
        LWP_bin_num = 0
        for val in xbin[1:]:
            if LWP_val > val:
                LWP_bin_num = LWP_bin_num + 1
        SWP_bin_num = 0         
        for val in ybin[1:]:
            if SWP_val > val:
                SWP_bin_num = SWP_bin_num + 1  

        # find number of points in that bin
        n = statistic[LWP_bin_num,SWP_bin_num]
        
        # probability of selection, formula determined through trial and error
        prob = np.exp(-n*0.0010)/3+0.005
        if prob>1:
            prob=1
        boolean = np.random.choice([1,0],p=[prob,1-prob])
        if boolean:
            selected[i][j]=1

# Read in NWP file to get location information
fWind = nc.Dataset(LAM_data_path+'wrfout_wind_d02_2020-03-28_12_00_00')
hgt = fWind["HGT"][0,:,:]
lon_in = fWind["XLONG"][0,:,:]
lat_in = fWind["XLAT"][0,:,:]
fWind.close()

# Don't select any points above sea level
selected[hgt>0] = 0

# Create output file
fn = random_file_path + 'randomSelect3-28.nc'
ds = nc.Dataset(fn, 'w', format='NETCDF4')
lon = ds.createDimension('lon', lon_in.shape[0])
lat = ds.createDimension('lat', lon_in.shape[1])
lons = ds.createVariable('lons','f4', ('lon','lat',))
lats = ds.createVariable('lats','f4', ('lon','lat',))
select = ds.createVariable('select','f4', ('lon','lat',))
lons[:] = lon_in
lats[:] = lat_in
select[:] = selected
ds.close()

### ---------- LAM Model Random Selection File 2--------------------------------------------------------------
# Import NWP file with info on LWP and SWP
from scipy import stats
fRad = nc.Dataset(LAM_data_path+'wrfout_rad_d02_2020-04-10_12_00_00')
LWP = fRad["LWP"][0,:,:]*1000
SWP = fRad["SWP"][0,:,:]*1000
fRad.close()

# Create bins of LWP/SWP and determine counts for each bin
statistic, xbin, ybin, bins = stats.binned_statistic_2d(LWP.flatten(), SWP.flatten(), values=np.ones(LWP.flatten().shape),statistic ='count', bins = [100,100],expand_binnumbers=True)


selected = np.zeros(LWP.shape)
# for each candidate point
for i in np.arange(0,LWP.shape[0]):
    for j in np.arange(0,LWP.shape[1]):
        # find which bin point is in
        LWP_val = LWP[i,j]
        SWP_val = SWP[i,j]
        LWP_bin_num = 0
        for val in xbin[1:]:
            if LWP_val > val:
                LWP_bin_num = LWP_bin_num + 1
        SWP_bin_num = 0         
        for val in ybin[1:]:
            if SWP_val > val:
                SWP_bin_num = SWP_bin_num + 1  

        # find number of points in that bin
        n = statistic[LWP_bin_num,SWP_bin_num]
        
        # probability of selection, formula determined through trial and error
        prob = np.exp(-n*0.0010)/3+0.005
        if prob>1:
            prob=1
        boolean = np.random.choice([1,0],p=[prob,1-prob])
        if boolean:
            selected[i][j]=1

# Read in NWP file to get location information
fWind = nc.Dataset(LAM_data_path+'wrfout_wind_d02_2020-04-10_12_00_00')
hgt = fWind["HGT"][0,:,:]
lon_in = fWind["XLONG"][0,:,:]
lat_in = fWind["XLAT"][0,:,:]
fWind.close()

# Don't select any points above sea level
selected[hgt>0] = 0

# Create output file
fn = random_file_path + 'randomSelect4-10.nc'
ds = nc.Dataset(fn, 'w', format='NETCDF4')
lon = ds.createDimension('lon', lon_in.shape[0])
lat = ds.createDimension('lat', lon_in.shape[1])
lons = ds.createVariable('lons','f4', ('lon','lat',))
lats = ds.createVariable('lats','f4', ('lon','lat',))
select = ds.createVariable('select','f4', ('lon','lat',))
lons[:] = lon_in
lats[:] = lat_in
select[:] = selected
ds.close()

### ---------- LAM Model Random Selection --------------------------------------------------------------
# Import NWP file with info on LWP and SWP
from scipy import stats
fRad = nc.Dataset(LAM_data_path+'wrfout_rad_d02_2020-04-26_06_00_00')
LWP = fRad["LWP"][0,:,:]*1000
SWP = fRad["SWP"][0,:,:]*1000
fRad.close()

# Create bins of LWP/SWP and determine counts for each bin
statistic, xbin, ybin, bins = stats.binned_statistic_2d(LWP.flatten(), SWP.flatten(), values=np.ones(LWP.flatten().shape),statistic ='count', bins = [100,100],expand_binnumbers=True)


selected = np.zeros(LWP.shape)
# for each candidate point
for i in np.arange(0,LWP.shape[0]):
    for j in np.arange(0,LWP.shape[1]):
        # find which bin point is in
        LWP_val = LWP[i,j]
        SWP_val = SWP[i,j]
        LWP_bin_num = 0
        for val in xbin[1:]:
            if LWP_val > val:
                LWP_bin_num = LWP_bin_num + 1
        SWP_bin_num = 0         
        for val in ybin[1:]:
            if SWP_val > val:
                SWP_bin_num = SWP_bin_num + 1  

        # find number of points in that bin
        n = statistic[LWP_bin_num,SWP_bin_num]
        
        # probability of selection, formula determined through trial and error
        prob = np.exp(-n*0.0010)/3+0.005
        if prob>1:
            prob=1
        boolean = np.random.choice([1,0],p=[prob,1-prob])
        if boolean:
            selected[i][j]=1

# Read in NWP file to get location information
fWind = nc.Dataset(LAM_data_path+'wrfout_wind_d02_2020-04-26_06_00_00')
hgt = fWind["HGT"][0,:,:]
lon_in = fWind["XLONG"][0,:,:]
lat_in = fWind["XLAT"][0,:,:]
fWind.close()

# Don't select any points above sea level
selected[hgt>0] = 0

# Create output file
fn = random_file_path + 'randomSelect4-26.nc'
ds = nc.Dataset(fn, 'w', format='NETCDF4')
lon = ds.createDimension('lon', lon_in.shape[0])
lat = ds.createDimension('lat', lon_in.shape[1])
lons = ds.createVariable('lons','f4', ('lon','lat',))
lats = ds.createVariable('lats','f4', ('lon','lat',))
select = ds.createVariable('select','f4', ('lon','lat',))
lons[:] = lon_in
lats[:] = lat_in
select[:] = selected
ds.close()
