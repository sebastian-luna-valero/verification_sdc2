import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml

data_parameters = 'parameters/data.yml'
data_path = './data'

def download_data(data_parameters, force=False):
    if not os.path.isdir(data_path):
        os.mkdir(data_path)
        
    with open(data_parameters, "r") as f:
        data_yml = yaml.load(f, Loader=yaml.FullLoader)

    for dataset in data_yml.keys():
        print(dataset)
        if force == True:
            shutil.rmtree(f"{data_path}/{dataset}")

        if not os.path.isdir(f"{data_path}/{dataset}"):
            pathname = data_yml[dataset]['path']
            os.mkdir(f"{data_path}/{dataset}")
            for filename in data_yml[dataset]['files']:
                command = f'wget --no-check-certificate "{pathname} download?path=%2F&files={filename}" -O {data_path}/{dataset}/{filename}'
                print(command)
                os.system(command)

download_data(data_parameters)

## Download data
#is os.path.isfile
#cat_file = './test2/sofia_test_output_cat.txt'
#
#truth_file = '../data/development/sky_dev_truthcat.txt'
#truth = pd.read_csv(truth_file, delim_whitespace=True)
#
##cat = np.genfromtxt(cat_file)
#names = open(cat_file, 'r').readlines()[10][1:-1].split(None)
#cat = pd.read_csv(cat_file, delim_whitespace=True, comment='#', names=names)
#
## Work with bright source to the left to check values
#x0, y0 = 23, 341
#cond = np.sqrt((cat['x']-x0)**2 + (cat['y']-y0)**2) < 5
#source = cat[cond].iloc[0]
#
#print(source[['x', 'y', 'ell_maj', 'f_sum', 'freq', 'kin_pa', 'w20']])
#print(truth.iloc[np.argmax(truth['line_flux_integral'])])

