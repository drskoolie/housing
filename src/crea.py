## Part 0: Intialization
import numpy as np
import pandas as pd

"""
    index_col=0,
    parse_dates=True,
    date_format="%b %Y",
"""

df_crea = pd.read_excel(
    "../research/data/crea/crea-all-time.xlsx",
)

## Part 1: Pulling Information about Columns
measures = df_crea.iloc[0,:][df_crea.iloc[0, :].notna()].to_list()[1:]
measures_idx = np.where(df_crea.iloc[0, :].notna())[0][1:] - 1
regions = df_crea.iloc[1,:][df_crea.iloc[1, :].notna()].to_list()[1:]
regions_idx = np.where(df_crea.iloc[1, :].notna())[0][1:] - 1
adjustments = df_crea.iloc[3,:][df_crea.iloc[3, :].notna()].to_list()[1:]
adjustments_idx = np.where(df_crea.iloc[3, :].notna())[0][1:] - 1

## Part 2: Setting up Columns
cols = [""] * df_crea.shape[1]

for idx in range(df_crea.shape[1]):
    pass

for i, measure in enumerate(measures):
    start_idx = measures_idx[i]
    end_idx = measures_idx[i+1] if i+1 < len(measures_idx) else len(cols)
    for j in range(start_idx, end_idx):
        cols[j] += measure

for i, region in enumerate(regions):
    start_idx = regions_idx[i]
    end_idx = regions_idx[i+1] if i+1 < len(regions_idx) else len(cols)
    for j in range(start_idx, end_idx):
        cols[j] += "_" + region

for i, adjustment in enumerate(adjustments):
    start_idx = adjustments_idx[i]
    end_idx = adjustments_idx[i+1] if i+1 < len(adjustments_idx) else len(cols)
    for j in range(start_idx, end_idx):
        cols[j] += "_" + adjustment
