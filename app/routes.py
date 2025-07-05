# climas/app/routes.py
from flask import render_template, request, Blueprint
from . import ml_model, recommend, data_utils
import plotly
import plotly.graph_objs as go
import json
import pandas as pd

main_bp = Blueprint('main', __name__)

# --- Load models and data once when the app starts ---
MODELS, FEATURES = ml_model.load_model_and_artifacts()
HISTORICAL_DATA = data_utils.load_processed_data()

@main_bp.route('/')
def index():
    """Renders the main input page."""
    return render_template('index.html')

@main_bp.route('/results', methods=['POST'])
def results():
    """Handles form submission and displays all analysis results."""
    # 1. Get user input
    region = request.form['region']
    land_use_sim_perc = int(request.form.get('land_use_sim', 0))
    land_use_modifier = land_use_sim_perc / 100.0

    # 2. Historical Data Visualization
    historical_plots = ml_model.create_historical_plots(HISTORICAL_DATA)

    # 3. AI Model Insights
    feature_importance_plot = ml_model.create_feature_importance_plot(MODELS, FEATURES)
    
    # 4. Future Prediction (Baseline)
    baseline_df = ml_model.predict_future_climate(MODELS, FEATURES, 2024, 2038)
    
    # 5. Scenario Simulation
    sim_params = {'land_use_change': land_use_modifier}
    simulated_df = ml_model.predict_future_climate(MODELS, FEATURES, 2024, 2038, simulation_params=sim_params)
    simulation_plot = ml_model.create_simulation_comparison_plot(baseline_df, simulated_df)

    # 6. Crop Recommendation
    sim_climate_2035 = simulated_df[simulated_df['date'].dt.year == 2035]
    avg_sim_temp = sim_climate_2035['predicted_temperature'].mean()
    avg_sim_rain = sim_climate_2035['predicted_rainfall'].mean()
    recommendations = recommend.recommend_crops(avg_sim_temp, avg_sim_rain)
    
    sim_change_text = f"{land_use_sim_perc}% {'increase' if land_use_sim_perc >= 0 else 'decrease'} in land use intensity (e.g. deforestation)"

    return render_template(
        'results.html',
        region=region,
        historical_temp_json=historical_plots['temp'],
        historical_rain_json=historical_plots['rain'],
        feature_importance_json=feature_importance_plot,
        simulation_graph_json=simulation_plot,
        sim_change_text=sim_change_text,
        recommendations=recommendations,
        avg_sim_temp=avg_sim_temp,
        avg_sim_rain=avg_sim_rain
    )