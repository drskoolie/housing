## Part 0: Intialization
import pandas as pd

df_bank_rate = pd.read_pickle("data/processed/df_bank_rate.pkl")
df_cpi = pd.read_pickle("data/processed/df_cpi.pkl")
df_crea = pd.read_pickle("data/processed/df_crea.pkl")
df_nhpi = pd.read_pickle("data/processed/df_nhpi.pkl")
df_residential_mortgage_credit = pd.read_pickle(
    "data/processed/df_residential_mortgage_credit.pkl"
)
df_vacancy_metro = pd.read_pickle("data/processed/df_vacancy_metro.pkl")

df_residential_mortgage_credit

## Part 1: Combining into one df
# --> Part 2a: Resampling
df_vacancy_metro_monthly = (
    df_vacancy_metro.resample("MS").first().interpolate(method="linear")
)
df_bank_rate_monthly = df_bank_rate.resample("MS").mean()["bank_rate"]

df = pd.merge_asof(df_crea, df_bank_rate, on="date", direction="nearest")
df = pd.merge_asof(
    df,
    df_vacancy_metro_monthly,
    on="date",
    direction="nearest",
    suffixes=("_bank_rate", "_vacancy"),
)

# Rename the columns for the merged dataframe
df.rename(
    columns={"value_bank_rate": "bank_rate", "value": "vacancy_rate"}, inplace=True
)
# Check for any missing values
print(df.isnull().sum())
