import unittest
import pandas as pd
from climaproj.ml_model import load_sample_data, train_model, predict_climate, simulate_scenario

class TestMLModel(unittest.TestCase):

    def setUp(self):
        """Load data and train models before each test."""
        self.df = load_sample_data()
        self.models = train_model(self.df)

    def test_load_sample_data_structure(self):
        """Ensure loaded data has required columns."""
        expected_columns = {'Year', 'Temperature', 'Rainfall', 'Humidity'}
        self.assertTrue(expected_columns.issubset(set(self.df.columns)))
        self.assertEqual(len(self.df), 25)

    def test_train_model_outputs(self):
        """Test model training returns dict with correct keys."""
        self.assertIn('Temperature', self.models)
        self.assertIn('Rainfall', self.models)
        self.assertIn('Humidity', self.models)

    def test_predict_climate_output_shape(self):
        """Ensure climate prediction returns expected number of rows."""
        years_ahead = 10
        predicted_df = predict_climate(self.models, years_ahead)
        self.assertEqual(len(predicted_df), years_ahead)
        self.assertIn('Year', predicted_df.columns)
        self.assertIn('Temperature', predicted_df.columns)

    def test_simulate_scenario_effects(self):
        """Test deforestation increases temp & reduces rainfall."""
        baseline = predict_climate(self.models, 5)
        simulated = simulate_scenario(baseline, deforestation_factor=0.5)  # 50% deforestation

        self.assertTrue((simulated['Temperature'] > baseline['Temperature']).all())
        self.assertTrue((simulated['Rainfall'] < baseline['Rainfall']).all())


if __name__ == '__main__':
    unittest.main()
