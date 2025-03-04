from datetime import datetime, timedelta
import numpy as np

def generate_forecast(model, days, last_price):
    try:
        forecast = model.forecast(steps=days)
        forecast_values = forecast.tolist()
        start_date = datetime.now()
        forecast_dates = [start_date + timedelta(days=i) for i in range(days)]
        forecast_date_strings = [d.strftime('%Y-%m-%d') for d in forecast_dates]

        forecast_data = [
            {'date': date, 'price': price, 'forecast': True}
            for date, price in zip(forecast_date_strings, forecast_values)
        ]

        slope, _ = np.polyfit(np.arange(len(forecast_values)), forecast_values, 1)
        trend_type = 'up' if slope > 0 else 'down' if slope < 0 else 'stable'
        percentage_change = ((forecast_values[-1] - last_price) / last_price) * 100

        return forecast_data, {'type': trend_type, 'percentage': float(percentage_change)}
    except Exception as e:
        raise Exception(f"Forecast generation error: {str(e)}")