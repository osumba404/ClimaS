# app.py

from flask import Flask, render_template, request
import plotly.io as pio
import plotly.graph_objects as go

# Import modularized functions
from app.ml_model import train_model, predict_climate, simulate_scenario
from app.data_utils import load_sample_data
from app.recommend import recommend_crops

# Initialize Flask app
app = Flask(__name__)

# =======================
# ROUTE: Home Page
# =======================
@app.route('/')
def index():
    """
    Home page where the user selects prediction or simulation.
    """
    return render_template('index.html')

# =======================
# ROUTE: Climate Prediction
# =======================
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """
    Handles the climate prediction workflow:
    - Accepts number of years for prediction.
    - Loads sample/historical data.
    - Trains prediction model.
    - Generates future climate graphs.
    - Provides crop recommendations.
    """
    years_ahead = int(request.form.get('years_ahead', 10)) if request.method == 'POST' else 10

    # Load and process historical climate data
    df = load_sample_data()

    # Train prediction model
    models = train_model(df)

    # Predict future climate trends
    predicted_df = predict_climate(models, years_ahead)

    # Plot predicted temperature, rainfall, humidity
    graphs = generate_prediction_graphs(predicted_df)

    # Recommend suitable crops based on future climate
    crops = recommend_crops(predicted_df)

    return render_template('predict.html', graphs=graphs, crops=crops, years_ahead=years_ahead)

# =======================
# ROUTE: Climate Simulation
# =======================
@app.route('/simulate', methods=['GET', 'POST'])
def simulate():
    """
    Handles climate simulation workflow:
    - Accepts deforestation adjustment factor.
    - Loads and predicts baseline climate.
    - Simulates climate under user-defined land-use changes.
    - Compares baseline vs. simulated trends.
    """
    years_ahead = int(request.form.get('years_ahead', 10)) if request.method == 'POST' else 10
    deforestation_factor = float(request.form.get('deforestation_factor', 0.0)) if request.method == 'POST' else 0.0

    # Load and process historical climate data
    df = load_sample_data()

    # Train prediction model
    models = train_model(df)

    # Predict baseline climate
    baseline_df = predict_climate(models, years_ahead)

    # Apply user-defined simulation
    simulated_df = simulate_scenario(baseline_df, deforestation_factor)

    # Plot comparative graphs for temperature and rainfall
    graphs = generate_simulation_graphs(baseline_df, simulated_df)

    return render_template('simulate.html', graphs=graphs, years_ahead=years_ahead, deforestation_factor=deforestation_factor)

# =======================
# Helper Function: Generate Prediction Graphs
# =======================
def generate_prediction_graphs(predicted_df):
    """
    Creates Plotly graphs for predicted temperature, rainfall, and humidity.
    """
    graphs = {}

    # Temperature Graph
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(x=predicted_df['Year'], y=predicted_df['Temperature'], mode='lines', name='Temperature'))
    fig_temp.update_layout(title='Predicted Temperature Trends')

    # Rainfall Graph
    fig_rain = go.Figure()
    fig_rain.add_trace(go.Scatter(x=predicted_df['Year'], y=predicted_df['Rainfall'], mode='lines', name='Rainfall'))
    fig_rain.update_layout(title='Predicted Rainfall Trends')

    # Humidity Graph
    fig_hum = go.Figure()
    fig_hum.add_trace(go.Scatter(x=predicted_df['Year'], y=predicted_df['Humidity'], mode='lines', name='Humidity'))
    fig_hum.update_layout(title='Predicted Humidity Trends')

    # Embed the graphs into the HTML
    graphs['temp_graph'] = pio.to_html(fig_temp, full_html=False)
    graphs['rain_graph'] = pio.to_html(fig_rain, full_html=False)
    graphs['hum_graph'] = pio.to_html(fig_hum, full_html=False)

    return graphs

# =======================
# Helper Function: Generate Simulation Graphs
# =======================
def generate_simulation_graphs(baseline_df, simulated_df):
    """
    Creates comparative graphs for baseline vs simulated scenarios.
    """
    graphs = {}

    # Temperature Comparison Graph
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(x=baseline_df['Year'], y=baseline_df['Temperature'], mode='lines', name='Baseline'))
    fig_temp.add_trace(go.Scatter(x=simulated_df['Year'], y=simulated_df['Temperature'], mode='lines', name='Simulated'))
    fig_temp.update_layout(title='Temperature: Baseline vs Simulated')

    # Rainfall Comparison Graph
    fig_rain = go.Figure()
    fig_rain.add_trace(go.Scatter(x=baseline_df['Year'], y=baseline_df['Rainfall'], mode='lines', name='Baseline'))
    fig_rain.add_trace(go.Scatter(x=simulated_df['Year'], y=simulated_df['Rainfall'], mode='lines', name='Simulated'))
    fig_rain.update_layout(title='Rainfall: Baseline vs Simulated')

    # Embed the graphs into the HTML
    graphs['temp_graph'] = pio.to_html(fig_temp, full_html=False)
    graphs['rain_graph'] = pio.to_html(fig_rain, full_html=False)

    return graphs

# =======================
# Flask App Runner
# =======================
if __name__ == '__main__':
    app.run(debug=True)
