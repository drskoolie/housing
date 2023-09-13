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
# --> Part 2a: Bank-Rate and Vacancy-Rate
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


plt.figure(figsize=(12, 6))
sns.lineplot(
    data=df_bank_rate,
    x="date",
    y="value",
    label="bank rate",
    linewidth=2.5,
    color="crimson",
)
sns.lineplot(
    data=df_vacancy_metro,
    x="date",
    y="value",
    label="vacancy rate",
    linewidth=2.5,
    color="blue",
)

plt.title("Bank Rate vs Vacancy Rate", fontsize=16, fontweight="bold", loc="left")
plt.xlabel("Date", fontsize=14, labelpad=15)
plt.ylabel("Rate (%)", fontsize=14, labelpad=15)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig("plots/bank_vacancy_rates.png")
plt.show()
