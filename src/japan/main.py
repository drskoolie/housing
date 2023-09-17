## Part 0: Initialization
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style()

df_bank_rate = pd.read_csv("data/raw/japan/bank-rate.csv")
df_cpi = pd.read_csv("data/raw/japan/cpi.csv")
df_hpi = pd.read_csv("data/raw/japan/residential-property-prices.csv")

## Part 1: Data Preprocessing
df_bank_rate.columns = df_bank_rate.columns.str.lower()
df_cpi.columns = df_cpi.columns.str.lower()
df_hpi.columns = df_hpi.columns.str.lower()

df_bank_rate["date"] = pd.to_datetime(df_bank_rate["date"])
df_bank_rate.index = df_bank_rate["date"]
df_bank_rate = df_bank_rate.drop(["date"], axis=1)
df_bank_rate.rename(columns = {df_bank_rate.columns[0]: "bank_rate"}, inplace=True)

df_cpi["date"] = pd.to_datetime(df_cpi["date"])
df_cpi.index = df_cpi["date"]
df_cpi = df_cpi.drop(["date"], axis=1)
df_cpi.rename(columns = {df_cpi.columns[0]: "cpi"}, inplace=True)

df_hpi["date"] = pd.to_datetime(df_hpi["date"])
df_hpi.index = df_hpi["date"]
df_hpi = df_hpi.drop(["date"], axis=1)
df_hpi.rename(columns = {df_hpi.columns[0]: "hpi"}, inplace=True)

df_japan = pd.merge(df_bank_rate, df_cpi, on="date")
df_japan = pd.merge(df_japan, df_hpi, on="date")

## Part 2: Data Engineering
df_japan
