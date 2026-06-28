import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.dashboard.service import resumo_auditoria

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/auditoria")
def auditoria_fiscal(empresa_id: uuid.UUID, db: Session = Depends(get_db)):
    return resumo_auditoria(db, empresa_id)
