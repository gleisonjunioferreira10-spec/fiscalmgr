import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_empresa_id
from app.db.session import get_db
from app.modules.dashboard.service import resumo_auditoria

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/auditoria")
def auditoria_fiscal(
    db: Session = Depends(get_db),
    empresa_id: uuid.UUID = Depends(get_current_empresa_id),
):
    return resumo_auditoria(db, empresa_id)
