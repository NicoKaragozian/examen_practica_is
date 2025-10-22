from abc import ABC, abstractmethod

# --- 1. Estrategias de Cálculo de Envío ---

class ShippingStrategy(ABC):
    """
    Interfaz para la Estrategia de Cálculo de Envío.
    """
    @abstractmethod
    def calculate(self, total_weight_kg: float) -> float:
        pass

class LocalShippingStrategy(ShippingStrategy):
    """
    Calcula el costo para envíos locales.
    Regla: $5 (base) + $1 por kg.
    """
    def calculate(self, total_weight_kg: float) -> float:
        return 5.0 + (1.0 * total_weight_kg)

class NationalShippingStrategy(ShippingStrategy):
    """
    Calcula el costo para envíos nacionales.
    Regla: $10 (base) + $2 por kg.
    """
    def calculate(self, total_weight_kg: float) -> float:
        return 10.0 + (2.0 * total_weight_kg)

class InternationalShippingStrategy(ShippingStrategy):
    """
    Calcula el costo para envíos internacionales.
    Regla: $25 (base) + $5 por kg.
    """
    def calculate(self, total_weight_kg: float) -> float:
        return 25.0 + (5.0 * total_weight_kg)

# --- 2. Estrategias de Descuento ---

class DiscountStrategy(ABC):
    """
    Interfaz para la Estrategia de Descuento.
    """
    @abstractmethod
    def apply_discount(self, base_cost: float) -> float:
        pass

class NoDiscountStrategy(DiscountStrategy):
    """
    No aplica ningún descuento.
    """
    def apply_discount(self, base_cost: float) -> float:
        return 0.0

class PrimeUserStrategy(DiscountStrategy):
    """
    Aplica un 15% de descuento para usuarios Prime.
    """
    def apply_discount(self, base_cost: float) -> float:
        return base_cost * 0.15

class NewUserStrategy(DiscountStrategy):
    """
    Aplica un descuento fijo de $5 para usuarios nuevos.
    """
    def apply_discount(self, base_cost: float) -> float:
        # Se asegura que el descuento no sea mayor al costo base
        return min(5.0, base_cost)