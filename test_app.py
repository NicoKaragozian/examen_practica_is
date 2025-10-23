import unittest
from fastapi.testclient import TestClient
from main import app

class TestShippingAPI(unittest.TestCase):
    """
    Pruebas para el endpoint /calculate-shipping de la API.
    """
    
    def setUp(self):
        # El TestClient nos permite hacer 'requests' falsos a nuestra app
        self.client = TestClient(app) 

    def test_calculate_local_no_discount(self):
        # 1. Preparar el JSON de prueba
        test_payload = {
            "items": [{"id": 1, "weight_kg": 2.0, "category": "books"}], # 2kg total
            "destination": "local",
            "coupon": None
        }
        
        # 2. Hacer el POST request
        response = self.client.post("/calculate-shipping", json=test_payload)
        
        # 3. Verificar resultados
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Lógica: Local = 5 + (1 * 2kg) = 7.0
        # Descuento: 0.0
        self.assertAlmostEqual(data["base_cost"], 7.0)
        self.assertAlmostEqual(data["discount_applied"], 0.0)
        self.assertAlmostEqual(data["final_cost"], 7.0)

    def test_calculate_international_prime_discount(self):
        test_payload = {
            "items": [
                {"id": 1, "weight_kg": 1.0, "category": "electronics"}, # 1kg
                {"id": 2, "weight_kg": 3.0, "category": "other"}      # 3kg
            ], # 4kg total
            "destination": "international",
            "coupon": "PRIME_USER"
        }
        
        response = self.client.post("/calculate-shipping", json=test_payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Lógica: International = 25 + (5 * 4kg) = 45.0
        # Descuento: 15% de 45.0 = 6.75
        # Final: 45.0 - 6.75 = 38.25
        self.assertAlmostEqual(data["base_cost"], 45.0)
        self.assertAlmostEqual(data["discount_applied"], 6.75)
        self.assertAlmostEqual(data["final_cost"], 38.25)

if __name__ == '__main__':
    unittest.main()
