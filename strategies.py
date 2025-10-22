"""Strategy pattern skeletons for shipping cost and discounts.

Define abstract interfaces and a simple calculator context to compose
shipping and discount strategies. Concrete strategies can be implemented in
separate modules and injected where needed.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class ShippingStrategy(ABC):
    """Defines the interface for shipping cost calculation strategies."""

    @abstractmethod
    def calculate(self, *, weight: float, distance: float, base_rate: float) -> float:
        """Compute shipping cost given core inputs."""
        raise NotImplementedError


class DiscountStrategy(ABC):
    """Defines the interface for discount application strategies."""

    @abstractmethod
    def apply(self, *, cost: float) -> float:
        """Return discounted cost based on a strategy-specific rule."""
        raise NotImplementedError


class ShippingCostCalculator:
    """Composition root for strategies.

    Example:

        calculator = ShippingCostCalculator(FixedRateStrategy(), TenPercentOff())
        total = calculator.calculate(weight=2.0, distance=100, base_rate=0.5)
    """

    def __init__(
        self,
        shipping_strategy: ShippingStrategy,
        discount_strategy: Optional[DiscountStrategy] = None,
    ) -> None:
        self.shipping_strategy = shipping_strategy
        self.discount_strategy = discount_strategy

    def calculate(self, *, weight: float, distance: float, base_rate: float) -> float:
        cost = self.shipping_strategy.calculate(
            weight=weight, distance=distance, base_rate=base_rate
        )
        if self.discount_strategy is not None:
            cost = self.discount_strategy.apply(cost=cost)
        return cost

