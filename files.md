climas/
│
├── app/                             # Main application package
│   ├── __init__.py                  # Flask app factory
│   ├── routes.py                    # Flask routes (/, /predict, /simulate, /recommend)
│   ├── ml_model.py                  # AI/ML logic (model training, prediction, feature importance)
│   ├── data_utils.py                # Data fetching, preprocessing utilities
│   ├── recommend.py                 # Crop recommendation logic
│   ├── static/                      # Static files (CSS, JS, images)
│   │   ├── style.css
│   │   └── scripts.js
│   ├── templates/                   # HTML templates
│   │   ├── base.html                # Base layout (includes navbar/footer)
│   │   ├── index.html               # Home page with region selection & graphs
│   │   ├── predict.html             # Shows climate predictions
│   │   ├── simulate.html            # Climate simulation interface
│   │   └── recommend.html           # Crop recommendation display
│   └── models/                      # Trained models & preprocessing files
│       └── climate_model.pkl
│
├── datasets/                        # Raw and processed datasets
│   ├── raw/                         # Original downloaded datasets
│   └── processed/                   # Cleaned, ready-to-use data files
│
├── .env                             # API keys (e.g., OpenWeatherMap), Flask secrets
├── requirements.txt                 # Python dependencies
├── app.py                           # App entry point
└── README.md                        # Project documentation

