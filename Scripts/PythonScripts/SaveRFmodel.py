# -*- coding: utf-8 -*-
"""
This script is part of the RemoteSensing-of-River-Ice tutorial (https://github.com/SdeRodaHusman/remotesensing-of-river-ice/blob/main/README.md).

This script is used to save a Random Forest model.

The following input file is required:
    - Trainig data set (csv-file, output of Scripts/PythonScripts/CreateFeatureMatrix_TrainingValidation.py)

The output of this script is a sav-file

@author: SdeRodaHusman (contact: S.deRodaHusman@tudelft.nl), created on  Wed Jul  8 14:56:34 2020
"""

# Import libraries
import numpy as np
import pandas as pd
from osgeo import gdal
from osgeo import osr
from sklearn.ensemble import RandomForestClassifier
import pickle

# -- Uncomment the following lines --
# training_data =  pd.read_csv(...) # Give file location training data 

# Select the columns of interest
X_training = training_data[['VH_intensity','GLCM_mean']] # Indicate features of interest, following from Scripts/PythonScripts/FeatureSelection.py
Y_training = training_data['IceStage'] # Labels

# Create a Gaussian Classifier (change the hyperparamters to optimal values, following from Scripts/PythonScripts/Hyperparameters.py)
clf=RandomForestClassifier(n_estimators=46, max_depth = 13, min_samples_split=2, min_samples_leaf=1, random_state=12)

# Train the model using the training set
clf.fit(X_training,Y_training)

# Save the model to disk
filename = 'finalized_model.sav'
pickle.dump(clf, open(filename, 'wb'))