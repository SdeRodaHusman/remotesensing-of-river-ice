# remotesensing-of-river-ice
Classify river ice using SAR data

This repository provides material used for the paper: <add a link here>

Overview
========

The repository contains scripts and Python Notebooks which can be used to perform a classify river ice (rubble ice, sheet ice, open water) during breakup using SAR data.

The scripts make use of:
  1) SNAP (version 7.0)
  2) QGIS (version 3.0)
  3) Python Notebooks

Tutorial
========

The overall analysis is performed in a number of steps, starting with the download of all required datasets, such as:

* Synthetic Aperture RADAR data, aqcuired during river breakup (for example; Sentinel-1, via https://scihub.copernicus.eu/)
* Outline of river

The actual steps required for the analysis are quite time consuming and include:

1. Preprocess the SAR images in SNAP (scripts/convert.cmd)
      Produces two shapefiles (polylines and polygons) representing hydrography

2. Split linear hydrography features into small polylines in order to perform the analysis (notebooks/ExplodeShpPolylines.ipynb)

3. Upload results of 2. to Google Fusion Table (UploadToFusionTable.ipynb)

4. Select required catchment boundaries from HydroBASINS. Catchment size should be smaller than current Google Earth Engine download limit!

5. Upload catchments to the Google Fusion Table

6. Prepare regular grid file (grid.kml) and upload to Google Fusion Table, the resulting asset id needs to be updated in the OSM_automatic_NDWI.js script

7. Download SRTM extracts clipped by catchment boundaries (src/javascript/download_SRTM.js)

8. Deleniate drainage network for every sub-catchment DEM from 6. and compute HAND dataset (and all other related hydrological dataset) using python/generate-hydro-datasets-runner.py

9. Convert results of 7. to regular grid tiles and upload to Google Earth Engine as raster assets.

10. Adjust src/javascript/download_water.js do use the new HAND, grid (a copy of src/javascript-ee-playground/OSM_automatic_NDWI.js).

11. Prepare training set for GEE Playground scripts (10.) by performing script runs for a number of tiles, repeat until the results are good for hilly areas,
    For flat areas and sufficient cloud-free images the script should produce good results without any changes

12. Detect surface water mask for every grid tile using src/javascript/download_water.js. src/javascript/templates provides example on how to parallelize water detection.

13. Upload (re-tile if necessart) the resulting water mask to Google Earth Engine

14. Compute positional and thematic accuracy using src/javascript-ee-playground/OSM_compute_buffers_export.js and src/javascript-ee-playground/OSM_stat_per_catchment.js
