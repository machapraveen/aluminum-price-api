# Aluminum Price API

A Flask API for forecasting aluminum prices using an ARIMA model.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run locally: `python src/app.py`
3. Deploy to Render: Push to Git repository and configure as Web Service.

## Endpoints
- GET/POST `/predict?days=<int>`: Returns historical and forecast data.
- POST `/export_forecast`: Exports forecast as CSV.