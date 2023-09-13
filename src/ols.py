## Part 0: Initialization
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tsa.stattools import grangercausalitytests
import statsmodels.api as sm

pd.options.mode.chained_assignment = None  # default='warn'
sns.set_style("whitegrid")

## Part 1: Data Importing
df_vacancy_metro = pd.read_csv("data/processed/vacancy-metro.csv", index_col=False)
df_bank_rate = pd.read_csv("data/processed/bank-rate.csv", index_col=False)
df_hpi = pd.read_csv("data/processed/hpi.csv", index_col=False)
df_new_hpi = pd.read_csv("data/processed/new-hpi.csv", index_col=False)
df_cpi = pd.read_csv("data/processed/cpi.csv", index_col=False)

df_vacancy_metro["date"] = pd.to_datetime(df_vacancy_metro["date"], format="%Y-%m-%d")
df_bank_rate["date"] = pd.to_datetime(df_bank_rate["date"], format="%Y-%m-%d")
df_hpi["date"] = pd.to_datetime(df_hpi["date"], format="%Y-%m-%d")
df_new_hpi["date"] = pd.to_datetime(df_new_hpi["date"], format="%Y-%m-%d")
df_cpi["date"] = pd.to_datetime(df_cpi["date"], format="%Y-%m-%d")

df_cpi_shelter = df_cpi[df_cpi["groups"] == "Shelter"][["date", "value"]].reset_index(
    drop=True
)

base_date = "2005-01-01"
base_df_hpi = df_hpi.loc[df_hpi["date"] == base_date, "value"].values[0]
base_df_new_hpi = df_new_hpi.loc[df_new_hpi["date"] == base_date, "value"].values[0]
base_df_cpi_shelter = df_cpi_shelter.loc[
    df_cpi_shelter["date"] == base_date, "value"
].values[0]

# df_vacancy_metro["pct_change"] = df_vacancy_metro["value"].pct_change() * 100
# df_bank_rate["pct_change"] = df_bank_rate["value"].pct_change() * 100
df_hpi["pct_change"] = df_hpi["value"].pct_change() * 100
df_new_hpi["pct_change"] = df_new_hpi["value"].pct_change() * 100
df_cpi_shelter["pct_change"] = df_cpi_shelter["value"].pct_change() * 100

## Part 2: Regression Analysis
# Rename the 'value' columns in df_bank_rate and df_vacancy_metro before merging
df_bank_rate.rename(columns={'value': 'bank_rate'}, inplace=True)
df_vacancy_metro.rename(columns={'value': 'vacancy_rate'}, inplace=True)

## Part 1b: Resampling
df_vacancy_metro.set_index('date', inplace=True)
df_vacancy_metro_monthly = df_vacancy_metro.resample('M').first()
df_vacancy_metro_monthly = df_vacancy_metro_monthly.interpolate(method='linear')
df_vacancy_metro_monthly.reset_index(inplace=True)
df_vacancy_metro.reset_index(inplace=True)


df_hpi = df_hpi.sort_values(by='date')
df_hpi.rename(columns={"value": "hpi"}, inplace=True)
df_bank_rate = df_bank_rate.sort_values(by='date')
df_vacancy_metro_monthly = df_vacancy_metro_monthly.sort_values(by='date')

# Merge the dataframes on the 'date' column
df = pd.merge_asof(df_hpi.drop(columns="pct_change"), df_bank_rate, on='date', direction='nearest')
df = pd.merge_asof(df, df_vacancy_metro_monthly, on='date', direction='nearest', suffixes=('_bank_rate', '_vacancy'))

# Rename the columns for the merged dataframe
df.rename(columns={'value_bank_rate': 'bank_rate', 'value': 'vacancy_rate'}, inplace=True)

# Check for any missing values
print(df.isnull().sum())

## Part 3: Run Models
models = []
for shift in range(0, 20):
    df['hpi_lagged'] = df['hpi'].shift(-shift)
    df.dropna(inplace=True)
    X = df[['bank_rate', 'vacancy_rate']]
    Y = df['hpi_lagged']
    X = sm.add_constant(X)
    model = sm.OLS(Y, X).fit()
    models.append(model)

with open("txt/models.txt", "a") as f:
    for shift, model in enumerate(models):
        print("--------------------", file=f)
        print(f"Shift = {shift}", file=f)
        print("--------------------", file=f)
        print(model.summary(), file=f)
        print("\n\n\n", file=f)

print(df[['bank_rate', 'vacancy_rate']].corr())

# Variance Inflation Factor
vif = pd.DataFrame()
vif['Features'] = X.columns
vif['VIF Factor'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print(vif)

grangercausalitytests(df[['bank_rate', 'vacancy_rate']], maxlag=2)
grangercausalitytests(df[['vacancy_rate', 'bank_rate']], maxlag=2)
