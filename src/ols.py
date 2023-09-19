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
df["bank_rate_cumsum"] = df["bank_rate"].cumsum()
df.dropna(inplace=True)
df['time_trend'] = range(len(df))

shift = 6
df["crea_lagged"] = df["crea"].shift(-shift)

df.dropna(inplace=True)
X = df[["bank_rate_cumsum", "time_trend"]]
Y = df["crea_lagged"]
X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()
print(model.summary())
