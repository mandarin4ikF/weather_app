import unittest
from geocoder import get_coordinates
from weather import get_weather_by_coords
class TestWeatherProject(unittest.TestCase):
    def test_geocoder_valid_address(self):
        coords = get_coordinates("Москва")
        self.assertIsNotNone(coords)
        self.assertEqual(len(coords), 2)
    def test_geocoder_invalid_address(self):
        coords = get_coordinates("asdasdasdasd")
        self.assertIsNone(coords)
    def test_weather_response(self):
        coords = get_coordinates("Москва")
        self.assertIsNotNone(coords)
        weather = get_weather_by_coords(*coords)
        self.assertIsNotNone(weather)
        self.assertIn('main', weather)
if __name__ == '__main__':
    unittest.main()
