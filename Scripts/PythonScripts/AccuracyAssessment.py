# -*- coding: utf-8 -*-
"""
This script is part of the RemoteSensing-of-River-Ice tutorial (https://github.com/SdeRodaHusman/remotesensing-of-river-ice/blob/main/README.md).

This script is used to assess the accuracy of the developed classifier. The following metrics are evaluated:
    - Confusion matrix (CM)
    - Kappa statistic (Kappa)
    - Overall accuracy (OA)
    
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

# Function to create fancy confusion matrix
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')


    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
# Read files
S1_training = pd.read_csv(import_training,parse_dates=['date'])
S1_validation = pd.read_csv(import_validation,parse_dates=['date'])

# Only select columns that are used, with the optimal, non-correlated features (see Scripts/PythonScripts/FeatureSelection.py)
X_training = S1_training[['VH_intensity', 'GLCM_mean']] 
Y_training = S1_training['IceStage'] # Labels

X_validation = S1_validation[['VH_intensity', 'GLCM_mean']]
Y_validation = S1_validation['IceStage'] # Labels


# Build Random Forest model (using optimal hyperparameters (see Scripts/PythonScripts/Hyperparameters.py)
# and classify the validation data
clf=RandomForestClassifier(n_estimators=46, max_depth = 13, min_samples_split=2, min_samples_leaf=1, random_state=12)
clf.fit(X_training,Y_training)
Y_prediction =clf.predict(X_validation)


# Accuracy assessment (confusion matrix, kappa, overall accuracy)
CM = confusion_matrix(Y_validation, Y_prediction)
kappa = cohens_kappa(CM).kappa
kappa_var = cohens_kappa(CM).var_kappa
overall_accuracy = metrics.accuracy_score(Y_validation, Y_prediction)  

# Visualize the confusion matrix
sns.set()
plt.figure(dpi=400)
plot_confusion_matrix(CM, classes=['Sheet ice', 'Ice jam', 'Open water'], normalize=True,
                      title='S1-Int - Normalized confusion matrix')
plt.ylim([2.5, -.5])
plt.grid(False)
plt.show()
sns.set()