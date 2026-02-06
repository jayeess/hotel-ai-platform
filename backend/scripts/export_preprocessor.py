import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

# Load the data
data = pd.read_csv("Hotel_reservations_cleaned.csv")

# Same processing as the notebook
X = data.drop(columns=['Booking_ID', 'booking_status', 'arrival_datetime', 'booking_status_numeric'], errors='ignore')

# Identify categorical columns
categorical_cols = X.select_dtypes(include=['object']).columns
print(f"Categorical columns: {list(categorical_cols)}")

encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    encoders[col] = le

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Create assets directory if not exists
os.makedirs("backend/assets", exist_ok=True)

# Save preprocessors
joblib.dump(scaler, "backend/assets/scaler.joblib")
joblib.dump(encoders, "backend/assets/encoders.joblib")

# Save column names to ensure order
joblib.dump(list(X.columns), "backend/assets/feature_columns.joblib")

print("Preprocessors saved to backend/assets/")
