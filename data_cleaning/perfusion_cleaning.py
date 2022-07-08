#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys 
sys.path.append('../module/CSV_cleaner')

# Libraries
import argparse
import pandas as pd
import pickle
import re
import numpy as np
import cleaner as cl


# Constants
default_filepath = "../data/cerebral_perfusion_data/data_description/GE-75_data_summary_table.csv"
#python perfusion_cleaning.py -p ../data/cerebral_perfusion_data/data_description/GE-75_data_summary_table.csv -v -o clean_data/perfusion_v1.csv


# Arguments
parser = argparse.ArgumentParser(description='data cleaning arguments for the perfusion dataset')
parser.add_argument('--path', '-p', type=str, required=False, default=default_filepath,
                    help='filepath to the perfusion dataset [default:../data/cerebral_perfusion_data/data_description/GE-75_data_summary_table.csv]')
parser.add_argument('--output', '-o', type=str, required=False, default='output.csv',
                    help='[default: output.csv]')
parser.add_argument('--threshold', '--t', required=False, type=float, default=(2/3), help='keep column with t-percentage of non missing value, drop otherwise, [default: 2/3')
parser.add_argument('-v', '--verbose', required=False, action="store_true", help='Talk a lot.')

args = parser.parse_args()


# Data Loading
pickle_in = open("perfusion_dict.pkl","rb")
perfusion_dict = pickle.load(pickle_in)

df = pd.read_csv(args.path)

# Cleaning

## Missing data
if args.verbose:
    print('Missing data')
df.dropna(how='all', axis='columns', inplace=True)
df.dropna(how='all', axis='index', inplace=True)

##  String cleaning
if args.verbose:
    print('String cleaning')
df = cl.clean_column_name(df)
df = cl.clean_str_column(df)

## Clean from file
if args.verbose:
    print('Cleaning from file')
df = cl.clean_from_dict(df, perfusion_dict)


## Inconsistency
### patients annotated with and without diabetes
inconsistent_patients_index = df[df["patient id"].isin(perfusion_dict["drop_row"])].index
df.drop(labels=inconsistent_patients_index, axis='index', inplace=True)

### wrong column type
df["dm family history"] = pd.to_numeric(df["dm family history"], errors='ignore', downcast='integer')

## Missing value
if args.verbose:
    print('Missing value')
thresh = args.threshold
df = df.dropna(thresh=len(df)*thresh, axis='columns')


# Write file
df.to_csv(args.output, index=False, encoding='utf-8')
print(f"file written to {(args.output)}")