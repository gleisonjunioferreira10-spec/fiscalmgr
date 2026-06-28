import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.produto import RegraTributariaUF
from app.schemas.regra_uf import RegraTributariaUFCreate, RegraTributariaUFOut

router = APIRouter(prefix="/regras-uf", tags=["regras-uf"])


@router.post("", response_model=RegraTributariaUFOut, status_code=201)
def criar_regra(payload: RegraTributariaUFCreate, db: Session = Depends(get_db)):
    regra = RegraTributariaUF(**payload.model_dump())
    db.add(regra)
    db.commit()
    db.refresh(regra)
    return regra


@router.get("", response_model=list[RegraTributariaUFOut])
def listar_regras(produto_id: uuid.UUID, db: Session = Depends(get_db)):
    return db.query(RegraTributariaUF).filter(RegraTributariaUF.produto_id == produto_id).all()


@router.delete("/{regra_id}", status_code=204)
def remover_regra(regra_id: uuid.UUID, db: Session = Depends(get_db)):
    regra = db.get(RegraTributariaUF, regra_id)
    if not regra:
        raise HTTPException(status_code=404, detail="Regra não encontrada")
    db.delete(regra)
    db.commit()
