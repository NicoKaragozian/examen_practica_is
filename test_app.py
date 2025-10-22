import unittest

from fastapi.testclient import TestClient
from main import app


class TestApp(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_calculate_shipping_basic(self):
        payload = {
            "weight": 2.5,
            "distance": 100,
            "base_rate": 0.5,
            "discount": 0.1,
        }
        response = self.client.post("/calculate-shipping", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("cost", data)
        self.assertIsInstance(data["cost"], (int, float))
        self.assertGreaterEqual(data["cost"], 0)

    def test_validation_errors(self):
        # Negative values should fail validation
        bad = {"weight": -1, "distance": 10}
        response = self.client.post("/calculate-shipping", json=bad)
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main(verbosity=2)

