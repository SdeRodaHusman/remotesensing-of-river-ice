# -*- coding: utf-8 -*-
"""
This script is part of the RemoteSensing-of-River-Ice tutorial (https://github.com/SdeRodaHusman/remotesensing-of-river-ice/blob/main/README.md).

This script is used to create the following:
    - Training matrix
    - Validation matrix

Before this step, you need the following folders prepared:
    - Training folder: csv-files of all sample areas that you want to use for training, 
    you only have to do this split (into 70% training data and 30% validation data) 
    for one feature, all the other extracted feature values of sample areas can be 
    in one folder, no splitting required.
    - Validation folder: see explanation above
    - One folder per feature, including all csv-files with sample area values 
    for the feature of interest
    
@author: SdeRodaHusman (contact: S.deRodaHusman@tudelft.nl), created on  Wed Jul  8 14:56:34 2020
"""

# Import libraries
import numpy as np
import pandas as pd
import os
import glob
import re


# -- Uncomment the following lines --

#output_path = os.path.abspath(...)  (Give your output path to save the training-validation feaeture matrices)

######## Indicate paths - training and validation (VV)
# import_training_VV = ... # Give the path of the CSV file with dataset of feature values for all training sample pixels (f.e. with VV intensities)
#csv_files_training = glob.glob(inputdir_training_VV + '*.csv')

# import_validation_VV = ... # Give the path of the CSV file with dataset of feature values for all validation sample pixels (f.e. with VV intensities)
#csv_files_validation = glob.glob(inputdir_validation_VV + '*.csv')


######## Indicate paths - for all other features (of course you can change features to any feature of interest)
#inputdir_VH = ... # Give the path of the CSV file with dataset of VH feature values
#csv_files_VH = glob.glob(inputdir_VH + '*.csv')
#
#inputdir_alpha = ... # Give the path of the CSV file with dataset of Alpha feature values
#csv_files_alpha = glob.glob(inputdir_alpha + '*.csv')
#
#inputdir_anis = ... # Give the path of the CSV file with dataset of Anisotropy feature values
#csv_files_anis = glob.glob(inputdir_anis + '*.csv')
#
#inputdir_entr = ... # Give the path of the CSV file with dataset of Entropy feature values
#csv_files_entr = glob.glob(inputdir_entr + '*.csv')
#
#inputdir_GLCMmean = ... # Give the path of the CSV file with dataset of GLCM mean feature values
#csv_files_GLCMmean = glob.glob(inputdir_GLCMmean + '*.csv')
#
#inputdir_GLCMvar = ... # Give the path of the CSV file with dataset of GLCm variance feature values
#csv_files_GLCMvar = glob.glob(inputdir_GLCMvar + '*.csv')
#
#inputdir_GLCMcor = ... # Give the path of the CSV file with dataset of GLCM correlation feature values
#csv_files_GLCMcor = glob.glob(inputdir_GLCMcor + '*.csv')


# Define functions
def obtain_date_csvfile(csv_filenumber):
        filename_csv = os.path.splitext(csv_filenumber)[0]  # Remove extension from filename
        split_filename_csv = re.split('-|_', filename_csv)  # Split filename
        year = split_filename_csv[10]
        month = split_filename_csv[11]
        day = split_filename_csv[12]
        
        date = '{}-{}-{}'.format(month,day,year)
        number = split_filename_csv[14]
        icestage = split_filename_csv[15]
        return date, number, icestage

