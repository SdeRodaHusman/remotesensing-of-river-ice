# remotesensing-of-river-ice

This repository provides material used for the paper: <add a link here> ...

Overview
========

River ice during breakup can be classified using a Random Forest classifier. The repository contains scripts and models which can be used to classify river ice during breakup using SAR data.

The scripts make use of:
  1) SNAP (version 8.0)
  2) QGIS (version 3.0)
  3) Python (e.g. Spyder, Anaconda version 3.0)

There are two paths in this tutorial that can be followed to perform classification (also see the figure below), namely:
- **Option 1:** Generic approach (use the developed classifier presented in the paper, which was trained for the Athabasca River, Alberta using Sentinel-1 SAR data)
- **Option 2:** Build your own Random Forest classifier (follow this step when you want to build your own classifier, e.g. when you want to classify another river or use data from a SAR mission that is differently polarized than Sentinel-1 (VV-VH). 

The steps needed for the first and second paths are described below.

![alt text](https://github.com/SdeRodaHusman/remotesensing-of-river-ice/blob/main/Figures/Roadmap_RemoteSensingofRiverIce.jpg?raw=true)


Tutorial 1 - Generic approach
========

The overall analysis and classification are performed in a number of steps, starting with the download of all required datasets, such as:

* Developed Random Forest classifier (this can be found in RFmodel/S1_RFmodel_AthabascaRiver.sav)
* Outline of river of interest (outlines of the Peace River and Athabasca River can be found in Data/OutlinePeaceAthabascaRiver)

The actual steps required for the analysis include:

Step 1. **Download Sentinel-1 SLC SAR images**

Download SAR images that you would like to classify, for example via https://scihub.copernicus.eu/.

Step 2. **Preprocess Sentinel-1 SLC SAR images** *(Scripts/XLMgraphs/S1_Intensity.xml, Scripts/XLMgraphs/S1_Texture.xml)*

Produces preprocessed NetCDF files for (1) intensity and (2) texture features. XML graphs can be used in SNAP or using the provided GPT script *(Scripts/GPTscript.bat)*

Step 3. **Combine all preprocessed images into one NetCDF file** *(Scripts/XLMgraphs/CombinePreprocessedImages.xml)*

Combines the preprocessed intensity and texture images by using the *Collocation* option in SNAP. 

Step 4. **Create CSV file with all features** *(Scripts/PythonScripts/CreateFeatureMatrix_SARimage.py)*

Produces a CSV file with VH intensity and GLCM mean values for all pixels of the SAR image of interest.

Step 5. **Perform Random Forest classification** *(Scripts/PythonScripts/ClassifySARimage.py)* 

Creates a NetCDF file in which all pixels are classified as sheet ice, rubble ice or open water. 



Tutorial 2 - Build your own Random Forest classifier
========

The overall analysis and classification are performed in a number of steps, starting with the download of all required datasets, such as:

* Outline of river of interest (outlines of the Peace River and Athabasca River can be found in Data/OutlinePeaceAthabascaRiver)

The actual steps required for the analysis are quite time consuming and include:

Step 1. **Download multiple SLC SAR images during breakup**

It is advisable to download multiple images that include different breakup processes (at least three images including rubble ice pixels, three including sheet ice pixels, and three including open water pixels). When Sentinel-1 images are used, these can be downloaded via https://scihub.copernicus.eu/.

Step 2. **Preprocess the SLC SAR images** *(Scripts/XLMgraphs/S1_Intensity.xml, Scripts/XLMgraphs/S1_Polarimetric.xml, Scripts/XLMgraphs/S1_Texture.xml)*

The scripts provided in the *Scripts/XLMgraphs/* folder produce preprocessed NetCDF files for (1) intensity, (2) polarimetric and (3) texture features for Sentinel-1. XML graphs can be used in SNAP or using the provided GPT script *(Scripts/GPTscript.bat)*. When other SAR missions are used, note that the provided scripts should be adjusted. SNAP does not allow to perform the step *Apply orbit file* on other missions than Sentinel-1, so this step should be removed for other missions. 

Step 3. **Load preprocessed NetCDF files in QGIS and create sample areas (based on reference data** *(Videos/SampleAreasQGIS.mp4)*

Load the preprocessed NetCDFs in QGIS and create sample areas from which the ice stage is known. It is recommended to create a total of 70 sample areas from 100 pixels each, 
for all ice stage (rubble ice, sheet ice and open water) of interest. Hence, 210 sample areas (or 21000 pixels) will be created. This method is also explained in *Videos/SampleAreasQGIS.mp4*.

Step 4. **Extract feature values for all sample areas** *(Videos/SampleAreasQGIS.mp4 and Scripts/QGISmodels/ExtractFeatureValues.model3)*

Extract feature values for all sample pixels, use .csv as output. This can be done in QGIS, see video *Videos/SampleAreasQGIS.mp4* for an in-depth explanation.  

Step 5. **Split sample areas into training and validation datasets**

Create two folders; for each ice stage randomly put 50 sample areas (or 70% of the sample areas) in one folder and the other 20 sample areas (or 30% of the sample areas). This step only has to be performed once, e.g. only for HH intensity. The other feature values do not have to be split into training and validation datasets.  

Step 6. **Create CSV file for training and validation data with all features and labels** *(Scripts/PythonScripts/CreateFeatureMatrix_TrainingValidation.py)*

Produces two CSV files, one for training and one for validation. These files consist of matrices including all training or validation pixels with all feature values. 

Step 7. **Select the optimal, non-correlated features** *(Scripts/PythonScripts/FeatureSelection.py)* 

Based on a pair-wise correlation between all features and a Recursive Feature Elimination with Cross-Validation (RFECV) of the training data set, the optimal features for Random Forest classification can be found. 

Step 8. **Find the optimal hyperparameters** *(Scripts/PythonScripts/Hyperparamters.py)* 

Produces the optimal values for four different Random Forest parameters: (1) n_estimators, (2) max_depth, (3) min_samples_split and (4) min_sample_leaf. 


Step 9. **Compute the accuracy of the developed classifier** *(Scripts/PythonScripts/AccuracyAssessment.py)* 

Gives the (1) confusion matrix, (2) overall accuracy and (3) kappa value of the developed classifier.

Step 10. **Compare the performance of two classifiers (optional)** *(Scripts/PythonScripts/HypothesisTesting.py)* 

Compares two classifiers that make use of different features, based on the kappa values and the associated variances. This script tells whether one classifier is significantly better than another one (95% confidence level). This step is not required.

Step 11. **Save the developed classifier** *(Scripts/PythonScripts/SaveRFmodel.py)* 

The developed classifier can be saved as SAV file. All decisions made in the model are included in this file. Now you can classify a SAR image during breakup. To do so, start with step 1 of the *Generic approach* (see the tutorial described above). 
