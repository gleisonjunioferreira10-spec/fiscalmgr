from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.produto import Produto
from app.modules.validador.service import ValidacaoBloqueadaError, validar_venda
from app.schemas.validacao import ValidacaoFiscalOut, ValidarVendaRequest

router = APIRouter(prefix="/validador", tags=["validador"])


@router.post("/validar-venda", response_model=list[ValidacaoFiscalOut])
def validar_venda_endpoint(payload: ValidarVendaRequest, db: Session = Depends(get_db)):
    produto = db.get(Produto, payload.produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    try:
        return validar_venda(db, produto, payload.uf_destino, payload.preco_venda)
    except ValidacaoBloqueadaError as exc:
        raise HTTPException(status_code=422, detail=exc.ocorrencias) from exc
