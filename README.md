# A New Machine Learning Retrieval of Liquid Water Path Optimized for Mixed-Phase Cold Air Outbreaks Using Radiometer and Radar Observations

This README will describe the steps to create a LWP/WVP retrieval on your own based on the methods described in Ephraim et al 2025
. Data files are also provided such that you can replicate the retrieval used during the CAESAR campaign. 

## Prerequisites
Install PAMTRA (this is the radiative transfer model we use)
- https://github.com/igmk/pamtra

## Setup Steps
1. Add all the files in the /examples folder in this repository into $HOME/pamtra/examples (this folder will be created when installing PAMTRA)
2. Replace $HOME/lib/python/pyPamtra/core.py and $HOME/lib/python/pyPamtra/importer.py with the versions provided in the /pyPamtra folder in this repository
    - core.py is updated to include the WCR constants
    - core.py also has a helper function called runParallelPamtraRandom which only runs PAMTRA radiative transfer simulations on selected points, as opposed to the entire domain
    - importer.py has a helper function called readWrfCOMBLERandom3D that reads in the WRF NWP data and transforms it into a PAMTRA data structure
    - importer.py also has several other custom helper functions that are not used in the operational retrieval, but were used in testing
3. Copy NWP data into a directory of your choosing

## File Descriptions
- randomSelection.py: This file uses a random weighted selection scheme to select the points to do radiative transfer simulations on
- wrfToPamtra-random-3D.py: This file runs passive and active PAMTRA ratiative transfer simulations on the points selected from a given NWP file
- combineCuts-3D.py: This file combines partitions of the passive radiative transfer simulation outputs into one file with the same x/y dimensions as the original NWP file
- combineCuts-radar3D: This file combines partitions of the active radiative transfer simulation outputs into one file with the same x/y dimensions as the original NWP file. This file also does the calculation that vertically integrates reflectivity
- makePoints.py: This file uses the outputs from combineCuts-3D.py and combineCuts-radar3D.py along with the NWP model data to create a list of coordinate points for training/testing
- findHyperparameters.py: This file finds the optimal hyperparameters for the MLPNN regressor using 5-fold validation
- findHyperparametersRF.py: This file finds the optimal hyperparameters for the RF regressor using 5-fold validation
- testing.ipynb: This file conducts model testing of the LWP and WVP retrievals

## Steps
1. Run randomSelection.py
    a.



