# API de Costos de Envío (FastAPI)

Implementación para el examen de práctica: calcula costo de envío usando el patrón Strategy para destino y para descuentos.

## Endpoint
- POST `/calculate-shipping`
  - Input JSON:
    {
      "items": [
        { "id": 1, "weight_kg": 0.5, "category": "electronics" },
        { "id": 2, "weight_kg": 2.0, "category": "books" }
      ],
      "destination": "local" | "national" | "international",
      "coupon": null | "PRIME_USER" | "NEW_USER"
    }
  - Output JSON:
    {
      "base_cost": number,
      "discount_applied": number,
      "final_cost": number
    }

Reglas de ejemplo:
- Local: $5 + ($1 × peso_total)
- National: $10 + ($2 × peso_total)
- International: $25 + ($5 × peso_total)
- Descuentos: PRIME_USER 15%, NEW_USER $5 fijos, sin cupón 0

## Ejecutar localmente
- Instalar dependencias: `pip install -r requirements.txt`
- Correr tests: `python -m unittest -v`
- Iniciar API: `uvicorn main:app --reload`

## CI
- Workflow en `.github/workflows/ci.yml` ejecuta `pip install -r requirements.txt` y `python -m unittest -v` en `push`/`pull_request` a `main`.

## Despliegue (Render.com)
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port 10000`
