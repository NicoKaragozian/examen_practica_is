from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional

# Importamos nuestras estrategias
from strategies import (
    ShippingStrategy, LocalShippingStrategy, NationalShippingStrategy, InternationalShippingStrategy,
    DiscountStrategy, NoDiscountStrategy, PrimeUserStrategy, NewUserStrategy
)

app = FastAPI(title="API de Costos de Envío")

# --- 1. Modelos de Datos (Pydantic) ---

class Item(BaseModel):
    id: int
    weight_kg: float
    category: str

class ShippingRequest(BaseModel):
    items: List[Item]
    destination: str
    coupon: Optional[str] = None # Opcional, puede ser nulo

class ShippingResponse(BaseModel):
    base_cost: float = Field(..., example=15.0)
    discount_applied: float = Field(..., example=2.25)
    final_cost: float = Field(..., example=12.75)


# --- 2. "Fábricas" de Estrategias ---
# Diccionarios que mapean el string del JSON a nuestra clase de Estrategia

SHIPPING_STRATEGIES = {
    "local": LocalShippingStrategy(),
    "national": NationalShippingStrategy(),
    "international": InternationalShippingStrategy()
}

DISCOUNT_STRATEGIES = {
    "PRIME_USER": PrimeUserStrategy(),
    "NEW_USER": NewUserStrategy(),
}
# Usaremos NoDiscountStrategy como default
NO_DISCOUNT = NoDiscountStrategy()


# --- 3. Endpoint de la API ---

@app.post("/calculate-shipping", response_model=ShippingResponse)
async def calculate_shipping_cost(request: ShippingRequest):
    """
    Calcula el costo de envío basado en el peso total, destino y cupón.
    """
    
    # 1. Calcular peso total
    total_weight = sum(item.weight_kg for item in request.items)
    
    # 2. Seleccionar Estrategia de Envío
    shipping_strategy = SHIPPING_STRATEGIES.get(request.destination, LocalShippingStrategy()) # Default a local si no se encuentra
    
    # 3. Seleccionar Estrategia de Descuento
    discount_strategy = DISCOUNT_STRATEGIES.get(request.coupon, NO_DISCOUNT) # Default a sin descuento
    
    # 4. Aplicar Estrategias
    base_cost = shipping_strategy.calculate(total_weight)
    discount_applied = discount_strategy.apply_discount(base_cost)
    final_cost = base_cost - discount_applied
    
    # 5. Devolver respuesta
    return ShippingResponse(
        base_cost=base_cost,
        discount_applied=discount_applied,
        final_cost=final_cost
    )

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Costos de Envío. Use el endpoint /docs para la documentación."}
