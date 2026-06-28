from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import get_current_empresa_id
from app.modules.tributario.aliquotas_uf import ESTADOS
from app.modules.tributario.service import sugerir_regra_uf

router = APIRouter(prefix="/tributario", tags=["tributario"])


@router.get("/sugestao-uf")
def sugestao_uf(
    uf_origem: str,
    uf_destino: str,
    importado: bool = False,
    _empresa_id=Depends(get_current_empresa_id),
):
    if uf_origem.upper() not in ESTADOS or uf_destino.upper() not in ESTADOS:
        raise HTTPException(status_code=422, detail="UF inválida")
    return sugerir_regra_uf(uf_origem, uf_destino, importado=importado)
