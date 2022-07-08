#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import re
import warnings
from colorama import Fore, Style
import pandas as pd 
import numpy as np
import cleaner as cl
from pandas.testing import assert_frame_equal, assert_series_equal



# FUNCTIONS 
##### CLEANING
class TestCleaningModule(unittest.TestCase):

    def test_clean_column_name(self):
        df_test = pd.DataFrame({"ColUmn_1": [1,2,3,np.nan], "COLUMN 2 ":["A", "b", np.nan, "c" ], "COLumN, 3": [1,2,3, "a"], "colUmn: 4":[1,2,3,4]})

        results  = cl.clean_column_name(df_test)
        expected_results = pd.DataFrame({"column 1": [1,2,3,np.nan], "column 2": ["A", "b", np.nan, "c" ], "column 3":[1,2,3, "a"], "column 4":[1,2,3,4]})

        assert_frame_equal(results, expected_results, "Test clean column name method")


    def test_clean_str_column(self):
        df_test = pd.DataFrame({"ColUmn_1": [1,2,3,np.nan], "COLUMN 2 ":["A", "b", np.nan, "c" ], "COLumN, 3": [1,2,3, "a"], "colUmn: 4":[1,2,3,4]})

        results  = cl.clean_str_column(df_test)
        expected_results = pd.DataFrame({"ColUmn_1": [1,2,3,np.nan], "COLUMN 2 ":["a", "b", np.nan, "c" ], "COLumN, 3": [1,2,3, "a"], "colUmn: 4":[1,2,3,4]})

        assert_frame_equal(results, expected_results, "Test clean str name method")


    def test_clean_from_dict(self):
        df_test = pd.DataFrame({"ColUmn_1": [1,2,3,np.nan], "COLUMN 2 ":["A", "b", np.nan, "c" ], "COLumN, 3": [1,2,3, "a"], "colUmn: 4":[1,2,3,4]})

        dict_clean = {"drop_col": ["ColUmn_1"], "replace": {re.compile("^a$"): "replaced a"}, "rename": {"colUmn: 4": "column four"}}
        results = cl.clean_from_dict(df_test, dict_clean)

        expected_results = pd.DataFrame({"COLUMN 2 ":[ "A", "b", np.nan, "c" ], "COLumN, 3": [1,2,3, "replaced a"], "column four":[1,2,3,4]})

        assert_frame_equal(results, expected_results, "Test clean from dict")


##### CHECKING
    def test_cell_type_warnings(table):
        df_test = pd.DataFrame({"ColUmn_1": [1,2,3,np.nan], "COLUMN 2 ":["A", "b", np.nan, "c" ], "COLumN, 3": [1,2,3, "a"], "colUmn: 4":[1,2,3,4]})

        results_1, results_2 = cl.cell_type_warnings(df_test)
        expected_results_1 = pd.DataFrame({"majority_cell_type": [int], "pandas_type": [object]}, index=["COLumN, 3"])
        expected_results_2 = pd.Series([2], index=["COLumN, 3"])

        assert_frame_equal(results_1, expected_results_1, "Test cell type warnings, type comparaison")
        assert_series_equal(results_2, expected_results_2, "Test cell type warnings, type count")


    def test_get_unique_value_col(table, string=False):
        #df_test = pd.DataFrame({"ColUmn_1": [1,2,3,np.nan, np.nan], "COLUMN 2 ":["A", "A", "b", np.nan, "c" ], "COLumN, 3": [1,2,3, "a", 1], "colUmn: 4":[1,2,3,4, 4.0]})

        #results = cl.get_unique_value_col(df_test)
        #expected_results = df_test = pd.DataFrame({"ColUmn_1": [1,2,3,np.nan], "COLUMN 2 ":["A", "b", np.nan, "c" ], "COLumN, 3": [1,2,3, "a"], "colUmn: 4":[1,2,3,4, 4.0]})
        pass

    def test_find_features(self):
       #df_test = pd.DataFrame({"ColUmn_1": [[1,2,3,np.nan]], "COLUMN 2 ": [["A", "b", np.nan, "c" ]], "COLumN, 3": [[1,2,3, "a"]], "colUmn: 4":[[1,2,3,4]]})
        pass


if __name__ == '__main__':
    unittest.main()