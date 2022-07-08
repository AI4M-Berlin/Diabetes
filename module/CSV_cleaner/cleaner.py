#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import warnings
from colorama import Fore, Style
import plotly.express as px
import pandas as pd


# FUNCTIONS 

#### CLEANING 
def clean_column_name(table):
    """ 
    Clean column names 

    put column names in lower case \n
    remove ",", ":", "-" \n
    remove spaces at the beginning and the end of the str \n
    replace '_' by " " 
    
    Args:
        table (pandas dataframe) : dataframe to clean
    
    Returns:
        pandas dataframe: a copy of the dataframe
    """

    table_copy = table.copy()
    table_copy.columns = table_copy.columns.str.lower()
    table_copy.columns = [re.sub('(,)|(:)|(-)', '', x) for x in table_copy.columns]
    table_copy.columns = [re.sub('(_)', ' ', x) for x in table_copy.columns]
    table_copy.columns = [x.strip() for x in table_copy.columns]
    return table_copy


def clean_str_column(table):
    """ 
    Clean string type cell of pandas dataframe  

    put str in lower case \n
    remove ",", ":", "-" \n
    remove spaces at the beginning and the end of the str \n
    replace '_' by " " 
    
    Args:
        table (pandas dataframe) : dataframe to clean
    
    Returns:
        pandas dataframe: a copy of the dataframe
    """
    table_copy = table.copy()
    table_copy = table_copy.applymap((lambda x: str.lower(x) if isinstance(x, str) else x))
    table_copy = table_copy.applymap((lambda x: re.sub('(,)|(:)|(-)', '', x) if isinstance(x, str) else x))
    table_copy = table_copy.applymap((lambda x: re.sub('(_)', ' ', x) if isinstance(x, str) else x))
    table_copy = table_copy.applymap((lambda x: x.strip() if isinstance(x, str) else x))
    return table_copy


def clean_from_dict(table, dictionnary):
    """ 
    Clean dataframe from a dictionnary

    
    Args:
        table (pandas dataframe) : dataframe to clean
        dictionnary (dict) : dictionnary must be: \n
        \t {"drop_col": columns to drop as list, 
        \t "replace": dictionnary of str to replace (see pandas.DataFrame.replace()), 
        \t rename: dictionnary of column to rename pandas.DataFrame.rename()}
    
    Returns:
        pandas dataframe: a copy of the dataframe
    """
    table_copy = table.copy()
    for key, value in dictionnary.items():
        if key == "drop_col":
            table_copy.drop(labels=value, inplace=True, axis='columns', errors="ignore")
        elif key == "replace":
            table_copy.replace(value, regex=True, inplace=True)
        elif key == "rename": 
            table_copy.rename(mapper=value, axis=1, inplace=True)
        else: 
            print(f"{key} is not implemented, check spelling please")
    return table_copy


### CHECKING
def cell_type_warnings(table):
    """    Check if cell type are consistent across columns

    Check if the majority cell type is consistent with dtype (pandas dataframe). Note that str type is considered as equel to object type)
    Check if there are multiple types per column. Note: ignore NA
    
    Args:
        table (pandas.DataFrame): dataframe to clean

    Returns:
        pandas.DataFrame: dataframe with the majority type found per column and dtype of that same column
        pandas.DataFrame: dataframe with type count per column for column with more than one type
    """ 

    table_copy = table.copy()

    warnings.formatwarning = lambda msg, *args, **kwargs: f'{msg}\n'

    cell_type = table_copy.applymap(type).mode().iloc[0]
    type_comparaison = cell_type.compare(table_copy.dtypes)
    
    str_object = type_comparaison[(type_comparaison["self"] == str) & (type_comparaison["other"] == object)].index
    type_comparaison.drop(labels=str_object, axis="index", inplace=True)
    type_comparaison.rename(mapper={"self": "majority_cell_type", "other": "pandas_type"}, axis=1, inplace=True)
    
    if not type_comparaison.empty:
        warnings.warn(f"{Fore.YELLOW}WARNING: dtypes assigned to the following columns are not consistent with the cell type {Style.RESET_ALL}")
        print(f"{type_comparaison}\n")
    
    cell_type_count = table_copy.applymap(type, na_action="ignore").nunique()
    cell_type_count_warning = cell_type_count[cell_type_count != 1]

    if not cell_type_count_warning.empty:
        warnings.warn(f"{Fore.YELLOW}WARNING: Following columns contain multiple data types {Style.RESET_ALL}")
        print(f"{cell_type_count[cell_type_count != 1]}\n")
    
    return type_comparaison, cell_type_count_warning

def get_unique_value_col(table, string=False):
    """
    Computes unique value per column

    Args:
        table (pandas.DataFrame): dataframe to use
        string (bool, optional): Compute unique value only for column of type str. Defaults to False.

    Returns:
        pandas.DataFrame: return pandas dataframe with set of unique value and column name as index
    """
    unique_value = []
    unique_value_str = set()
    for col in table.columns:
        unique_value.append(list(pd.unique(table[col])))
        if string and col != 'patient id':
            unique_value_str.update(set(pd.unique(table[col])))
    
    if string: 
        #even when the column dtype is str, some values are not string
        unique_value_str_clean = unique_value_str.copy()
        for el in unique_value_str:
            if not(isinstance(el, str)):
                unique_value_str_clean.remove(el)
        return(unique_value_str_clean)
    
    return pd.DataFrame({"unique_value": unique_value}, index=table.columns) 


def find_features(table, regex):
    """
    Find column name that either contain regex in its name or in its values

    Args:
        table (pandas.DataFrame): dataframe to use
        regex (regular expression): _description_

    Returns:
        list: column names
    """

    r = re.compile(regex)
    
    #Search in name columns
    results_columns = (set(table.loc[:, table.columns.str.contains(r)].columns))
    
    #Search in values 
    str_columns = table.dtypes[table.dtypes == object].index #str columns
    results_value = table[str_columns].applymap(func=(lambda x: (r.search(x)) if pd.notnull(x) else x)).any()
    
    #combine results
    results_columns.update(results_value[results_value].index)
    
    return results_columns

### PLOTING
def plot_na(table, axis):
    """
    Plot NA count of column or index

    Args:
        table (pandas.DataFrame): _description_
        axis (str or int): {index (0), columns (1)}

    Returns:
        _type_: _description_
    """
    na_count = table.isna().sum(axis=axis).sort_values(ascending=False)
    if axis==0:
        labels={'index': 'features', 'value':'missing value count'}
        fig = px.bar(na_count, height=600, width=2000, labels=labels)

    else:
        labels={'index': 'number of missing value', 'value':'number of patients'}
        fig = px.bar(na_count.value_counts().sort_index(), height=600, width=2000, labels=labels)

    fig.update_layout(font_size=8, bargap=0.3)
    return fig


