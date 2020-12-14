# -*- coding: utf-8 -*-
"""
This script is part of the RemoteSensing-of-River-Ice tutorial (https://github.com/SdeRodaHusman/remotesensing-of-river-ice/blob/main/README.md).

This script is used to classify a SAR image by using a Random Forest model based on multiple features.

The following input files are required:
    - Trainig data set (csv-file, output of Scripts/PythonScripts/CreateFeatureMatrix_TrainingValidation.py)
    Alternative: you can also load a created Random Forest model instead of training the model based on the traning data set. 
    - Preprocessed intensity features for pixels that you want to classify (csv-file, output of Scripts/PythonScripts/Create
FeatureMatrix_SARimage.py)
    - Preprocessed polarimetric features for pixels that you want to classify (csv-file, output of Scripts/PythonScripts/Create
FeatureMatrix_SARimage.py)
    - Preprocessed texture features for pixels that you want to classify (csv-file, output of Scripts/PythonScripts/Create
FeatureMatrix_SARimage.py)

The output of this script is a GeoTiff file with classified pixels. This file can be imported in QGIS, for example. 
In this output product the ice classes are represented with numbers, where sheet ice = 1, rubble ice = 2, open water = 3.
@author: SdeRodaHusman (contact: S.deRodaHusman@tudelft.nl), created on  Wed Jul  8 14:56:34 2020
"""

# Import libraries
import numpy as np
import pandas as pd
from osgeo import gdal
from osgeo import osr
from sklearn.ensemble import RandomForestClassifier
import pickle # only required when you want to import a Random Forest model (.sav file)

# -- Uncomment the following lines --
# output_path = ...  (Give your output path to save the classified GeoTiff file)

# training_data =  pd.read_csv(...) # Give file location training data 
# ALTERNATIVE (instead of trainig_data): load a Random Forest model (sav-file): loaded_model = pickle.load(open(filename, 'rb'))

#data_intensity = pd.read_csv(...) # Give file location of preprocessed intensity features (output of Scripts/PythonScripts/CreateFeatureMatrix_SARimage.py)
#data_polarimetric = pd.read_csv(...) # Give file location of preprocessed polarimetric features (output of Scripts/PythonScripts/CreateFeatureMatrix_SARimage.py)
#data_texture = pd.read_csv(...) # Give file location of preprocessed texture features (output of Scripts/PythonScripts/CreateFeatureMatrix_SARimage.py)


# Select the columns of interest
X_training = training_data[['VH_intensity','GLCM_mean']] # Indicate features of interest, following from Scripts/PythonScripts/FeatureSelection.py
Y_training = training_data['IceStage'] # Labels

# Reformat preprocessed SAR image files
data_all = pd.concat([data_intensity, data_polarimetric, data_texture], axis=1)
data_all = data_all.loc[:,~data_all.columns.duplicated()]
data_all = data_all.replace([np.inf, -np.inf], np.nan)
data_all = data_all.dropna()

lon = data_all['lon']
lat = data_all['lat']

# Select colums of interest of pixels that should be classified (use same features as in X_training)
X_classifySAR = data_all[['VH_intensity','GLCM_mean']]

# Create a Gaussian Classifier
clf=RandomForestClassifier(n_estimators=46, max_depth = 13, min_samples_split=2, min_samples_leaf=1, random_state=12)

# Train the model using the training set
clf.fit(X_training,Y_training)

# Classify the pixels of interest
Y_prediction=clf.predict(X_classifySAR)

df_final = pd.DataFrame({'lon': lon, 'lat': lat, 'Prediction': Y_prediction})

# Write ice classes as numbers, where sheetice = 1, rubble ice = 2, openwater = 3
df_final_numbers = df_final
df_final_numbers['Prediction'] = df_final_numbers['Prediction'].replace('sheetice',1)
df_final_numbers['Prediction'] = df_final_numbers['Prediction'].replace('rubbleice',2)
df_final_numbers['Prediction'] = df_final_numbers['Prediction'].replace('openwater',3)

# Create matrix of data
lons = df_final_numbers['lon']
lats = df_final_numbers['lat']
vals = df_final_numbers['Prediction']

# Craate arrays (this step is required when writing GeoTiff files)
lat_vals, lat_idx = np.unique(lats, return_inverse=True)
lon_vals, lon_idx = np.unique(lons, return_inverse=True)
vals_array = np.empty(lat_vals.shape + lon_vals.shape)
vals_array.fill(np.nan) 
vals_array[lat_idx, lon_idx] = vals
array = np.array(vals_array)

# Write to GeoTiff
xmin,ymin,xmax,ymax = [lon_vals.min(),lat_vals.max(),lon_vals.max(),lat_vals.min()]
nrows,ncols = np.shape(array)
xres = (xmax-xmin)/float(ncols)
yres = (ymax-ymin)/float(nrows)
geotransform=(xmin,xres,0,ymax,0, -yres)   

output_raster = gdal.GetDriverByName('GTiff').Create(output_path,ncols, nrows, 1 ,gdal.GDT_Byte) #GDT_Float32
output_raster.GetRasterBand(1).WriteArray( array ) 
output_raster.SetGeoTransform(geotransform)
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)
output_raster.SetProjection(srs.ExportToWkt())
output_raster = None