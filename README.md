# remotesensing-of-river-ice

This repository provides material used for the paper: <add a link here> ...

Overview
========

River ice during breakup can be classified using a Random Forest classifier. The repository contains scripts and models which can be used to perform a classify river ice (rubble ice, sheet ice, open water) during breakup using SAR data.

The scripts make use of:
  1) SNAP (version 8.0)
  2) QGIS (version 3.0)
  3) Python (e.g. Spyder, Anaconda version 3.0)

There are two paths in this tutorial that can be used for classification (also see the figure below), namely:
- **Option 1:** Generic approach (use the developed classifier presented in the paper, which was trained for the Athabasca River, Alberta using Sentinel-1 SAR data)
- **Option 2:** Build your own Random Forest classifier (follow this step when you want to build your own classifier, e.g. when you want to classify another river or use data from a SAR mission that is differently polarized than Sentinel-1 (VV-VH). 

The steps needed for the first and second path are described below.

![alt text](https://github.com/SdeRodaHusman/remotesensing-of-river-ice/blob/main/Figures/Roadmap_RFmodel.jpg?raw=true)


Tutorial - Generic approach
========

The overall analysis and classification is performed in a number of steps, starting with the download of all required datasets, such as:

* Devoloped Random Forest classifier (this can be found in RFmodel/S1_RFmodel_AthabascaRiver.sav)
* Outline of river of interest (outines of the Peace River and Athabasca River can be found in Data/OutlinePeaceAthabascaRiver)

The actual steps required for the analysis are quite time consuming and include:

Step 1. **Download Sentinel-1 SLC SAR images**

Download SAR images that you would like to classify, for example via https://scihub.copernicus.eu/)

Step 2. **Preprocess Senitnel-1 SLC SAR images** *(Scripts/XLMgraphs/S1_Intensity.xml, Scripts/XLMgraphs/S1_Texture.xml)*

Produces preprocessed NetCDF files for (1) intensity and (2) texture features. XML graphs can be used in SNAP or using the provided GPT script *(Scripts/GPTscript.bat)*

Step 3. **Combine all preprocessed images into one NetCDF file** *(Scripts/XLMgraphs/CombinePreprocessedImages.xml)*

Combines the preprocessed intensity and texture images by using the *Collocation* option in SNAP. 

Step 4. **Create CSV file with all features** *(Scripts/PythonScripts/CreateFeatureMatrix_SARimage.py)*

Produces a CSV file with VH intensity and GLCM mean values for all pixels of the SAR image of interest.

Step 5. **Perform Random Forest classification** *(Scripts/PythonScripts/ClassifySARimage.py)* 

Creates a NetCDF file in which all pixels are classified as sheet ice, rubble ice or open water. 



Tutorial - Build your own Random Forest classifier
========

The overall analysis and classification is performed in a number of steps, starting with the download of all required datasets, such as:

* Devoloped Random Forest classifier (this can be found in RFmodel/S1_RFmodel_AthabascaRiver.sav)
* Outline of river of interest (outines of the Peace River and Athabasca River can be found in Data/OutlinePeaceAthabascaRiver)

The actual steps required for the analysis are quite time consuming and include:

Step 1. **Download Sentinel-1 SLC SAR images**

Download SAR images that you would like to classify, for example via https://scihub.copernicus.eu/)

Step 2. **Preprocess Senitnel-1 SLC SAR images** *(Scripts/XLMgraphs/S1_Intensity.xml, Scripts/XLMgraphs/S1_Texture.xml)*

Produces preprocessed NetCDF files for (1) intensity and (2) texture features. XML graphs can be used in SNAP or using the provided GPT script *(Scripts/GPTscript.bat)*

Step 3. **Combine all preprocessed images into one NetCDF file** *(Scripts/XLMgraphs/CombinePreprocessedImages.xml)*

Combines the preprocessed intensity and texture images by using the *Collocation* option in SNAP. 

Step 4. **Create CSV file with all features** *(Scripts/PythonScripts/CreateFeatureMatrix_SARimage.py)*

Produces a CSV file with VH intensity and GLCM mean values for all pixels of the SAR image of interest.

Step 5. **Perform Random Forest classification** *(Scripts/PythonScripts/ClassifySARimage.py)* 

Creates a NetCDF file in which all pixels are classified as sheet ice, rubble ice or open water. 


2. Load the preprocessed NetCDFs in QGIS and create sample areas from which the ice stage is known. It is recommended to create a total of 70 sample areas from 100 pixels each, 
for all ice stage (rubble ice, sheet ice and open water) of interest. Hence, 210 sample areas (or 21000 pixels) will be created. 

3. Extract feature values for all sample pixels, use .csv as output. This can be done in QGIS (Scripts/QGISmodels/ExtractFeatureValues.model3). 

4. Split the extracted sample areas randomly for each ice stage: 50 for training, 20 for validation.

5. Select the optimal, non-correlated features (Scripts/PythonScripts/FeatureSelection.py).

6. Compute the appropriate hyperparameters for the Random Forest model (Scripts/PythonScripts/Hyperparameters.py) using validation curves.

7. Create classification maps for preprocessed SAR images (Scripts/PythonScripts/ClassificationMaps.py).

8. Assess the accuracy of the developed classifier (Scripts/PythonScripts/AccuracyAssessment.py). Optional: compare whether a combination of features performs significantly better than another combination (Scripts/PythonScripts/HypothesisTesting.py).
