from fastapi import APIRouter

from app.api.v1 import dashboard, produtos, regras_uf, validador

api_router = APIRouter()
api_router.include_router(produtos.router)
api_router.include_router(regras_uf.router)
api_router.include_router(validador.router)
api_router.include_router(dashboard.router)
