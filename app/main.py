# ---------------------------------------------------------
# © 2025 Roberto De Las Morenas García o CodeHarlequin. Todos los derechos reservados.
# Este código es parte del proyecto ApiShop.
# Licencia: GPL-3.0
# ---------------------------------------------------------

from fastapi import FastAPI
from app.routers import product, category

app = FastAPI(
    title="ApiShop",
    description="API avanzada para gestión de tienda",
    version="1.0.0"
)

app.include_router(product.router)
app.include_router(category.router)