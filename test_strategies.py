import unittest

from strategies import (
    LocalShippingStrategy,
    NationalShippingStrategy,
    InternationalShippingStrategy,
    NoDiscountStrategy,
    PrimeUserStrategy,
    NewUserStrategy,
)


class TestShippingStrategies(unittest.TestCase):
    def test_local_shipping(self):
        s = LocalShippingStrategy()
        self.assertEqual(s.calculate(total_weight=0), 5.0)
        self.assertEqual(s.calculate(total_weight=3), 8.0)  # 5 + 1*3

    def test_national_shipping(self):
        s = NationalShippingStrategy()
        self.assertEqual(s.calculate(total_weight=0), 10.0)
        self.assertEqual(s.calculate(total_weight=3), 16.0)  # 10 + 2*3

    def test_international_shipping(self):
        s = InternationalShippingStrategy()
        self.assertEqual(s.calculate(total_weight=0), 25.0)
        self.assertEqual(s.calculate(total_weight=3), 40.0)  # 25 + 5*3


class TestDiscountStrategies(unittest.TestCase):
    def test_no_discount(self):
        d = NoDiscountStrategy()
        self.assertEqual(d.apply(cost=100.0), 0.0)

    def test_prime_user(self):
        d = PrimeUserStrategy()
        self.assertAlmostEqual(d.apply(cost=100.0), 15.0, places=2)

    def test_new_user(self):
        d = NewUserStrategy()
        self.assertAlmostEqual(d.apply(cost=100.0), 5.0, places=2)
        # Discount should not exceed cost
        self.assertAlmostEqual(d.apply(cost=3.0), 3.0, places=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

