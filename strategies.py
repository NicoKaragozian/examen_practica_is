"""Strategy pattern implementations for shipping cost and discounts.

Defines abstract interfaces, concrete strategies for shipping by destination
and discounts by coupon, plus a small composition helper and selector
utilities.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class ShippingStrategy(ABC):
    """Defines the interface for shipping cost calculation strategies."""

    @abstractmethod
    def calculate(self, *, total_weight: float) -> float:
        """Compute base shipping cost given total weight in kg."""
        raise NotImplementedError


class DiscountStrategy(ABC):
    """Defines the interface for discount application strategies."""

    @abstractmethod
    def apply(self, *, cost: float) -> float:
        """Return the discount amount (not the final cost)."""
        raise NotImplementedError


class ShippingCostCalculator:
    """Composition root for strategies."""

    def __init__(
        self,
        shipping_strategy: ShippingStrategy,
        discount_strategy: Optional[DiscountStrategy] = None,
    ) -> None:
        self.shipping_strategy = shipping_strategy
        self.discount_strategy = discount_strategy

    def compute(self, *, total_weight: float) -> tuple[float, float, float]:
        """Return (base_cost, discount_applied, final_cost)."""
        base_cost = self.shipping_strategy.calculate(total_weight=total_weight)
        discount_applied = 0.0
        if self.discount_strategy is not None:
            discount_applied = self.discount_strategy.apply(cost=base_cost)
        final_cost = max(base_cost - discount_applied, 0.0)
        return base_cost, discount_applied, final_cost


# Concrete Shipping Strategies

class LocalShippingStrategy(ShippingStrategy):
    """Local: $5 + ($1 * total_weight)."""

    def calculate(self, *, total_weight: float) -> float:
        return 5.0 + 1.0 * max(total_weight, 0.0)


class NationalShippingStrategy(ShippingStrategy):
    """National: $10 + ($2 * total_weight)."""

    def calculate(self, *, total_weight: float) -> float:
        return 10.0 + 2.0 * max(total_weight, 0.0)


class InternationalShippingStrategy(ShippingStrategy):
    """International: $25 + ($5 * total_weight)."""

    def calculate(self, *, total_weight: float) -> float:
        return 25.0 + 5.0 * max(total_weight, 0.0)


# Concrete Discount Strategies

class NoDiscountStrategy(DiscountStrategy):
    def apply(self, *, cost: float) -> float:
        return 0.0


class PrimeUserStrategy(DiscountStrategy):
    """15% off of base cost."""

    def apply(self, *, cost: float) -> float:
        return 0.15 * max(cost, 0.0)


class NewUserStrategy(DiscountStrategy):
    """Flat $5 off of base cost."""

    def apply(self, *, cost: float) -> float:
        return min(5.0, max(cost, 0.0))


# Selector helpers

def select_shipping_strategy(destination: str) -> ShippingStrategy:
    dest = (destination or "").strip().lower()
    if dest == "local":
        return LocalShippingStrategy()
    if dest == "national":
        return NationalShippingStrategy()
    if dest == "international":
        return InternationalShippingStrategy()
    # Default to raising so callers can handle validation at API layer
    raise ValueError(f"Unsupported destination: {destination}")


def select_discount_strategy(coupon: Optional[str]) -> DiscountStrategy:
    code = (coupon or "").strip().upper()
    if code == "PRIME_USER":
        return PrimeUserStrategy()
    if code == "NEW_USER":
        return NewUserStrategy()
    return NoDiscountStrategy()
