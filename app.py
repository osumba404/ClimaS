from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px
import plotly.io as pio
import json

app = Flask(__name__)

# Sample historical climate data (simulating WorldClim/NASA POWER)
# In production, replace with API calls or pre-downloaded datasets
def load_sample_data():
    data = {
        'Year': range(2000, 2025),
        'Temperature': [25.0 + i * 0.1 + np.random.normal(0, 0.5) for i in range(25)],
        'Rainfall': [800 + i * 2 + np.random.normal(0, 50) for i in range(25)],
        'Humidity': [60 + i * 0.5 + np.random.normal(0, 5) for i in range(25)]
    }
    return pd.DataFrame(data)

# Crop recommendation lookup table
crop_recommendations = {
    'Maize': {'temp_min': 20, 'temp_max': 30, 'rainfall_min': 600, 'rainfall_max': 1200},
    'Sorghum': {'temp_min': 25, 'temp_max': 35, 'rainfall_min': 400, 'rainfall_max': 800},
    'Cassava': {'temp_min': 22, 'temp_max': 32, 'rainfall_min': 500, 'rainfall_max': 1500}
}

# Train Random Forest model
def train_model(df):
    X = df[['Year']]
    models = {}
    for target in ['Temperature', 'Rainfall', 'Humidity']:
        y = df[target]
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        models[target] = model
    return models

# Predict future climate
def predict_climate(models, years_ahead):
    future_years = np.array(range(2025, 2025 + years_ahead)).reshape(-1, 1)
    predictions = {}
    for target, model in models.items():
        predictions[target] = model.predict(future_years)
    return pd.DataFrame({
        'Year': range(2025, 2025 + years_ahead),
        'Temperature': predictions['Temperature'],
        'Rainfall': predictions['Rainfall'],
        'Humidity': predictions['Humidity']
    })

# Simulate scenario (e.g., deforestation increases temperature, reduces rainfall)
def simulate_scenario(df, deforestation_factor):
    df_simulated = df.copy()
    df_simulated['Temperature'] += deforestation_factor * 0.5  # +0.5°C per 10% deforestation
    df_simulated['Rainfall'] *= (1 - deforestation_factor * 0.2)  # -20% rainfall per 10% deforestation
    return df_simulated

# Recommend crops based on predicted climate
def recommend_crops(predicted_climate):
    recommendations = []
    for crop, criteria in crop_recommendations.items():
        temp_ok = criteria['temp_min'] <= predicted_climate['Temperature'].mean() <= criteria['temp_max']
        rain_ok = criteria['rainfall_min'] <= predicted_climate['Rainfall'].mean() <= criteria['rainfall_max']
        if temp_ok and rain_ok:
            recommendations.append(crop)
    return recommendations if recommendations else ["No suitable crops found"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    years_ahead = 10
    if request.method == 'POST':
        years_ahead = int(request.form.get('years_ahead', 10))
    
    # Load and process data
    df = load_sample_data()
    models = train_model(df)
    predicted_df = predict_climate(models, years_ahead)
    
    # Generate Plotly graphs
    fig_temp = px.line(predicted_df, x='Year', y='Temperature', title='Predicted Temperature')
    fig_rain = px.line(predicted_df, x='Year', y='Rainfall', title='Predicted Rainfall')
    fig_hum = px.line(predicted_df, x='Year', y='Humidity', title='Predicted Humidity')
    
    graphs = {
        'temp_graph': pio.to_html(fig_temp, full_html=False),
        'rain_graph': pio.to_html(fig_rain, full_html=False),
        'hum_graph': pio.to_html(fig_hum, full_html=False)
    }
    
    # Crop recommendations
    crops = recommend_crops(predicted_df)
    
    return render_template('predict.html', graphs=graphs, crops=crops, years_ahead=years_ahead)

@app.route('/simulate', methods=['GET', 'POST'])
def simulate():
    years_ahead = 10
    deforestation_factor = 0.0
    if request.method == 'POST':
        years_ahead = int(request.form.get('years_ahead', 10))
        deforestation_factor = float(request.form.get('deforestation_factor', 0.0))
    
    # Load and process data
    df = load_sample_data()
    models = train_model(df)
    baseline_df = predict_climate(models, years_ahead)
    simulated_df = simulate_scenario(baseline_df, deforestation_factor)
    
    # Generate comparative Plotly graphs
    fig_temp = px.line(title='Temperature (Baseline vs Simulated)')
    fig_temp.add_scatter(x=baseline_df['Year'], y=baseline_df['Temperature'], name='Baseline')
    fig_temp.add_scatter(x=simulated_df['Year'], y=simulated_df['Temperature'], name='Simulated')
    
    fig_rain = px.line(title='Rainfall (Baseline vs Simulated)')
    fig_rain.add_scatter(x=baseline_df['Year'], y=baseline_df['Rainfall'], name='Baseline')
    fig_rain.add_scatter(x=simulated_df['Year'], y=simulated_df['Rainfall'], name='Simulated')
    
    graphs = {
        'temp_graph': pio.to_html(fig_temp, full_html=False),
        'rain_graph': pio.to_html(fig_rain, full_html=False)
    }
    
    return render_template('simulate.html', graphs=graphs, years_ahead=years_ahead, deforestation_factor=deforestation_factor)

if __name__ == '__main__':
    app.run(debug=True)