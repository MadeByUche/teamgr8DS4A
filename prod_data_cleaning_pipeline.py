from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import seaborn as sns
import pandas as pd
import numpy as np
import requests
import base64
import json
import re
import os
from cms_data_prepration import clean_and_prepare_dataset
import dataset_info as d_info

NAN_REPLACEMENT_STR_KEY_LST = ["Not "]

DATA_FILES_TO_CLEAN = {
    "hospital_general_information": {
        'file_name': "hospital_general_information.csv",
        'data_info': d_info.hospital_general_information_info
    },
    "patient_experience_care_domain_scores": {
        'file_name': "patient_experience_care_domain_scores.csv",
        'data_info': d_info.patient_experience_care_domain_scores_info
    },
    "complications_and_deaths": {
        'file_name': "complications_and_deaths.csv",
        'data_info': d_info.complications_and_deaths_info
    },
    "hospital_hchaps": {
        'file_name': "hospital_hchaps.csv",
        'data_info': d_info.hospital_hchaps_info
    },
    "timely_effective_care_hospital": {
        'file_name': "timely_effective_care_hospital.csv",
        'data_info': d_info.timely_effective_care_hospital_info
    },
    "hospital_value_based_performance": {
        'file_name': "hospital_value_based_performance.csv",
        'data_info': d_info.hospital_value_based_performance_info
    },
    # "us_city_population_estimates": {
    #     'file_name': "us_city_population_estimates.csv",
    #     'data_info': d_info.hospital_value_based_performance_info
    # },
}

# TODO(anewla): build pipeline to generate this table
ANALYSIS_DATA_FILES = {
    # what are the various views that we would like for our analysis?
    "prod_data": {
        "input": [],
        "output": ""
    },
}


def read_csv(df_name, path):
    df = None
    with open(path, 'r'):
        df = pd.read_csv(path)
    df.name = df_name
    return df


def write_csv(df, file_path, index=False):
    df.to_csv(file_path, index=index)


def main(raw_dir="raw", output_dir="cleaned", write=False, process_list=[], data_files_info=DATA_FILES_TO_CLEAN, print_samples=False, read_csv=read_csv, write_csv=write_csv):
    df_dict = {}
    for name, info in data_files_info.items():
        if not process_list or name in process_list:
            curr_file_name = data_files_info[name]['file_name']
            curr_df = read_csv(name, os.path.join(raw_dir, curr_file_name))
            df_dict[name] = clean_and_prepare_dataset(
                curr_df,
                name,
                info['data_info'],
                nan_replacement_str_key_lst=NAN_REPLACEMENT_STR_KEY_LST
            )
    if print_samples:
        column_batch = 5
        sample_size = 10
        for k in df_dict:
            print(f"name: {k}\ndtypes\n{df_dict[k].dtypes}\n\n")
            for i in range(0, len(df_dict[k].columns), column_batch):
                print(df_dict[k].sample(sample_size).iloc[:, i:i + column_batch].to_string())
            print()
    if write:
        for name in df_dict:
            curr_file_name = data_files_info[name]['file_name']
            write_csv(df_dict[name], os.path.join(output_dir, curr_file_name))
    return df_dict


if __name__ == '__main__':
    main()
