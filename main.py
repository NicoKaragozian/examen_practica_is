from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="Shipping Cost API", version="0.1.0")


class ShippingRequest(BaseModel):
    weight: float = Field(..., ge=0, description="Package weight in kg")
    distance: float = Field(..., ge=0, description="Shipping distance in km")
    base_rate: float = Field(1.0, ge=0, description="Base rate per kg*km")
    discount: float = Field(0.0, ge=0.0, le=1.0, description="Discount fraction 0-1")


class ShippingResponse(BaseModel):
    cost: float
    currency: str = "USD"


@app.post("/calculate-shipping", response_model=ShippingResponse)
def calculate_shipping(payload: ShippingRequest) -> ShippingResponse:
    """Calculate a simple shipping cost.

    This is a baseline implementation that multiplies weight, distance, and a
    configurable base rate, then optionally applies a discount fraction.

    The design intentionally keeps the core logic simple so strategies can be
    plugged in later (see `strategies.py`).
    """
    gross = payload.weight * payload.distance * payload.base_rate
    final = gross * (1 - payload.discount)
    return ShippingResponse(cost=round(final, 2), currency="USD")

