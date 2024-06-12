# Import packages
import unittest
from app import app  # Importez votre application Flask directement depuis le fichier app.py

# Global variables definition
n_clients = 1000

# API tests
class TestDefaulPredictAPI(unittest.TestCase):

    def setUp(self):
        # Créez un client de test Flask pour simuler les requêtes HTTP
        self.app = app.test_client()

    # Test # 1
    def test_welcome(self):
        # Effectuez une requête GET à l'endpoint racine de l'API
        response = self.app.get('/')
        
        # Testez la réponse
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello world! Welcome to the falask API!")

    # Test # 2
    def test_load_client_list(self):
        # Effectuez une requête GET à l'endpoint '/client_list' de l'API
        response = self.app.get('/client_list')
        
        # Testez la réponse
        self.assertEqual(response.status_code, 200)

        # Testez le format de la réponse
        id_list = response.json()
        self.assertIsInstance(id_list, list)
        self.assertEqual(len(id_list), n_clients)
        self.assertEqual(id_list[0], 438333)  # Vérifiez le premier ID de la liste

    # Test # 3
    def test_load_client(self):
        client_id = 438333
        # Effectuez une requête GET à l'endpoint '/client' avec l'ID du client
        response = self.app.get(f'/client?id={client_id}')
        
        # Testez la réponse
        self.assertEqual(response.status_code, 200)

        # Testez les données du client
        client = response.json()
        self.assertEqual(client['AMT_ANNUITY'], 19908.0)
        self.assertEqual(client['AMT_CREDIT'], 252000.0)
        self.assertEqual(client['AMT_INCOME_TOTAL'], 315000.0)
        self.assertEqual(client['DAYS_BIRTH'], 29)

    # Test # 4
    def test_load_data(self):
        col = 'DAYS_BIRTH'
        # Effectuez une requête GET à l'endpoint '/data' avec la colonne spécifiée
        response = self.app.get(f'/data?col={col}')
        
        # Testez la réponse
        self.assertEqual(response.status_code, 200)

        # Testez le format des données
        age_list = response.json()
        self.assertIsInstance(age_list, list)
        self.assertEqual(len(age_list), n_clients)
        self.assertAlmostEqual(age_list[0], 29.85753424657534)  # Utilisez `assertAlmostEqual` pour les valeurs flottantes

    # Test # 5
    def test_predict_default(self):
        client_id = 438333
        # Effectuez une requête GET à l'endpoint '/predict_default' avec l'ID du client
        response = self.app.get(f'/predict_default?id_client={client_id}')
        
        # Testez la réponse
        self.assertEqual(response.status_code, 200)

        # Testez la prédiction
        prediction = response.json()
        self.assertAlmostEqual(prediction['proba_0'], 0.0022691398703050814)
        self.assertAlmostEqual(prediction['proba_1'], 0.9977308601296949)

if __name__ == '__main__':
    unittest.main()
