# app/recommend.py
# Crop lookup with ideal growing conditions
CROP_RECOMMENDATIONS = {
    'Maize': {
        'temp_min': 20, 'temp_max': 30,
        'rainfall_min': 600, 'rainfall_max': 1200
    },
    'Sorghum': {
        'temp_min': 25, 'temp_max': 35,
        'rainfall_min': 400, 'rainfall_max': 800
    },
    'Cassava': {
        'temp_min': 22, 'temp_max': 32,
        'rainfall_min': 500, 'rainfall_max': 1500
    },
    'Millet': {
        'temp_min': 24, 'temp_max': 34,
        'rainfall_min': 350, 'rainfall_max': 700
    },
    'Sweet Potato': {
        'temp_min': 20, 'temp_max': 30,
        'rainfall_min': 500, 'rainfall_max': 1300
    }
}


# ------------------------------------------
# Recommend Crops Based on Projected Climate
# ------------------------------------------
def recommend_crops(predicted_climate):
    """
    Suggests crops suitable for predicted climate conditions.
    Args:
        predicted_climate (pd.DataFrame): Forecasted climate data
    Returns:
        list: Crop names suitable for the predicted averages
    """
    avg_temp = predicted_climate['Temperature'].mean()
    avg_rain = predicted_climate['Rainfall'].mean()

    recommendations = []

    for crop, criteria in CROP_RECOMMENDATIONS.items():
        temp_ok = criteria['temp_min'] <= avg_temp <= criteria['temp_max']
        rain_ok = criteria['rainfall_min'] <= avg_rain <= criteria['rainfall_max']

        if temp_ok and rain_ok:
            recommendations.append(crop)

    return recommendations if recommendations else ["No suitable crops found"]
