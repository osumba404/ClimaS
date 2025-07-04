# app/recommend.py

# Static crop lookup (expandable)
crop_recommendations = {
    'Maize': {'temp_min': 20, 'temp_max': 30, 'rainfall_min': 600, 'rainfall_max': 1200},
    'Sorghum': {'temp_min': 25, 'temp_max': 35, 'rainfall_min': 400, 'rainfall_max': 800},
    'Cassava': {'temp_min': 22, 'temp_max': 32, 'rainfall_min': 500, 'rainfall_max': 1500}
}


# ===============================
# Recommend Crops Based on Climate
# ===============================
def recommend_crops(predicted_df):
    """
    Recommends crops suitable for projected climate conditions.

    Args:
        predicted_df (DataFrame): Future climate trends with 'Temperature' and 'Rainfall'.

    Returns:
        list: Suitable crops or fallback message.
    """
    recommendations = []
    avg_temp = predicted_df['Temperature'].mean()
    avg_rain = predicted_df['Rainfall'].mean()

    for crop, criteria in crop_recommendations.items():
        temp_ok = criteria['temp_min'] <= avg_temp <= criteria['temp_max']
        rain_ok = criteria['rainfall_min'] <= avg_rain <= criteria['rainfall_max']

        if temp_ok and rain_ok:
            recommendations.append(crop)

    return recommendations if recommendations else ["No suitable crops found"]
