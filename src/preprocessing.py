## Part 0: Initialization
import pandas as pd

## Part 1: Loading Data
df_crea = pd.read_excel("data/raw/mls-pi/Not Seasonally Adjusted.xlsx")
df_interest = pd.read_csv("data/raw/interest-rate/interest-rate.csv")
df_nhpi = pd.read_csv("data/raw/new-housing-price-index/18100205.csv")
df_residential_mortgage_credit = pd.read_csv(
    "data/raw/residential-mortgage-credit//10100129.csv"
)
df_vacancy = pd.read_csv("data/raw/vacancy-rates/34100127.csv")

df_cpi_1 = pd.read_csv("data/raw/cpi/cpi1.csv")
df_cpi_2 = pd.read_csv("data/raw/cpi/cpi2.csv")
df_cpi = pd.concat([df_cpi_1, df_cpi_2], ignore_index=True)
del df_cpi_1, df_cpi_2


## Part 2: Data Preprocessing
# --> Part 2a: Stats Canada
def preprocess_stat_canada(df, col_name, coordinate, date_format):
    df.columns = df.columns.str.lower()
    df_coor = df[df["coordinate"] == coordinate]
    df_coor = df_coor[["ref_date", "value"]]
    df_coor = df_coor.dropna(subset=["value"])
    df_coor["date"] = pd.to_datetime(df_coor["ref_date"], format=date_format)
    df_coor.drop(["ref_date"], axis=1, inplace=True)
    df_coor = df_coor[["date", "value"]]
    df_coor.rename(columns={"value": col_name}, inplace=True)
    df_coor.reset_index(drop=True, inplace=True)
    df_coor.set_index("date", inplace=True)
    return df_coor


df_bank_rate = preprocess_stat_canada(df_interest, "bank_rate", 1.38, "%Y-%m-%d")
df_nhpi = preprocess_stat_canada(df_nhpi, "nhpi", 1.1, "%Y-%m")
df_residential_mortgage_credit = preprocess_stat_canada(
    df_residential_mortgage_credit, "residential_mortgage_credit", "1.1.1.1", "%Y-%m",
)
df_vacancy_metro = preprocess_stat_canada(df_vacancy, "vacancy_rate", 1, "%Y")

## Part 2b: MLS
df_crea.columns = df_crea.columns.str.lower()
df_crea = df_crea[["date", "composite_hpi"]]
df_crea.reset_index(drop=True, inplace=True)
df_crea.set_index("date", inplace=True)

## Part 2c: CPI
df_cpi.columns = df_cpi.columns.str.lower()
df_cpi = df_cpi[df_cpi["geo"] == "Canada"]
df_cpi.rename(columns={"products and product groups": "groups"}, inplace=True)
df_cpi["date"] = pd.to_datetime(df_cpi["ref_date"], format="%Y-%m")
df_cpi = df_cpi[["date", "groups", "coordinate", "value", "uom", "uom_id"]]
df_cpi.reset_index(drop=True, inplace=True)
df_cpi.set_index("date", inplace=True)

## Part 3: Data Exporting
df_bank_rate.to_pickle("data/processed/df_bank_rate.pkl")
df_cpi.to_pickle("data/processed/df_cpi.pkl")
df_crea.to_pickle("data/processed/df_crea.pkl")
df_nhpi.to_pickle("data/processed/df_nhpi.pkl")
df_residential_mortgage_credit.to_pickle("data/processed/df_residential_mortgage_credit.pkl")
df_vacancy_metro.to_pickle("data/processed/df_vacancy_metro.pkl")
