import unittest
from strategies import (
    LocalShippingStrategy, NationalShippingStrategy, InternationalShippingStrategy,
    NoDiscountStrategy, PrimeUserStrategy, NewUserStrategy
)

class TestShippingStrategies(unittest.TestCase):
    """
    Pruebas para las estrategias de cálculo de envío[cite: 2665].
    """
    
    def test_local_shipping(self):
        strategy = LocalShippingStrategy()
        # Regla: 5.0 + (1.0 * kg)
        self.assertEqual(strategy.calculate(10), 15.0)
        self.assertEqual(strategy.calculate(0), 5.0)

    def test_national_shipping(self):
        strategy = NationalShippingStrategy()
        # Regla: 10.0 + (2.0 * kg)
        self.assertEqual(strategy.calculate(10), 30.0)
        
    def test_international_shipping(self):
        strategy = InternationalShippingStrategy()
        # Regla: 25.0 + (5.0 * kg)
        self.assertEqual(strategy.calculate(10), 75.0)

class TestDiscountStrategies(unittest.TestCase):
    """
    Pruebas para las estrategias de descuento.
    """

    def test_no_discount(self):
        strategy = NoDiscountStrategy()
        self.assertEqual(strategy.apply_discount(100.0), 0.0)

    def test_prime_user_discount(self):
        strategy = PrimeUserStrategy()
        # Regla: 15% de descuento
        self.assertEqual(strategy.apply_discount(100.0), 15.0)
        self.assertEqual(strategy.apply_discount(50.0), 7.5)

    def test_new_user_discount(self):
        strategy = NewUserStrategy()
        # Regla: $5 fijos, con tope del costo total
        self.assertEqual(strategy.apply_discount(100.0), 5.0)
        self.assertEqual(strategy.apply_discount(3.0), 3.0) # El descuento no puede ser mayor al costo
        self.assertEqual(strategy.apply_discount(5.0), 5.0)

if __name__ == '__main__':
    unittest.main() [cite: 2687]