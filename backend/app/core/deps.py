import uuid

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import decodificar_access_token
from app.db.session import get_db
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    try:
        payload = decodificar_access_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado") from exc

    usuario = db.get(Usuario, uuid.UUID(payload["sub"]))
    if not usuario or not usuario.ativo:
        raise HTTPException(status_code=401, detail="Usuário inválido")
    return usuario


def get_current_empresa_id(usuario: Usuario = Depends(get_current_user)) -> uuid.UUID:
    return usuario.empresa_id


def get_db_tenant(
    db: Session = Depends(get_db),
    empresa_id: uuid.UUID = Depends(get_current_empresa_id),
) -> Session:
    """Sessão de banco com o tenant atual configurado para as políticas de Row-Level Security.

    O Postgres só aplica as políticas dentro da transação onde `app.current_empresa_id`
    foi definido (SET LOCAL); por isso esta dependência precisa substituir `get_db` em
    qualquer rota que leia/escreva tabelas multi-tenant.
    """
    if db.bind is not None and db.bind.dialect.name == "postgresql":
        db.execute(text("SET LOCAL app.current_empresa_id = :empresa_id"), {"empresa_id": str(empresa_id)})
    return db
