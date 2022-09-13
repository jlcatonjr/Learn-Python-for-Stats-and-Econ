from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.api import VAR
import statsmodels.api as sm
import copy
import pingouin
from scipy.stats import pearsonr
p_val = .05



def adfuller_df(df, maxlag, regression = "c"):
    dct = {}
    for key, val in df.items():
        dct[key] = adfuller(val, maxlag=maxlag, autolag = "aic", regression = regression)[1]#.pvalue

    return dct

def cointegration_df(df):
    dct = {}
    for key1 in df:
        dct[key1] = {}
        for key2 in df:
            if key1 == key2:
                dct[key1][key2] = np.nan
            else:
                dct[key1][key2] = coint_johansen(df[[key1,key2]], det_order=0, k_ar_diff=1).lr1
    return pd.DataFrame(dct)
