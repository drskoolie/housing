## Part 0: Initialization
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.crea import df_crea

from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tsa.stattools import grangercausalitytests
import statsmodels.api as sm

pd.options.mode.chained_assignment = None  # default='warn'
sns.set_style("whitegrid")

df_cpi = pd.read_pickle("data/processed/df_cpi.pkl")
df_bank_rate = pd.read_pickle("data/processed/df_bank_rate.pkl")
df_nhpi = pd.read_pickle("data/processed/df_nhpi.pkl")
df_vacancy_metro = pd.read_pickle("data/processed/df_vacancy_metro.pkl")


## Part 2: Regression Analysis
df_vacancy_metro_monthly = df_vacancy_metro.resample("MS").first()
df_vacancy_metro_monthly = df_vacancy_metro_monthly.interpolate(method="linear")

df = pd.merge_asof(
    df_crea["Dollar Volume_Canada_Unadjusted"],
    df_bank_rate,
    on="date",
    direction="nearest",
)
df = pd.merge_asof(
    df,
    df_vacancy_metro_monthly,
    on="date",
    direction="nearest",
    suffixes=("_bank_rate", "_vacancy"),
)

df = df.rename(columns={"Dollar Volume_Canada_Unadjusted": "crea"})
df = df.set_index(["date"])

## Part 3: Run Models
shift = 6
df["crea_lagged"] = df["crea"].shift(-shift)

df.dropna(inplace=True)
X = df[["bank_rate", "vacancy_rate"]]
Y = df["crea_lagged"]
X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()
print(model.summary())


"""
                            OLS Regression Results
==============================================================================
Dep. Variable:            crea_lagged   R-squared:                       0.440
Model:                            OLS   Adj. R-squared:                  0.438
Method:                 Least Squares   F-statistic:                     201.8
Date:                Sat, 16 Sep 2023   Prob (F-statistic):           2.03e-65
Time:                        18:16:07   Log-Likelihood:                -12465.
No. Observations:                 517   AIC:                         2.494e+04
Df Residuals:                     514   BIC:                         2.495e+04
Df Model:                           2
Covariance Type:            nonrobust
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------
const         2.008e+10   1.12e+09     17.951      0.000    1.79e+10    2.23e+10
bank_rate    -1.429e+09   7.12e+07    -20.078      0.000   -1.57e+09   -1.29e+09
vacancy_rate -8.701e+08   3.49e+08     -2.495      0.013   -1.56e+09   -1.85e+08
==============================================================================
Omnibus:                      206.425   Durbin-Watson:                   0.155
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              780.017
Skew:                           1.834   Prob(JB):                    4.18e-170
Kurtosis:                       7.770   Cond. No.                         27.1
==============================================================================
"""

