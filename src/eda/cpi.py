## Part 0: Intialization
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pd.options.mode.chained_assignment = None  # default='warn'
sns.set_style()

df_bank_rate = pd.read_pickle("data/processed/df_bank_rate.pkl")
df_cpi = pd.read_pickle("data/processed/df_cpi.pkl")
df_crea = pd.read_pickle("data/processed/df_crea.pkl")
df_residential_mortgage_credit = pd.read_pickle(
    "data/processed/df_residential_mortgage_credit.pkl"
)

## Part 1: Finding Groups
unique_coordinates = df_cpi["coordinate"].unique()
coordinate_to_group = {
    coord: df_cpi.loc[df_cpi["coordinate"] == coord, "groups"].iloc[0]
    for coord in unique_coordinates
}

## Part 2: Select Groups
"""
2.8: 'Rented accommodation',
2.81: 'Rent',
2.82: "Tenants' insurance premiums",
2.84: 'Owned accommodation',
2.85: 'Mortgage interest cost',
2.86: "Homeowners' replacement cost",
2.87: 'Property taxes and other special charges',
2.88: "Homeowners' home and mortgage insurance",
2.89: "Homeowners' maintenance and repairs",
"""


def plot_cpi(df_cpi, coordinate):
    fig, ax = plt.subplots(1, 2, figsize=(18,9))
    df_cpi_coor = df_cpi[df_cpi["coordinate"] == coordinate]
    sns.lineplot(
        ax=ax[0],
        data=df_cpi_coor,
        x=df_cpi_coor.index,
        y="value",
        color="blue",
    )
    ax[0].set_title(df_cpi_coor["groups"].iloc[0])
    ax[0].fill_between(
        df_cpi_coor.index,
        df_cpi_coor["value"],
        alpha=0.1,
        color="blue",
    )
    df_cpi_coor["pct_change"] = df_cpi_coor["value"].pct_change(periods=12) * 100

    sns.lineplot(
        ax=ax[1],
        data=df_cpi_coor,
        x=df_cpi_coor.index,
        y="pct_change",
        color="blue",
    )
    ax[1].set_title(df_cpi_coor["groups"].iloc[0])

for coor in [2.81, 2.82, 2.84, 2.85, 2.86, 2.87, 2.88, 2.89]:
    plot_cpi(df_cpi, coor)
    plt.savefig(
        f"plots/cpi/{df_cpi['groups'][df_cpi['coordinate'] == coor].iloc[0]}.png"
    )
    plt.close()

