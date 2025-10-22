import unittest

from fastapi.testclient import TestClient
from main import app


class TestApp(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_calculate_shipping_local_prime(self):
        payload = {
            "items": [
                {"id": 1, "weight_kg": 0.5, "category": "electronics"},
                {"id": 2, "weight_kg": 2.0, "category": "books"},
            ],
            "destination": "local",
            "coupon": "PRIME_USER",
        }
        response = self.client.post("/calculate-shipping", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # total weight = 2.5; local base = 5 + 1*2.5 = 7.5; prime 15% = 1.125; final = 6.375
        self.assertAlmostEqual(data["base_cost"], 7.5, places=2)
        self.assertAlmostEqual(data["discount_applied"], 1.12, places=2)
        self.assertAlmostEqual(data["final_cost"], 6.38, places=2)

    def test_invalid_destination(self):
        payload = {
            "items": [{"id": 1, "weight_kg": 1.0, "category": "x"}],
            "destination": "moon",
            "coupon": None,
        }
        response = self.client.post("/calculate-shipping", json=payload)
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main(verbosity=2)
