import pickle
import pandas as pd

# Load your saved model (adjust filename if different)
with open('trained_model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict(features_df):
    # features_df must match training columns: ['mean_ndvi', 'cum_rain_30d', 'temp_anomaly', 'mean_temp_c']
    prediction = model.predict(features_df)
    return prediction[0]  # Return single value (e.g., 'healthy', 'moderate', 'high')