# Create training dataset 
df_training = []
for csv_tr in csv_files_training:   
    date_VV = obtain_date_csvfile(csv_tr)[0]   
    number_VV =  obtain_date_csvfile(csv_tr)[1]
    icestage_VV =  obtain_date_csvfile(csv_tr)[2] 
    read_VV = pd.read_csv(csv_tr, sep=',')
    value_VV = 10*np.log10(read_VV['VALUE'])
    
    for csv_VH in csv_files_VH:   
        date_VH = obtain_date_csvfile(csv_VH)[0]   
        number_VH =  obtain_date_csvfile(csv_VH)[1]
        icestage_VH =  obtain_date_csvfile(csv_VH)[2]  
        read_VH = pd.read_csv(csv_VH, sep=',')
        value_VH = 10*np.log10(read_VH['VALUE'])
        depol_ratio = 10*np.log10(read_VH['VALUE'] / read_VV['VALUE'])

        if date_VV == date_VH and number_VV == number_VH and icestage_VV == icestage_VH:
            
            for csv_alpha in csv_files_alpha:
                date_alpha = obtain_date_csvfile(csv_alpha)[0]   
                number_alpha =  obtain_date_csvfile(csv_alpha)[1]
                icestage_alpha =  obtain_date_csvfile(csv_alpha)[2]  
                read_alpha = pd.read_csv(csv_alpha, sep=',')
                value_alpha = read_alpha['VALUE']
             
                if date_VV == date_alpha and number_VV == number_alpha and icestage_VV == icestage_alpha:

                    for csv_anis in csv_files_anis:
                        date_anis = obtain_date_csvfile(csv_anis)[0]   
                        number_anis =  obtain_date_csvfile(csv_anis)[1]
                        icestage_anis =  obtain_date_csvfile(csv_anis)[2]  
                        read_anis = pd.read_csv(csv_anis, sep=',')
                        value_anis = read_anis['VALUE']
                            
                        if date_VV == date_anis and number_VV == number_anis and icestage_VV == icestage_anis:

                            for csv_entr in csv_files_entr:
                                date_entr = obtain_date_csvfile(csv_entr)[0]   
                                number_entr =  obtain_date_csvfile(csv_entr)[1]
                                icestage_entr =  obtain_date_csvfile(csv_entr)[2]  
                                read_entr = pd.read_csv(csv_entr, sep=',')
                                value_entr = read_entr['VALUE']
                                
                                if date_VV == date_entr and number_VV == number_entr and icestage_VV == icestage_entr:

                                    for csv_GLCMmean in csv_files_GLCMmean:
                                        date_GLCMmean = obtain_date_csvfile(csv_GLCMmean)[0]   
                                        number_GLCMmean =  obtain_date_csvfile(csv_GLCMmean)[1]
                                        icestage_GLCMmean =  obtain_date_csvfile(csv_GLCMmean)[2]  
                                        read_GLCMmean = pd.read_csv(csv_GLCMmean, sep=',')
                                        value_GLCMmean = read_GLCMmean['VALUE']
                                        
                                        if date_VV == date_GLCMmean and number_VV == number_GLCMmean and icestage_VV == icestage_GLCMmean:
                                            
                                            for csv_GLCMvar in csv_files_GLCMvar:
                                                date_GLCMvar = obtain_date_csvfile(csv_GLCMvar)[0]   
                                                number_GLCMvar =  obtain_date_csvfile(csv_GLCMvar)[1]
                                                icestage_GLCMvar =  obtain_date_csvfile(csv_GLCMvar)[2]  
                                                read_GLCMvar = pd.read_csv(csv_GLCMvar, sep=',')
                                                value_GLCMvar = read_GLCMvar['VALUE']
                                                
                                                if date_VV == date_GLCMvar and number_VV == number_GLCMvar and icestage_VV == icestage_GLCMvar:
                                                    
                                                    for csv_GLCMcor in csv_files_GLCMcor:
                                                        date_GLCMcor = obtain_date_csvfile(csv_GLCMcor)[0]   
                                                        number_GLCMcor =  obtain_date_csvfile(csv_GLCMcor)[1]
                                                        icestage_GLCMcor =  obtain_date_csvfile(csv_GLCMcor)[2]  
                                                        read_GLCMcor = pd.read_csv(csv_GLCMcor, sep=',')
                                                        value_GLCMcor = read_GLCMcor['VALUE']
                                                        
                                                        if date_VV == date_GLCMcor and number_VV == number_GLCMcor and icestage_VV == icestage_GLCMcor:
                                                          
                                                            df_S1 = pd.DataFrame({'VV_intensity': value_VV, 'VH_intensity': value_VH, 'Depol_ratio': depol_ratio, 'Alpha': value_alpha,  'Anisotropy': value_anis, 'Entropy': value_entr, 'GLCM_mean': value_GLCMmean, 'GLCM_variance': value_GLCMvar, 'GLCM_correlation': value_GLCMcor, 'IceStage': icestage_VV, 'number': number_VV, 'date': date_VV})
                                                            df_S1 = df_S1.dropna()
                                                            df_S1_sample = df_S1.sample(n = 100, replace=True)
                                                            df_training.append(df_S1_sample)
                                    
