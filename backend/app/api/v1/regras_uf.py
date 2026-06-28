import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_empresa_id
from app.db.session import get_db
from app.models.produto import Produto, RegraTributariaUF
from app.schemas.regra_uf import RegraTributariaUFCreate, RegraTributariaUFOut

router = APIRouter(prefix="/regras-uf", tags=["regras-uf"])


def _validar_produto_da_empresa(db: Session, produto_id: uuid.UUID, empresa_id: uuid.UUID) -> None:
    produto = db.get(Produto, produto_id)
    if not produto or produto.empresa_id != empresa_id:
        raise HTTPException(status_code=404, detail="Produto não encontrado")


@router.post("", response_model=RegraTributariaUFOut, status_code=201)
def criar_regra(
    payload: RegraTributariaUFCreate,
    db: Session = Depends(get_db),
    empresa_id: uuid.UUID = Depends(get_current_empresa_id),
):
    _validar_produto_da_empresa(db, payload.produto_id, empresa_id)
    regra = RegraTributariaUF(**payload.model_dump())
    db.add(regra)
    db.commit()
    db.refresh(regra)
    return regra


@router.get("", response_model=list[RegraTributariaUFOut])
def listar_regras(
    produto_id: uuid.UUID,
    db: Session = Depends(get_db),
    empresa_id: uuid.UUID = Depends(get_current_empresa_id),
):
    _validar_produto_da_empresa(db, produto_id, empresa_id)
    return db.query(RegraTributariaUF).filter(RegraTributariaUF.produto_id == produto_id).all()


@router.delete("/{regra_id}", status_code=204)
def remover_regra(
    regra_id: uuid.UUID,
    db: Session = Depends(get_db),
    empresa_id: uuid.UUID = Depends(get_current_empresa_id),
):
    regra = db.get(RegraTributariaUF, regra_id)
    if not regra:
        raise HTTPException(status_code=404, detail="Regra não encontrada")
    _validar_produto_da_empresa(db, regra.produto_id, empresa_id)
    db.delete(regra)
    db.commit()
