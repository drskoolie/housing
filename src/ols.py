## Part 0: Initialization
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tsa.stattools import grangercausalitytests
import statsmodels.api as sm

pd.options.mode.chained_assignment = None  # default='warn'
sns.set_style("whitegrid")

# Part 1: Data Importing
df_cpi = pd.read_pickle("data/processed/df_cpi.pkl")
df_crea = pd.read_pickle("data/processed/df_crea.pkl")
df_bank_rate = pd.read_pickle("data/processed/df_bank_rate.pkl")
df_nhpi = pd.read_pickle("data/processed/df_nhpi.pkl")
df_vacancy_metro = pd.read_pickle("data/processed/df_vacancy_metro.pkl")

## Part 2: Regression Analysis
# --> Part 2a: Resampling
df_vacancy_metro_monthly = df_vacancy_metro.resample('M').first()
df_vacancy_metro_monthly = df_vacancy_metro_monthly.interpolate(method='linear')
df_vacancy_metro_monthly

df = pd.merge_asof(df_crea, df_bank_rate, on='date', direction='nearest')
df = pd.merge_asof(df, df_vacancy_metro_monthly, on='date', direction='nearest', suffixes=('_bank_rate', '_vacancy'))

# Rename the columns for the merged dataframe
df.rename(columns={'value_bank_rate': 'bank_rate', 'value': 'vacancy_rate'}, inplace=True)
# Check for any missing values
print(df.isnull().sum())

## Part 3: Run Models
shift = 6
df['hpi_lagged'] = df['hpi'].shift(-shift)
df.dropna(inplace=True)
X = df[['bank_rate', 'vacancy_rate']]
Y = df['hpi_lagged']
X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()
print(model.summary())

print(df[['bank_rate', 'vacancy_rate']].corr())

# Variance Inflation Factor
vif = pd.DataFrame()
vif['Features'] = X.columns
vif['VIF Factor'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print(vif)
grangercausalitytests(df[['bank_rate', 'vacancy_rate']], maxlag=2)
grangercausalitytests(df[['vacancy_rate', 'bank_rate']], maxlag=2)
