"""
This script performs unit tests on the impute_missing_prices function in impute_oil_table.py
"""
import unittest
import impute_oil_table
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal

class test_transformation(unittest.TestCase):
    
    def test_imputer(self):
        assert_frame_equal(
            impute_oil_table.impute_missing_prices(pd.DataFrame({'a':list(range(10)), 'b':[np.nan,2,5,6,7,np.nan,np.nan,np.nan,3,4]})), 
            pd.DataFrame({'a':list(range(10)), 'b':[2.0, 2.0, 5.0, 6.0, 7.0, 5.0, 5.0, 5.0, 3.0, 4.0]}))
        assert_frame_equal(
            impute_oil_table.impute_missing_prices(pd.DataFrame({'a':list(range(10)), 'b':[np.nan,np.nan,5,6,7,8,11,np.nan,np.nan,np.nan]})), 
            pd.DataFrame({'a':list(range(10)), 'b':[5.0, 5.0, 5.0, 6.0, 7.0, 8.0, 11.0, 11.0, 11.0, 11.0]}))
        assert_frame_equal(
            impute_oil_table.impute_missing_prices(pd.DataFrame({'a':list(range(10)), 'b':[np.nan,np.nan,5,np.nan,np.nan,8,11,np.nan,np.nan,np.nan]})), 
            pd.DataFrame({'a':list(range(10)), 'b':[5.0, 5.0, 5.0, 6.5, 6.5, 8.0, 11.0, 11.0, 11.0, 11.0]}))
        assert_frame_equal(
            impute_oil_table.impute_missing_prices(pd.DataFrame({'a':list(range(10)), 'b':[4, np.nan,np.nan,5,8,11,np.nan,3,9,np.nan]})), 
            pd.DataFrame({'a':list(range(10)), 'b':[4.0, 4.5, 4.5, 5.0, 8.0, 11.0, 7.0, 3.0, 9.0, 9.0]}))

if __name__ == '__main__':
    unittest.main()
