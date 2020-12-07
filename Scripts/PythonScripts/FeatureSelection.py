# -*- coding: utf-8 -*-
"""
This script is part of the RemoteSensing-of-River-Ice tutorial (https://github.com/SdeRodaHusman/remotesensing-of-river-ice/blob/main/README.md).

With this script, the optimal features for Random Forest classification can be found.
This is done by computing pair-wise correlation and Recursive Feature Elimination with Cross-Validation (RFECV).

@author: SdeRodaHusman (contact: S.deRodaHusman@tudelft.nl), created on Tue Jul 28 11:41:17 2020
"""


# -- Uncomment the following line --
# import_file = ... # Give the path of the CSV file with feature values for all sample pixels


# Import libraries
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt    
from scipy import stats
import pandas as pd
import os
import glob
import re
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV
import warnings
warnings.filterwarnings('ignore')
pd.options.display.max_columns = None

## STEP 0: Import and data preparation

# Import CSV file
df = pd.read_csv(import_file)

# Rename columns 
df.columns = ['VV intensity', 'VH intensity', 'VH/VV intensity', 'Pseudo-Alpha', 'Pseudo-Anisotropy', 'Pseudo-Entropy', 'GLCM Mean', 'GLCM Variance', 'GLCM Correlation', 'IceStage', 'number', 'date']
target = df['IceStage']
df.drop(['IceStage', 'number', 'date'], axis=1, inplace=True)

## STEP 1: Create correlation matrix 
corr_matrix = df.corr()
correlated_features = set()

for i in range(len(corr_matrix.columns)):
    for j in range(i):
        if abs(corr_matrix.iloc[i, j]) > 0.85:
            colname = corr_matrix.columns[i]
            correlated_features.add(colname)
            
print(correlated_features)

# Feature pairs that have a correlation > |0.85| are not used

## STEP 2: Compute RFECV

rfc = RandomForestClassifier(random_state=12)
rfecv = RFECV(estimator=rfc, step=1, cv=StratifiedKFold(10), scoring='accuracy')
rfecv.fit(df, target)

print('Optimal number of features: {}'.format(rfecv.n_features_))

# Create figure with obtained accuracy depending on the number of features selected
plt.figure(dpi=400)
plt.title('Sentinel-1 - RFECV Classification Accuracy')
plt.xlabel('Number of features selected [-]')#, fontsize=14)
plt.ylabel('Overall accuracy [-]')#, fontsize=14)
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_, color='#4c72b0', linewidth=3)
plt.show()

# Compute feature importance
df.drop(df.columns[np.where(rfecv.support_ == False)[0]], axis=1, inplace=True)

dset = pd.DataFrame()
dset['attr'] = df.columns
dset['importance'] = rfecv.estimator_.feature_importances_
dset = dset.sort_values(by='importance', ascending=True)

# Create figure with importance of each feature
plt.figure(dpi=400)
plt.barh(y=dset['attr'], width=dset['importance'], color='#4c72b0')
plt.title('Sentinel-1 - RFECV Feature Importance')
plt.xlabel('Feature Importance Score [-]')
plt.show()

