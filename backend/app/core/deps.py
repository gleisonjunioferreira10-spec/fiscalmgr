import uuid

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
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
