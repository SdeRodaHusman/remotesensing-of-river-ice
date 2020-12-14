# remotesensing-of-river-ice

This repository provides material used for the paper: <add a link here> ...

Overview
========

River ice during breakup can be classified using the generic Random Forest classifier, which was trained for the Athabasca River, Alberta using Sentinel-1 SAR data (RFmodel/S1_RFmodel_AthabascaRiver.sav). Another option is to train a Random Forest model based on new training data. The tutorial to do so is provided below. 

The repository contains scripts and models which can be used to perform a classify river ice (rubble ice, sheet ice, open water) during breakup using SAR data.

The scripts make use of:
  1) SNAP (version 7.0)
  2) QGIS (version 3.0)
  3) Python (e.g. Spyder, Anaconda version 3.0)

![alt text](https://github.com/SdeRodaHusman/remotesensing-of-river-ice/blob/main/Figures/Roadmap_RFmodel.jpg?raw=true)


Tutorial
========

The overall analysis and classification is performed in a number of steps, starting with the download of all required datasets, such as:

* Synthetic Aperture RADAR data, aqcuired during river breakup (for example; Sentinel-1, via https://scihub.copernicus.eu/)
* Outline of river of interest (outines of the Peace River and Athabasca River can be found in Data/OutlinePeaceAthabascaRiver)

The actual steps required for the analysis are quite time consuming and include:

1. Preprocess the raw SAR data (Scripts/XLMgraphs/...)
      Produces preprocessed NetCDF files for (1) intensity, (2) polarimetric and (3) texture features. XML graphs can be used in SNAP or using the provided GPT script    (Scripts/GPTscript.bat)

2. Load the preprocessed NetCDFs in QGIS and create sample areas from which the ice stage is known. It is recommended to create a total of 70 sample areas from 100 pixels each, for all ice stage (rubble ice, sheet ice and open water) of interest. Hence, 210 sample areas (or 21000 pixels) will be created. 

3. Extract feature values for all sample pixels, use .csv as output. This can be done in QGIS (Scripts/QGISmodels/ExtractFeatureValues.model3). 

4. Split the extracted sample areas randomly for each ice stage: 50 for training, 20 for validation.

5. Select the optimal, non-correlated features (Scripts/PythonScripts/FeatureSelection.py).

6. Compute the appropriate hyperparameters for the Random Forest model (Scripts/PythonScripts/Hyperparameters.py) using validation curves.

7. Create classification maps for preprocessed SAR images (Scripts/PythonScripts/ClassificationMaps.py).

8. Assess the accuracy of the developed classifier (Scripts/PythonScripts/AccuracyAssessment.py). Optional: compare whether a combination of features performs significantly better than another combination (Scripts/PythonScripts/HypothesisTesting.py).
