import unittest
import json
from app import app  # Assuming your Flask app is in a file named app.py

# Global variables definition (if needed, although it's generally better to avoid global state in tests)
n_clients = 1000

class TestDefaultPredictAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_welcome(self):
        response = self.app.get('/')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "Hello world! Welcome to the falask API!")

    def test_load_client_list(self):
        response = self.app.get('/client_list')
        id_list = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(id_list, list)
        self.assertEqual(len(id_list), n_clients)

        # Assuming first_id is supposed to be the first element in your client list
        first_id = id_list[0]
        self.assertEqual(first_id, 438333)

    def test_load_client(self):
        client_id = 438333
        response = self.app.get(f'/client?id={client_id}')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['DAYS_BIRTH'], 29)
        self.assertEqual(data['AMT_ANNUITY'], 19908.0)
        self.assertEqual(data['AMT_CREDIT'], 252000.0)
        self.assertEqual(data['AMT_INCOME_TOTAL'], 315000.0)

    def test_load_data(self):
        col = 'DAYS_BIRTH'
        response = self.app.get(f'/data?col={col}')
        age_list = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(age_list, list)
        self.assertEqual(len(age_list), n_clients)

        # Assuming first_age is supposed to be the first element in your age list
        first_age = 29.85753424657534
        self.assertAlmostEqual(age_list[0], first_age, places=5)  # Use places to account for floating-point precision

    def test_predict_default(self):
        client_id = 438333
        response = self.app.get(f'/predict_default?id_client={client_id}')
        prediction = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(prediction['proba_0'], 0.0022691398703050814, places=5)
        self.assertAlmostEqual(prediction['proba_1'], 0.9977308601296949, places=5)

if __name__ == '__main__':
    unittest.main()

    
