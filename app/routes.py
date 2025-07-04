# app/routes.py

from flask import Blueprint, render_template, request
from .ml_model import train_model, predict_climate, simulate_scenario
from .data_utils import load_sample_data
from .recommend import recommend_crops
import plotly.io as pio
import plotly.graph_objects as go

# Initialize blueprint
main = Blueprint('main', __name__)

# ---------------------------
# ROUTE: Home Page
# ---------------------------
@main.route('/')
def index():
    return render_template('index.html')


# ---------------------------
# ROUTE: Climate Prediction
# ---------------------------
@main.route('/predict', methods=['GET', 'POST'])
def predict():
    years_ahead = int(request.form.get('years_ahead', 10)) if request.method == 'POST' else 10
    df = load_sample_data()
    models = train_model(df)
    predicted_df = predict_climate(models, years_ahead)
    graphs = generate_prediction_graphs(predicted_df)
    crops = recommend_crops(predicted_df)

    return render_template('predict.html', graphs=graphs, crops=crops, years_ahead=years_ahead)


# ---------------------------
# ROUTE: Climate Simulation
# ---------------------------
@main.route('/simulate', methods=['GET', 'POST'])
def simulate():
    years_ahead = int(request.form.get('years_ahead', 10)) if request.method == 'POST' else 10
    deforestation_factor = float(request.form.get('deforestation_factor', 0.0)) if request.method == 'POST' else 0.0

    df = load_sample_data()
    models = train_model(df)
    baseline_df = predict_climate(models, years_ahead)
    simulated_df = simulate_scenario(baseline_df, deforestation_factor)
    graphs = generate_simulation_graphs(baseline_df, simulated_df)

    return render_template('simulate.html', graphs=graphs, years_ahead=years_ahead, deforestation_factor=deforestation_factor)


# ---------------------------
# Helper: Prediction Graphs
# ---------------------------
def generate_prediction_graphs(predicted_df):
    graphs = {}

    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(x=predicted_df['Year'], y=predicted_df['Temperature'], mode='lines', name='Temperature'))
    fig_temp.update_layout(title='Predicted Temperature Trends')
    
    fig_rain = go.Figure()
    fig_rain.add_trace(go.Scatter(x=predicted_df['Year'], y=predicted_df['Rainfall'], mode='lines', name='Rainfall'))
    fig_rain.update_layout(title='Predicted Rainfall Trends')
    
    fig_hum = go.Figure()
    fig_hum.add_trace(go.Scatter(x=predicted_df['Year'], y=predicted_df['Humidity'], mode='lines', name='Humidity'))
    fig_hum.update_layout(title='Predicted Humidity Trends')

    graphs['temp_graph'] = pio.to_html(fig_temp, full_html=False)
    graphs['rain_graph'] = pio.to_html(fig_rain, full_html=False)
    graphs['hum_graph'] = pio.to_html(fig_hum, full_html=False)

    return graphs


# ---------------------------
# Helper: Simulation Graphs
# ---------------------------
def generate_simulation_graphs(baseline_df, simulated_df):
    graphs = {}

    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(x=baseline_df['Year'], y=baseline_df['Temperature'], mode='lines', name='Baseline'))
    fig_temp.add_trace(go.Scatter(x=simulated_df['Year'], y=simulated_df['Temperature'], mode='lines', name='Simulated'))
    fig_temp.update_layout(title='Temperature: Baseline vs Simulated')

    fig_rain = go.Figure()
    fig_rain.add_trace(go.Scatter(x=baseline_df['Year'], y=baseline_df['Rainfall'], mode='lines', name='Baseline'))
    fig_rain.add_trace(go.Scatter(x=simulated_df['Year'], y=simulated_df['Rainfall'], mode='lines', name='Simulated'))
    fig_rain.update_layout(title='Rainfall: Baseline vs Simulated')

    graphs['temp_graph'] = pio.to_html(fig_temp, full_html=False)
    graphs['rain_graph'] = pio.to_html(fig_rain, full_html=False)

    return graphs
