import pickle
import pandas as pd
import os

def load_arima_model(model_path='aluminum_price_arima_model.pkl'):
    try:
        if not os.path.exists(model_path):
            raise FileNotFoundError("ARIMA model file not found")
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        print("Loaded ARIMA model successfully")
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None

def load_historical_data(data_path='Aluminium_Data.csv'):
    try:
        data = pd.read_csv(data_path, parse_dates=['Date'])
        data['Price'] = data['Price'].apply(
            lambda x: float(x.replace(',', '')) if isinstance(x, str) else x
        )
        data = data.sort_values('Date')
        return data
    except Exception as e:
        print(f"Error loading historical data: {str(e)}")
        return None