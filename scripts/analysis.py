import os
import shutil
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml

data_parameters = './parameters/data.yml'
param_development_small = './parameters/sofia_dev_small.par'

data_path = 'data'
results_path = 'results'

dev_small_cat = './results/development_small/developement_small_cat.txt'

def download_data(data_parameters, force=False):
    if not os.path.isdir(data_path):
        os.mkdir(data_path)
        
    with open(data_parameters, "r") as f:
        data_yml = yaml.load(f, Loader=yaml.FullLoader)

    for dataset in data_yml.keys():
        print(dataset)
        dataset_dir = os.path.join(data_path, dataset)
        if force == True:
            shutil.rmtree(dataset_dir)

        if not os.path.isdir(dataset_dir):
            pathname = data_yml[dataset]['path']
            os.mkdir(dataset_dir)
            for filename in data_yml[dataset]['files']:
                command = f'wget --no-check-certificate "{pathname}download?path=%2F&files={filename}" -O {dataset_dir}/{filename}'
                print(command)
                os.system(command)

def run_sofia(parameters, outputdir):
    """Only executed if directory does not exist"""
    if not os.path.isdir(results_path):
        os.mkdir(results_path)
        
    if not os.path.isdir(os.path.join(results_path, outputdir)):
        os.mkdir(os.path.join(results_path, outputdir))
        command = f"sofia {parameters}"
        print(command)
        os.system(command)
    return

def read_sofia_header(filename):
    with open(filename, 'r') as f:
        head_line = f.readlines()[10]
    head = re.split('\s+', head_line.strip('\n'))[1:] # 1: to remove #
    return head
        
def sofia2cat(catalog):
    head = read_sofia_header(catalog)
    raw_cat = pd.read_csv(catalog, delim_whitespace=True, header=None, names=head, comment='#')
    raw_cat.sort_values(by='f_sum', ascending=False, inplace=True)
    raw_cat_filtered = raw_cat[raw_cat['kin_pa']>0]
    print(raw_cat_filtered[['x', 'y', 'ell_maj', 'f_sum', 'freq', 'kin_pa', 'w20']])
    return raw_cat_filtered


def main():
    download_data(data_parameters, force=False)
    run_sofia(parameters=param_development_small,
              outputdir='development_small')
    raw_cat = sofia2cat(catalog=dev_small_cat)
    # Now needs to convert the sofia raw sofia catalog that has 
    # 'x', 'y', 'ell_maj', 'f_sum', 'freq', 'kin_pa', 'w20'
    # to
    # id ra dec hi_size line_flux_integral central_freq pa i w20
    # with the right physical units

if __name__ == "__main__":                
    main()

