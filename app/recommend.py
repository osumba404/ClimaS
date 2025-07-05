# climas/app/recommend.py
def recommend_crops(avg_temp, avg_rain):
    """Simple rule-based crop recommendation engine."""
    recommendations = []
    if 20 <= avg_temp <= 30 and avg_rain > 60:
        recommendations.append("Maize: Suitable for warm temperatures and moderate rainfall.")
    if avg_temp > 28 and avg_rain < 50:
        recommendations.append("Sorghum: Highly drought-resistant and thrives in heat.")
    if 18 <= avg_temp <= 25 and avg_rain > 80:
        recommendations.append("Coffee (Arabica): Prefers cooler, high-altitude climates with good rainfall.")
    if 25 <= avg_temp <= 35 and avg_rain > 70:
        recommendations.append("Cassava: Very hardy, tolerates heat and lower rainfall.")
    if 15 <= avg_temp <= 25 and 50 <= avg_rain <= 80:
        recommendations.append("Wheat: Prefers cooler temperatures and moderate rainfall.")
        
    if not recommendations:
        recommendations.append("Conditions may not be ideal for common crops. Consider specialized or resilient varieties.")
    return recommendations