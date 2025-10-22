from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional

from strategies import (
    ShippingCostCalculator,
    select_shipping_strategy,
    select_discount_strategy,
)


app = FastAPI(title="Shipping Cost API", version="1.0.0")


class Item(BaseModel):
    id: int
    weight_kg: float = Field(..., ge=0)
    category: str


class ShippingInput(BaseModel):
    items: List[Item]
    destination: str
    coupon: Optional[str] = None

    @validator("destination")
    def validate_destination(cls, v: str) -> str:
        allowed = {"local", "national", "international"}
        if v is None:
            raise ValueError("destination is required")
        if v.lower() not in allowed:
            raise ValueError("destination must be local, national, or international")
        return v


class ShippingOutput(BaseModel):
    base_cost: float
    discount_applied: float
    final_cost: float


@app.post("/calculate-shipping", response_model=ShippingOutput)
def calculate_shipping(payload: ShippingInput) -> ShippingOutput:
    """Calculate shipping cost from a list of items, destination, and coupon.

    Base cost is determined by destination strategy, using total weight.
    Discount applied is determined by coupon strategy.
    """
    total_weight = sum(item.weight_kg for item in payload.items)

    try:
        shipping_strategy = select_shipping_strategy(payload.destination)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    discount_strategy = select_discount_strategy(payload.coupon)
    calculator = ShippingCostCalculator(
        shipping_strategy=shipping_strategy, discount_strategy=discount_strategy
    )

    base_cost, discount_applied, final_cost = calculator.compute(total_weight=total_weight)

    return ShippingOutput(
        base_cost=round(base_cost, 2),
        discount_applied=round(discount_applied, 2),
        final_cost=round(final_cost, 2),
    )
