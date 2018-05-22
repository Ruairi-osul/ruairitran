# ephys
Set up for code sharing between sharplab, Oxford and the lab of Dr Kongfatt Wong-Lin, Ulster University

Contains code scripts for preprocessing and analysis of EEG and silicon probe data.

Ruairi O'Sullivan and Tran Tran 2018

## How to run the python code
Requires libraries associated with an anaconda python install: https://conda.io/docs/user-guide/install/download.html

  - Clone the repository and install anaconda
  - Find the script you would like to run and open its associated \*_\_config.py*_ in a text editor
  - Edit the parameters of the Options object
  - Save and run the config file at the command line

## Directories

Note: Some scripts in analysis directories are dependant on intemetiary .csv files created by the preprocessessing scripts. Make sure to read the documentation at the top of each script before running it.

### eeg_preprocess
Contains two scripts for preprocessing of raw EEG data stored in .continuous files.

#### create_eeg_dat
Packs data from many .continuous EEG files into one binary .dat file.

#### pds
Create a csv file of power spectral density overtime. 

### mua_preprocess
Contains scirpts for reading raw EEG data stored in .continuous files, applying filters and writing to a .dat file

### post_kilosort
read output of kilosort into tidy .csv files. Extract characteristics of good clusters and describe their firing patterns

### eeg_analysis
Plot spectrograms, mean power density plots etc. 