df_training_all = pd.concat(df_training, axis=0)
df_training_all = df_training_all.dropna() # Remove rows with nan value in column

# Create DataFrame formats
df_training_intensity = df_training_all[['VV_intensity', 'VH_intensity', 'Depol_ratio', 'IceStage', 'number', 'date']]
df_training_polarimetric = df_training_all[['Alpha', 'Anisotropy', 'Entropy', 'IceStage', 'number', 'date']]
df_training_texture = df_training_all[['GLCM_mean', 'GLCM_variance', 'GLCM_correlation', 'IceStage', 'number', 'date']]


# Create validation dataset 
df_validation = []
for csv_tr in csv_files_validation:   
    date_VV = obtain_date_csvfile(csv_tr)[0]   
    number_VV =  obtain_date_csvfile(csv_tr)[1]
    icestage_VV =  obtain_date_csvfile(csv_tr)[2] 
    read_VV = pd.read_csv(csv_tr, sep=',')
    value_VV = 10*np.log10(read_VV['VALUE'])
    
    for csv_VH in csv_files_VH:   
        date_VH = obtain_date_csvfile(csv_VH)[0]   
        number_VH =  obtain_date_csvfile(csv_VH)[1]
        icestage_VH =  obtain_date_csvfile(csv_VH)[2]  
        read_VH = pd.read_csv(csv_VH, sep=',')
        value_VH = 10*np.log10(read_VH['VALUE'])
        depol_ratio = 10*np.log10(read_VH['VALUE'] / read_VV['VALUE'])

        if date_VV == date_VH and number_VV == number_VH and icestage_VV == icestage_VH:
            
            for csv_alpha in csv_files_alpha:
                date_alpha = obtain_date_csvfile(csv_alpha)[0]   
                number_alpha =  obtain_date_csvfile(csv_alpha)[1]
                icestage_alpha =  obtain_date_csvfile(csv_alpha)[2]  
                read_alpha = pd.read_csv(csv_alpha, sep=',')
                value_alpha = read_alpha['VALUE']
             
                if date_VV == date_alpha and number_VV == number_alpha and icestage_VV == icestage_alpha:

                    for csv_anis in csv_files_anis:
                        date_anis = obtain_date_csvfile(csv_anis)[0]   
                        number_anis =  obtain_date_csvfile(csv_anis)[1]
                        icestage_anis =  obtain_date_csvfile(csv_anis)[2]  
                        read_anis = pd.read_csv(csv_anis, sep=',')
                        value_anis = read_anis['VALUE']
                            
                        if date_VV == date_anis and number_VV == number_anis and icestage_VV == icestage_anis:

                            for csv_entr in csv_files_entr:
                                date_entr = obtain_date_csvfile(csv_entr)[0]   
                                number_entr =  obtain_date_csvfile(csv_entr)[1]
                                icestage_entr =  obtain_date_csvfile(csv_entr)[2]  
                                read_entr = pd.read_csv(csv_entr, sep=',')
                                value_entr = read_entr['VALUE']
                                
                                if date_VV == date_entr and number_VV == number_entr and icestage_VV == icestage_entr:

                                    for csv_GLCMmean in csv_files_GLCMmean:
                                        date_GLCMmean = obtain_date_csvfile(csv_GLCMmean)[0]   
                                        number_GLCMmean =  obtain_date_csvfile(csv_GLCMmean)[1]
                                        icestage_GLCMmean =  obtain_date_csvfile(csv_GLCMmean)[2]  
                                        read_GLCMmean = pd.read_csv(csv_GLCMmean, sep=',')
                                        value_GLCMmean = read_GLCMmean['VALUE']
                                        
                                        if date_VV == date_GLCMmean and number_VV == number_GLCMmean and icestage_VV == icestage_GLCMmean:
                                            
                                            for csv_GLCMvar in csv_files_GLCMvar:
                                                date_GLCMvar = obtain_date_csvfile(csv_GLCMvar)[0]   
                                                number_GLCMvar =  obtain_date_csvfile(csv_GLCMvar)[1]
                                                icestage_GLCMvar =  obtain_date_csvfile(csv_GLCMvar)[2]  
                                                read_GLCMvar = pd.read_csv(csv_GLCMvar, sep=',')
                                                value_GLCMvar = read_GLCMvar['VALUE']
                                                
                                                if date_VV == date_GLCMvar and number_VV == number_GLCMvar and icestage_VV == icestage_GLCMvar:
                                                    
                                                    for csv_GLCMcor in csv_files_GLCMcor:
                                                        date_GLCMcor = obtain_date_csvfile(csv_GLCMcor)[0]   
                                                        number_GLCMcor =  obtain_date_csvfile(csv_GLCMcor)[1]
                                                        icestage_GLCMcor =  obtain_date_csvfile(csv_GLCMcor)[2]  
                                                        read_GLCMcor = pd.read_csv(csv_GLCMcor, sep=',')
                                                        value_GLCMcor = read_GLCMcor['VALUE']
                                                        
                                                        if date_VV == date_GLCMcor and number_VV == number_GLCMcor and icestage_VV == icestage_GLCMcor:
                                                          
                                                            df_S1 = pd.DataFrame({'VV_intensity': value_VV, 'VH_intensity': value_VH, 'Depol_ratio': depol_ratio, 'Alpha': value_alpha,  'Anisotropy': value_anis, 'Entropy': value_entr, 'GLCM_mean': value_GLCMmean, 'GLCM_variance': value_GLCMvar, 'GLCM_correlation': value_GLCMcor, 'IceStage': icestage_VV, 'number': number_VV, 'date': date_VV})
                                                            df_S1 = df_S1.dropna()
                                                            df_S1_sample = df_S1.sample(n = 100, replace=True)
                                                            df_validation.append(df_S1_sample)
                                    
