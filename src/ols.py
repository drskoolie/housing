## Part 0: Initialization
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.crea import df_crea

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
    df_crea["Average Price_Canada_Unadjusted"],
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

df = df.rename(columns={"Average Price_Canada_Unadjusted": "crea"})
df = df.set_index(["date"])
df["crea_pct_change"] = df["crea"].pct_change(12) * 100
window_shift = 24
df["crea_pct_change_moving_average"] = df["crea_pct_change"].rolling(window=window_shift).mean()
df["real_interest"] = df["bank_rate"] - df["crea_pct_change_moving_average"]
df.dropna(inplace=True)

shift = 0
df["crea_lagged"] = df["crea"].shift(-shift)
df["crea_pct_change_moving_average_lagged"] = df["crea_pct_change_moving_average"].shift(-window_shift)

df.dropna(inplace=True)
X = df[["real_interest", "vacancy_rate", "crea_pct_change_moving_average_lagged"]]
X = df[["real_interest", "vacancy_rate"]]
Y = df["crea_lagged"]
X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()
print(model.summary())
