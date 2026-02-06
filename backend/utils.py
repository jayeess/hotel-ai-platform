import pandas as pd
import numpy as np
import joblib
import os
from tensorflow.keras.models import load_model

class HotelModelWrapper:
    def __init__(self, assets_path="assets"):
        self.assets_path = assets_path
        self.model = None
        self.scaler = None
        self.encoders = None
        self.feature_columns = None
        self.load_assets()

    def load_assets(self):
        model_path = os.path.join(self.assets_path, "fds_model_1.keras")
        if not os.path.exists(model_path):
            model_path = os.path.join(self.assets_path, "fds_hotel_model.h5")
        
        self.model = load_model(model_path)
        self.scaler = joblib.load(os.path.join(self.assets_path, "scaler.joblib"))
        self.encoders = joblib.load(os.path.join(self.assets_path, "encoders.joblib"))
        self.feature_columns = joblib.load(os.path.join(self.assets_path, "feature_columns.joblib"))

    def preprocess(self, input_data: dict):
        df = pd.DataFrame([input_data])
        
        # Ensure all required columns are present (fill with defaults if missing)
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Reorder columns
        df = df[self.feature_columns]
        
        # Encode categorical
        for col, le in self.encoders.items():
            # Handle unknown labels by defaulting to the first class
            df[col] = df[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
            df[col] = le.transform(df[col])
            
        # Scale
        X_scaled = self.scaler.transform(df)
        return X_scaled

    def predict(self, input_data: dict):
        X = self.preprocess(input_data)
        prob = self.model.predict(X, verbose=0)[0][0]
        return float(prob)
