climas/                               # Root project folder
│
├── app/                             # Main Flask application logic
│   ├── __init__.py                  # Initializes Flask app, loads config, registers routes
│   ├── routes.py                    # Defines web routes: Home, Predict, Simulate, Recommend
│   ├── ml_model.py                  # Machine Learning logic: training, prediction, simulations
│   ├── data_utils.py                # Fetches, cleans, and processes climate data from APIs or files
│   ├── recommend.py                 # Contains logic to suggest crops based on predicted climate
│
│   ├── static/                      # Static files served by Flask (CSS, JS, Images)
│   │   ├── style.css                # Stylesheet for frontend UI
│   │   └── scripts.js               # Optional JS for frontend interactions (e.g., form validation)
│
│   ├── templates/                   # HTML templates rendered by Flask
│   │   ├── base.html                # Base layout with header, footer, shared structure
│   │   ├── index.html               # Landing page with region selection & forms
│   │   ├── predict.html             # Displays climate prediction results and graphs
│   │   ├── simulate.html            # Allows scenario-based simulations with result display
│   │   └── recommend.html           # Shows recommended crops based on predictions
│
│   └── models/                      # Stores trained ML models and preprocessing artifacts
│       └── climate_model.pkl        # Saved model for future predictions (updated after training)
│
├── datasets/                        # Climate datasets used for training and analysis
│   ├── raw/                         # Original, untouched datasets from sources like WorldClim, NASA
│   └── processed/                   # Cleaned, structured datasets ready for modeling
│
├── notebooks/                       # Jupyter Notebooks for exploratory analysis & prototyping
│   ├── data_exploration.ipynb       # Visualize historical climate trends, correlations
│   └── model_training.ipynb         # Experiment with model development interactively
│
├── logs/                            # Logs for monitoring model training and app behavior
│   ├── model_training.log           # Records training performance, errors, timestamps
│   └── app.log                      # General Flask app runtime logs (errors, requests)
│
├── tests/                           # Automated tests to validate app logic and model integrity
│   ├── test_data_utils.py           # Unit tests for data fetching, cleaning, and preprocessing
│   └── test_ml_model.py             # Unit tests for ML model functions: predict, simulate, etc.
│
├── .env                             # Environment variables (API keys, Flask secrets, config settings)
├── requirements.txt                 # Python package dependencies for the entire project
├── app.py                           # Main entry point that runs the Flask application
├── config.py                        # Set up SQLite db
└── README.md                        # Project overview, setup instructions, usage guide
