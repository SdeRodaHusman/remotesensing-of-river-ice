# -*- coding: utf-8 -*-
"""
This script is part of the RemoteSensing-of-River-Ice tutorial (https://github.com/SdeRodaHusman/remotesensing-of-river-ice/blob/main/README.md).

This script is used to test whether one classifier is significantly better than another classifier.
This is done using the Kappa_hat statistic, with an confidence level of 95%.
When Kappa_hat > 1.96, one classifier is significantly better (or worse) than the other.
    
@author: SdeRodaHusman (contact: S.deRodaHusman@tudelft.nl), created on Tue Jul 28 11:41:17 2020
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
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
import itertools
from scipy import stats
from statsmodels.stats.inter_rater import cohens_kappa, to_table


    
# Read files
S1_training = pd.read_csv(import_training,parse_dates=['date'])
S1_validation = pd.read_csv(import_validation,parse_dates=['date'])

# Give features of two classifiers that you want to compare
# In this example: classifier1 only uses intensity features; classifier2 uses intensity and texture features
X_training_classifier1 = S1_training[['VV_intensity', 'VH_intensity']] 
Y_training_classifier1 = S1_training['IceStage'] # Labels
X_validation_classifier1 = S1_validation[['VV_intensity', 'VH_intensity']]

X_training_classifier2 = S1_training[['VH_intensity', 'GLCM_mean']] 
Y_training_classifier2 = S1_training['IceStage'] # Labels
X_validation_classifier2 = S1_validation[['VH_intensity', 'GLCM_mean']]

Y_validation = S1_validation['IceStage'] # Labels


# Build Random Forest model (using optimal hyperparameters (see Scripts/PythonScripts/Hyperparameters.py)
# and classify the validation data, do this for classifier1 and classifier2
clf_classifier1 = RandomForestClassifier(n_estimators=46, max_depth = 13, min_samples_split=2, min_samples_leaf=1, random_state=12)
clf_classifier1.fit(X_training_classifier1,Y_training_classifier1)
Y_prediction_classifier1 = clf_classifier1.predict(X_validation_classifier1)

clf_classifier2 = RandomForestClassifier(n_estimators=46, max_depth = 13, min_samples_split=2, min_samples_leaf=1, random_state=12)
clf_classifier2.fit(X_training_classifier2,Y_training_classifier2)
Y_prediction_classifier2 = clf_classifier2.predict(X_validation_classifier2)

# Accuracy assessment (confusion matrix, kappa, overall accuracy), again do this for classifier1 and classifier2
CM_classifier1 = confusion_matrix(Y_validation, Y_prediction_classifier1)
kappa_classifier1 = cohens_kappa(CM_classifier1).kappa
kappa_var_classifier1 = cohens_kappa(CM_classifier1).var_kappa
 
CM_classifier2 = confusion_matrix(Y_validation, Y_prediction_classifier2)
kappa_classifier2 = cohens_kappa(CM_classifier2).kappa
kappa_var_classifier2 = cohens_kappa(CM_classifier2).var_kappa

# Compute Kappa_hat
KHAT = np.abs(kappa_classifier1 - kappa_classifier2) / np.sqrt(kappa_var_classifier1 + kappa_var_classifier2)