"""
File used to tune hyperparameters for the neural network regressor

"""

import numpy as np
import netCDF4 as nc
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
import copy
import random
import sys
import random
from scipy.stats import uniform, randint
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
    
# Randomly select 100 different architectures, method describes in Ephraim et al 2025
hidden_layers = []
for i in np.arange(1,100):
    num_layers = random.randint(1, 3)
    if num_layers==3:
        hidden_layers.append((random.randint(1, 10)*10,random.randint(1, 10)*10,random.randint(1, 10)*10))

    if num_layers==2:
        hidden_layers.append((random.randint(1, 10)*25,random.randint(1, 10)*25))

    if num_layers==1:
        hidden_layers.append((random.randint(1, 10)*50,))

# Full phase space of hyperparameters tested
param_dist = {
    'hidden_layer_sizes': hidden_layers,
    'activation': ['relu', 'tanh', 'logistic'],
    'alpha': [0.0001,0.001,0.01] 
}
            
# Initialize NN regressor
model = MLPRegressor(
random_state=20,
early_stopping=True, 
max_iter=500
)

# Use 5-fold validation testing to test the performance of the different model configurations on training data
grid = RandomizedSearchCV(model, param_dist, n_iter=100,n_jobs=-1, scoring='neg_root_mean_squared_error',verbose=3)
grid.fit(X_train[:,0:5], y_train)


print("BestParams")    
print(grid.best_params_)
print(grid.best_score_)
print(grid.cv_results_)


