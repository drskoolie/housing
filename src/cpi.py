## Part 0: Intialization
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pd.options.mode.chained_assignment = None  # default='warn'
sns.set_style()

df_bank_rate = pd.read_pickle("data/processed/df_bank_rate.pkl")
df_cpi = pd.read_pickle("data/processed/df_cpi.pkl")
df_crea = pd.read_pickle("data/processed/df_crea.pkl")

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
    df_cpi_coordinate = df_cpi[df_cpi["coordinate"] == coordinate]
    sns.lineplot(data=df_cpi_coordinate, x=df_cpi_coordinate.index, y="value", label="insurance")
    plt.title(df_cpi_coordinate["groups"].iloc[0])


plot_cpi(df_cpi, 2.88)
sns.lineplot(data=df_crea, x=df_crea.index, y="composite_hpi", label="composite_hpi")
sns.lineplot(data=df_bank_rate, x=df_bank_rate.index, y="bank_rate", label="bank_rate")
plt.show()

df_cpi_insurance = df_cpi[df_cpi["coordinate"] == 2.88]
df_cpi_insurance.rename(columns={"value": "insurance"}, inplace=True)
df_cpi_insurance = df_cpi_insurance[["insurance"]]

## Part 3: CREA generation
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Step 1 & 2: Split the data into training and test sets and train the model
df_merged = pd.merge(df_crea, df_cpi_insurance, how='inner', left_index=True, right_index=True)
X = df_merged["insurance"].values.reshape(-1, 1)
y = df_merged["composite_hpi"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

# Step 3: Test the model
y_pred = model.predict(X_test)

# Step 4: Calculate error metrics
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"Mean Absolute Error: {mae}")
print(f"R-squared: {r2}")
