from fastapi import APIRouter

from app.api.v1 import auth, dashboard, produtos, regras_uf, tributario, validador

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(produtos.router)
api_router.include_router(regras_uf.router)
api_router.include_router(tributario.router)
api_router.include_router(validador.router)
api_router.include_router(dashboard.router)
