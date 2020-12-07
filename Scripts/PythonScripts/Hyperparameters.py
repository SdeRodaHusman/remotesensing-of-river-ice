# -*- coding: utf-8 -*-
"""
This script is part of the RemoteSensing-of-River-Ice tutorial (https://github.com/SdeRodaHusman/remotesensing-of-river-ice/blob/main/README.md).

With this script, the optimal hyperparamters for the Random Forest model are found.

@author: SdeRodaHusman (contact: S.deRodaHusman@tudelft.nl), created on Thu Jul 30 14:27:08 2020
"""


# -- Uncomment the following line --
# import_training = ... # Give the path of the CSV file with dataset of feature values for all training sample pixels
# import_validation = ... # Give the path of the CSV file with dataset of feature values for all validation sample pixels


# Import libraries
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt    
from scipy import stats
import pandas as pd
import os
import glob
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import seaborn as sns
from sklearn.metrics import confusion_matrix
import itertools
from sklearn.model_selection import validation_curve

# Read files
S1_training = pd.read_csv(import_training,parse_dates=['date'])
S1_validation = pd.read_csv(import_validation,parse_dates=['date'])

# Only select columns that are used, with the optimal, non-correlated features (see Scripts/PythonScripts/FeatureSelection.py)
X_training = S1_training[['VH_intensity', 'GLCM_mean']] 
Y_training = S1_training['IceStage'] # Labels
X_validation = S1_validation[['VH_intensity', 'GLCM_mean']]

# Give range for each hyperparamter
n_estimators = np.arange(1, 100, 1)
max_depth = np.arange(1, 30, 1)
min_samples_split =  np.arange(2, 40, 1)
min_samples_leaf = np.arange(1, 30, 1)

n_steps = np.arange(1, 30, 1)

# Change param_name and param_range to hyperparameter that you want to tune
train_scores, test_scores = validation_curve(
                                RandomForestClassifier(),
                                X_training, Y_training, 
                                            param_name="min_samples_leaf", 
                                             param_range=min_samples_leaf,
                                             cv=3, 
                                             scoring="accuracy", 
                                             n_jobs=-1)

# Calculate mean and standard deviation for training set scores
train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)

# Calculate mean and standard deviation for test set scores
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

# Create figure of validation curve
plt.style.use('seaborn-darkgrid')
plt.figure(dpi=100)
# Plot accurancy bands for training and test data
plt.fill_between(min_samples_leaf, test_mean - test_std, test_mean + test_std, color="lightgray")
plt.fill_between(min_samples_leaf, train_mean - train_std, train_mean + train_std, color="gray")
# Plot mean accuracy scores for training and test sets
plt.plot(min_samples_leaf, train_mean, label="Training score", color="black")
plt.plot(min_samples_leaf, test_mean, label="Cross-validation score", color="dimgrey")

plt.title("Validation Curve - Minimum samples leaf", fontsize=17)
plt.xlabel("Minimum samples leaf [-]")
plt.ylabel("Accuracy Score [-]")
plt.tight_layout()
plt.legend(loc=4)
plt.ylim([0.5, 1.05])
plt.show()