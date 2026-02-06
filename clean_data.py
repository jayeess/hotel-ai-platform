import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv("Hotel_reservations.csv")

# Create arrival_datetime
df['arrival_datetime'] = pd.to_datetime(
    df['arrival_year'].astype(str) + '-' + df['arrival_month'].astype(str) + '-' + df['arrival_date'].astype(str),
    errors='coerce'
)

# Identify rows that failed conversion
failed_rows = df[df['arrival_datetime'].isna()]
print(f"Number of rows that failed date conversion: {len(failed_rows)}")

# Drop rows with null datetime (as planned in the notebook)
df_cleaned = df.dropna(subset=['arrival_datetime']).copy()

# Fix bookingstatus to numeric if it's for ANN
# 'Not_Canceled' -> 0, 'Canceled' -> 1
df_cleaned['booking_status_numeric'] = df_cleaned['booking_status'].apply(lambda x: 1 if x == 'Canceled' else 0)

# Save cleaned data
df_cleaned.to_csv("Hotel_reservations_cleaned.csv", index=False)
print("Cleaned data saved to Hotel_reservations_cleaned.csv")
