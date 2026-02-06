import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

print("--- Hotel Reservation AI Tester ---")

# 1. Load the cleaned data
try:
    data = pd.read_csv("Hotel_reservations_cleaned.csv")
except:
    print("Error: Please run clean_data.py first!")
    exit()

# 2. Load the trained model
try:
    model = load_model('fds_hotel_model.h5')
except:
    print("Error: fds_hotel_model.h5 not found. Please run the notebook first!")
    exit()

# 3. Preparation (The model needs the data in a specific format)
# We recreate the same processing as the notebook
X = data.drop(columns=['Booking_ID', 'booking_status', 'arrival_datetime', 'booking_status_numeric'], errors='ignore')
categorical_cols = X.select_dtypes(include=['object']).columns
le = LabelEncoder()
for col in categorical_cols:
    X[col] = le.fit_transform(X[col])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Pick 5 random samples to test
indices = np.random.choice(len(data), 5, replace=False)

print(f"\nTesting {len(indices)} random reservations...")
print("-" * 50)

for idx in indices:
    # Get features for this sample
    sample_features = X_scaled[idx].reshape(1, -1)
    
    # Get actual status
    actual = data.iloc[idx]['booking_status']
    
    # Make prediction
    prediction_prob = model.predict(sample_features, verbose=0)[0][0]
    prediction = "Canceled" if prediction_prob > 0.5 else "Not_Canceled"
    
    # Output results
    match = "✅ CORRECT" if prediction == actual else "❌ WRONG"
    print(f"Reservation ID: {data.iloc[idx]['Booking_ID']}")
    print(f"AI Prediction: {prediction} ({prediction_prob*100:.1f}% confidence)")
    print(f"Actual Status: {actual}")
    print(f"Result: {match}")
    print("-" * 50)
