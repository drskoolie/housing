## Part 0: Initialization
import pandas as pd

## Part 1: Loading Data
df_hpi = pd.read_excel("data/mls-pi/Not Seasonally Adjusted.xlsx")
df_vacancy = pd.read_csv("data/vacancy-rates/34100127.csv")
df_interest = pd.read_csv("data/interest-rate/interest-rate.csv")
df_new_hpi = pd.read_csv("data/new-housing-price-index/18100205.csv")

df_cpi_1 = pd.read_csv("data/cpi/cpi1.csv")
df_cpi_2 = pd.read_csv("data/cpi/cpi2.csv")
df_cpi = pd.concat([df_cpi_1, df_cpi_2], ignore_index=True)
del df_cpi_1, df_cpi_2


## Part 2: Data Cleaning
## Part 2a: Stats Canada
def clean_stat_canada(df, coordinate, date_format):
    df.columns = df.columns.str.lower()
    df_coor = df[df["coordinate"] == coordinate]
    df_coor = df_coor[["ref_date", "value"]]
    df_coor = df_coor.dropna(subset=["value"])
    df_coor["date"] = pd.to_datetime(df_coor["ref_date"], format=date_format)
    df_coor.drop(["ref_date"], axis=1, inplace=True)
    df_coor = df_coor[["date", "value"]]
    df_coor.reset_index(drop=True, inplace=True)
    return df_coor


df_vacancy_metro = clean_stat_canada(df_vacancy, 1, "%Y")
df_bank_rate = clean_stat_canada(df_interest, 1.38, "%Y-%m-%d")
df_new_hpi = clean_stat_canada(df_new_hpi, 1.1, "%Y-%m")


## Part 2b: MLS
df_hpi.columns = df_hpi.columns.str.lower()
df_hpi = df_hpi[["date", "composite_hpi"]]
df_hpi.rename(columns={"composite_hpi": "value"}, inplace=True)

## Part 2c: CPI
df_cpi.columns = df_cpi.columns.str.lower()
df_cpi = df_cpi[df_cpi["geo"] == "Canada"]
df_cpi.rename(columns={"products and product groups": "groups"}, inplace=True)
df_cpi["date"] = pd.to_datetime(df_cpi["ref_date"], format = "%Y-%m")
df_cpi = df_cpi[["date", "groups", "coordinate", "value", "uom", "uom_id"]]
df_cpi.reset_index(drop=True, inplace=True)


## Part 3: Data Exporting
df_hpi.to_csv("data/processed/hpi.csv", encoding="utf-8", index=False)
df_vacancy_metro.to_csv(
    "data/processed/vacancy-metro.csv", encoding="utf-8", index=False
)
df_bank_rate.to_csv("data/processed/bank-rate.csv", encoding="utf-8", index=False)
df_new_hpi.to_csv("data/processed/new-hpi.csv", encoding="utf-8", index=False)
df_cpi.to_csv("data/processed/cpi.csv", encoding="utf-8", index=False)
