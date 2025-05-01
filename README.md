# A New Machine Learning Retrieval of Liquid Water Path Optimized for Mixed-Phase Cold Air Outbreaks Using Radiometer and Radar Observations

This README will describe the steps to create a LWP/WVP retrieval on your own based on the methods described in Ephraim et al 2025
. Data files are also provided such that you can replicate the retrieval used during the CAESAR campaign. 

## Prerequisites
Install PAMTRA (this is the radiative transfer model we use)
- https://github.com/igmk/pamtra

## Steps
1. Add all the files in the /examples folder in this repository into $HOME/pamtra/examples (this folder will be created when installing PAMTRA)
2. Replace $HOME/lib/python/pyPamtra/core.py and $HOME/lib/python/pyPamtra/importer.py with the versions provided in the /pyPamtra folder in this repository
  - core.py is updated to include the WCR constants
  - core.py also has a




