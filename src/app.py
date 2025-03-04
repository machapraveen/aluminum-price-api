from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import io
from data_loader import load_arima_model, load_historical_data
from forecast_utils import generate_forecast

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Adjust origins for production

# Load model and data at startup
model = load_arima_model()
historical_data = load_historical_data()
last_historical_price = historical_data['Price'].iloc[-1] if historical_data is not None else 0

@app.route('/')
def home():
    return jsonify({"status": "Aluminum Price API is running", "message": "Use /predict to get forecasts"}), 200

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded.'}), 500
    if historical_data is None:
        return jsonify({'error': 'Historical data not loaded.'}), 500

    try:
        if request.method == 'POST':
            data = request.get_json()
            days = int(data.get('days', 30)) if data else 30
        else:
            days = int(request.args.get('days', 30))

        if days <= 0 or days > 365:
            return jsonify({'error': 'Days must be between 1 and 365.'}), 400

        # Format historical data (last 30 days)
        historical_subset = historical_data.tail(30).to_dict('records')
        historical_data_formatted = [
            {'date': row['Date'].strftime('%Y-%m-%d'), 'price': float(row['Price'])}
            for row in historical_subset
        ]

        # Generate forecast
        forecast_data, trend = generate_forecast(model, days, last_historical_price)

        response = {
            'historical_data': historical_data_formatted,
            'forecast_data': forecast_data,
            'trend': trend
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export_forecast', methods=['POST'])
def export_forecast():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON data.'}), 400

        forecast = data.get('forecast', {})
        if not forecast:
            return jsonify({'error': 'No forecast data provided.'}), 400

        df = pd.DataFrame(list(forecast.items()), columns=['Date', 'Price'])
        df['Price'] = df['Price'].round(2)
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='aluminum_price_forecast.csv'
        )
    except Exception as e:
        return jsonify({'error': f'Export error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)