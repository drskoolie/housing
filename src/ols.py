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
    df_crea["Average Price_Canada_Adjusted"],
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

df = df.rename(columns={"Average Price_Canada_Adjusted": "crea"})
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


## Part 4: Plotting
fig, ax = plt.subplots(1, 2, figsize=(18,9))
sns.lineplot(
    ax=ax[0],
    data=df_crea,
    x=df_crea.index,
    y="Average Price_Canada_Unadjusted",
    color="blue",
)

ax[0].set_title(df_crea["Average Price_Canada_Unadjusted"].name)
ax[0].fill_between(
    df_crea.index,
    df_crea["Average Price_Canada_Unadjusted"],
    alpha=0.1,
    color="blue",
)
df_crea["pct_change"] = df_crea["Average Price_Canada_Unadjusted"].pct_change(periods=12) * 100

sns.lineplot(
    ax=ax[1],
    data=df_crea,
    x=df_crea.index,
    y="pct_change",
    color="blue",
)
ax[1].set_title(df_crea["Average Price_Canada_Unadjusted"].name)
plt.show()
