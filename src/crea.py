## Part 0: Intialization
import pandas as pd

"""
    index_col=0,
    parse_dates=True,
    date_format="%b %Y",
"""

df_crea = pd.read_excel(
    "../research/data/crea/crea-all-time.xlsx",
)

## Part 1: Setting up Columns
measures = df_crea.iloc[0,:][df_crea.iloc[0, :].notna()].to_list()[1:]
regions = df_crea.iloc[1,:][df_crea.iloc[1, :].notna()].to_list()[1:]
seasonal_adjustments = df_crea.iloc[3,:][df_crea.iloc[3, :].notna()].to_list()[1:]

