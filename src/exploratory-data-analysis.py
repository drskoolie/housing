## Part 0: Initialization
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None  # default='warn'
sns.set_style("whitegrid")

## Part 1: Data Loading
df_cpi = pd.read_pickle("data/processed/df_cpi.pkl")
df_crea = pd.read_pickle("data/processed/df_crea.pkl")
df_bank_rate = pd.read_pickle("data/processed/df_bank_rate.pkl")
df_nhpi = pd.read_pickle("data/processed/df_nhpi.pkl")
df_vacancy_metro = pd.read_pickle("data/processed/df_vacancy_metro.pkl")

## Part 2: Exploratory Data Analysis

# --> Part 2a: Plot Simple
def time_plot(df, title, ylabel, location):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="date", y="value", linewidth=2.5, color="crimson")
    plt.title(title, fontsize=16, fontweight="bold", loc="left")
    plt.xlabel("Date", fontsize=14, labelpad=15)
    plt.ylabel(ylabel, fontsize=14, labelpad=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    sns.despine(left=True, bottom=True)

    # Display the plot
    plt.tight_layout()
    plt.savefig(location)
    plt.show()


time_plot(
    df_vacancy_metro,
    "Vacancy Rate Over Time in Metro Areas",
    "Vacancy Rate (%)",
    "plots/vacancy-rates.png",
)

time_plot(
    df_bank_rate,
    "Bank Rate Over Time",
    "Bank Rate (%)",
    "plots/bank-rates.png",
)

## Part 3b: Plot Multiple
df_cpi_shelter = df_cpi[df_cpi["groups"] == "Shelter"][["date", "value"]].reset_index(
    drop=True
)

base_date = "2005-01-01"
base_df_hpi = df_hpi.loc[df_hpi["date"] == base_date, "value"].values[0]
base_df_new_hpi = df_new_hpi.loc[df_new_hpi["date"] == base_date, "value"].values[0]
base_df_cpi_shelter = df_cpi_shelter.loc[
    df_cpi_shelter["date"] == base_date, "value"
].values[0]

df_hpi["value"] = df_hpi["value"] / base_df_hpi * 100
df_new_hpi["value"] = df_new_hpi["value"] / base_df_new_hpi * 100
df_cpi_shelter["value"] = df_cpi_shelter["value"] / base_df_hpi * 100

df_hpi["pct_change"] = df_hpi["value"].pct_change() * 100
df_new_hpi["pct_change"] = df_new_hpi["value"].pct_change() * 100
df_cpi_shelter["pct_change"] = df_cpi_shelter["value"].pct_change() * 100

plt.figure(figsize=(12, 6))
sns.lineplot(
    data=df_new_hpi,
    x="date",
    y="value",
    label="HPI-New (from StatCanada)",
    linewidth=2.5,
)
sns.lineplot(
    data=df_cpi_shelter, x="date", y="value", label="Shelter (from CPI)", linewidth=2.5
)
sns.lineplot(
    data=df_hpi, x="date", y="value", label="HPI (from real-estate)", linewidth=2.5
)

plt.title(
    "Comparing between different housing indices",
    fontsize=16,
    fontweight="bold",
    loc="left",
)
plt.xlabel("Date", fontsize=14, labelpad=15)
plt.ylabel("Value", fontsize=14, labelpad=15)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
sns.despine(left=True, bottom=True)

plt.legend(title="Data Source", title_fontsize="13", loc="upper left", fontsize="11")
plt.savefig("plots/different-hpi.png")
plt.show()

## Part 3c: Percentage Change
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=df_new_hpi,
    x="date",
    y="pct_change",
    label="HPI-New (from StatCanada)",
    linewidth=2,
    alpha=0.7,
)
sns.lineplot(
    data=df_cpi_shelter,
    x="date",
    y="pct_change",
    label="Shelter (from CPI)",
    linewidth=2,
    alpha=0.7,
)
sns.lineplot(
    data=df_hpi,
    x="date",
    y="pct_change",
    label="HPI (from real-estate)",
    linewidth=2,
    alpha=0.7,
)

plt.title(
    "Comparing between different housing indices (percentage change)",
    fontsize=16,
    fontweight="bold",
    loc="left",
)
plt.xlabel("Date", fontsize=14, labelpad=15)
plt.ylabel("Percentage Change", fontsize=14, labelpad=15)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
sns.despine(left=True, bottom=True)

plt.legend(title="Data Source", title_fontsize="13", loc="upper left", fontsize="11")
plt.savefig("plots/different-hpi-pct-change.png")
plt.show()

## Part 3d: Variables
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=df_hpi,
    x="date",
    y="pct_change",
    label="HPI",
    linewidth=2,
    alpha=0.7,
)
sns.lineplot(
    data=df_bank_rate,
    x="date",
    y="value",
    label="Bank Rate",
    linewidth=2,
    alpha=0.7,
)
sns.lineplot(
    data=df_vacancy_metro,
    x="date",
    y="value",
    label="Vacancy Rate",
    linewidth=2,
    alpha=0.7,
)

plt.title(
    "Housing Price Index and Others",
    fontsize=16,
    fontweight="bold",
    loc="left",
)
plt.xlabel("Date", fontsize=14, labelpad=15)
plt.ylabel("Rate/Index", fontsize=14, labelpad=15)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
sns.despine(left=True, bottom=True)

plt.legend(title="Data Source", title_fontsize="13", loc="upper left", fontsize="11")
plt.savefig("plots/different-hpi-pct-change.png")
plt.show()