df_validation_all = pd.concat(df_validation, axis=0)
df_validation_all = df_validation_all.dropna() # Remove rows with nan value in column

# Create DataFrame formats
df_validation_intensity = df_validation_all[['VV_intensity', 'VH_intensity', 'Depol_ratio', 'IceStage', 'number', 'date']]
df_validation_polarimetric = df_validation_all[['Alpha', 'Anisotropy', 'Entropy', 'IceStage', 'number', 'date']]
df_validation_texture = df_validation_all[['GLCM_mean', 'GLCM_variance', 'GLCM_correlation', 'IceStage', 'number', 'date']]


# Write to CSV file - training
df_training_all.to_csv(os.path.join(output_path, 'S1_Training.csv'), index = False, header=True)    
df_training_intensity.to_csv(os.path.join(output_path, 'S1_Training_Intensity.csv'), index = False, header=True)    
df_training_texture.to_csv(os.path.join(output_path, 'S1_Training_Texture.csv'), index = False, header=True)    
df_training_polarimetric.to_csv(os.path.join(output_path, 'S1_Training_Polarimetric.csv'), index = False, header=True)    

# Write to CSV file - validation
df_validation_all.to_csv(os.path.join(output_path, 'S1_Validation.csv'), index = False, header=True)    
df_validation_intensity.to_csv(os.path.join(output_path, 'S1_Validation_Intensity.csv'), index = False, header=True)    
df_validation_texture.to_csv(os.path.join(output_path, 'S1_Validation_Texture.csv'), index = False, header=True)    
df_validation_polarimetric.to_csv(os.path.join(output_path, 'S1_Validation_Polarimetric.csv'), index = False, header=True)    
