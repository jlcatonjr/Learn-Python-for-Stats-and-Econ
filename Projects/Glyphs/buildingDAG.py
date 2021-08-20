import pandas as pd
import pingouin as pg


def gen_DAG(df, method = "pearson", sig = 0.05):
    # Correlation type:
    # 'pearson': Pearson r product-moment correlation
    # 'spearman': Spearman ρ rank-order correlation
    # 'kendall': Kendall’s τB correlation (for ordinal data)
    # 'bicor': Biweight midcorrelation (robust)
    # 'percbend': Percentage bend correlation (robust)
    # 'shepherd': Shepherd’s pi correlation (robust)
    # 'skipped': Skipped correlation (robust)
    pcs_dct = {}
    sig_corr_dct = {}
    for x in df.keys():
        sig_corr_dct[x] = []
        pcs_dct[x]={}
        for y in df.keys():
            # control variables
            # select variables that are not x or y
            other_vars = [z for z in df.keys() if z != y and z != x ]
            if x == y:
                # No need to calculate if the variable is itself
                pcs_dct[x][y] = 1
            else:
                pcs_dct[x][y] = df.partial_corr(x=x,y=y, covar=other_vars,
                                      method=method).round(3)
                if pcs_dct[x][y]["p-val"].values[0] < sig:
                    sig_corr_dct[x].append((y, pcs_dct[x][y]["r"].values[0]))

    return pcs_dct, sig_corr_dct

df = pd.read_excel("dataWithSomeReformatting.xlsx", index_col = [0])
keys = ["General_outcome", 
         'Current Impact_Factor',
         #'Impact_F_Publishing_Year',
         'Num_Citations',
         'Public',
         'Private',
         'University',
         'International',
         'Research']

# select small set of variables to include in dataframe
pc_df = df[keys]#.dropna(axis=0, how = "any")



pcs_dct, sig_corrs = gen_DAG(pc_df, sig = .1, method="pearson")


print(pcs_dct)
print(sig_corrs)