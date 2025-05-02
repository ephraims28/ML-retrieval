"""
File used to tune hyperparameters for the random forest regressor

"""


import numpy as np
import netCDF4 as nc
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
import copy
import random
import sys
from sklearn.model_selection import RandomizedSearchCV

# Get user input
retrievalType = sys.argv[1] # LWP or WVP

points_output_file_path = '/points/file/path'

# Import training points from each model run
LAM_values1 = np.load(points_output_file_path+'MasonNormalRime_3-28-12z_3D_95GHz_Values.npy')
LAM_points1 = np.load(points_output_file_path+'3-28-12z_3D_95GHz_Points.npy')

LAM_values2 = np.load(points_output_file_path+'MasonNormalRime_4-10-12z_3D_95GHz_Values.npy')
LAM_points2 = np.load(points_output_file_path+'4-10-12z_3D_95GHz_Points.npy')

LAM_values3 = np.load(points_output_file_path+'MasonNormalRime_4-26-6z_3D_95GHz_Values.npy')
LAM_points3 = np.load(points_output_file_path+'4-26-6z_3D_95GHz_Points.npy')


# Concatenate training points into a single data structure
if retrievalType == "LWP":
    X_train = np.concatenate((LAM_values1[:,0:5],LAM_values2[:,0:5],LAM_values3[:,0:5]),axis=0)
    y_train = np.concatenate((LAM_points1[:,0],LAM_points2[:,0],LAM_points3[:,0]),axis=0)

if retrievalType == "WVP":
    X_train = np.concatenate((LAM_values1[:,0:5],LAM_values2[:,0:5],LAM_values3[:,0:5]),axis=0)
    y_train = np.concatenate((LAM_points1[:,2],LAM_points2[:,2],LAM_points3[:,2]),axis=0)

# Full phase space of hyperparameters tested
param_dist = {
    'criterion': ["squared_error", "friedman_mse","poisson"],
    'n_estimators': np.arange(1,50)
}

# Initialize random forest regressor
model = RandomForestRegressor(
random_state=0
)

# Use 5-fold validation testing to test the performance of the different model configurations on training data
grid = RandomizedSearchCV(model, param_dist, n_iter=10,n_jobs=-1, scoring='neg_root_mean_squared_error',verbose=3)
grid.fit(X_train[:,0:4], y_train)

print("BestParams")    
print(grid.best_params_)
print(grid.best_score_)
print(grid.cv_results_)


