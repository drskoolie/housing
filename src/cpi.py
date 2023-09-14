## Part 0: Intialization
import pandas as pd

df_cpi = pd.read_pickle("data/processed/df_cpi.pkl")

## Part 1: Finding Groups
unique_coordinates = df_cpi["coordinate"].unique()
coordinate_to_group = {
    coord: df_cpi.loc[df_cpi["coordinate"] == coord, "groups"].iloc[0]
    for coord in unique_coordinates
}
