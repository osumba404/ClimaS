# 🌍 ClimaS - Climate Smart: Predictive Climate Intelligence Platform

**ClimaS** is a Flask-based web application that empowers users to visualize historical climate trends, predict future conditions, simulate human-driven scenarios like deforestation, and receive tailored crop recommendations based on projected climates. The goal is to support data-driven climate resilience, particularly for agriculture in vulnerable regions.

---

## 🚀 Project Features

✅ Collect historical and live climate data for a chosen region  
✅ Predict temperature, rainfall, and humidity trends for the next 5, 10, or 15 years  
✅ Identify key drivers of climate change using feature importance analysis  
✅ Interactive graphs for exploring temperature, rainfall, and other trends  
✅ Simulate land-use scenarios (e.g., deforestation increase, afforestation efforts)  
✅ Recommend climate-resilient crops based on projected environmental conditions  

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/osumba404/climas.git
cd climas

### 2️⃣ Install Required Packages

pip install -r requirements.txt

### 3️⃣ Configure Environment Variables

Create a .env file in the project root:
FLASK_SECRET=your_secret_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here

### 4️⃣ Run the Application

python app.py


##📊 Typical Workflow
1. User selects a region
2. System retrieves and processes historical climate data
3. Trends in temperature, rainfall, and humidity are displayed interactively
4. AI model predicts future climate conditions
5. Users simulate land-use changes like deforestation/afforestation
6. Updated projections shown based on simulations
7. System suggests crops best suited to the predicted climate

##🔧 Technologies Used
Flask — Python web framework
Pandas & Scikit-learn — Data preprocessing and machine learning
Matplotlib & Plotly — Visualizations and interactive graphs
OpenWeatherMap API — Real-time weather data integration
Jupyter Notebooks — Prototyping and data exploration


##💡 Potential Future Enhancements
Satellite imagery analysis for land cover detection (Sentinel-2, Landsat)
Integration with advanced forecasting APIs (e.g., Mistral AI)
Expanded simulation options: urban expansion, conservation zones
User accounts and scenario-saving capability
Mobile-friendly interface


##🤝 Contributing
Contributions are welcome! To contribute:

Fork the repository
Create a new feature branch
Commit your changes
Submit a pull request for review
Bug reports, feature suggestions, and code improvements are encouraged.