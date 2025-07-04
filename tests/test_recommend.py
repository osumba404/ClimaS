# run test with: python -m unittest discover tests



import unittest
import pandas as pd
from climaproj.recommend import recommend_crops, CROP_RECOMMENDATIONS

class TestCropRecommendations(unittest.TestCase):

    def test_recommendation_for_maize_conditions(self):
        """Maize should be recommended within ideal climate range."""
        climate = pd.DataFrame({
            'Temperature': [25] * 10,
            'Rainfall': [900] * 10
        })
        crops = recommend_crops(climate)
        self.assertIn('Maize', crops)

    def test_no_crops_when_conditions_bad(self):
        """Returns fallback message if climate is unsuitable."""
        climate = pd.DataFrame({
            'Temperature': [40] * 10,
            'Rainfall': [100] * 10
        })
        crops = recommend_crops(climate)
        self.assertEqual(crops, ["No suitable crops found"])

    def test_multiple_crops_possible(self):
        """Multiple crops can be recommended if all match."""
        climate = pd.DataFrame({
            'Temperature': [26] * 10,
            'Rainfall': [700] * 10
        })
        crops = recommend_crops(climate)
        expected = {'Maize', 'Sorghum', 'Cassava', 'Sweet Potato'}
        self.assertTrue(expected.intersection(set(crops)))


if __name__ == '__main__':
    unittest.main()
