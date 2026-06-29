from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import criar_access_token, hash_senha, verificar_senha
from app.db.session import get_db
from app.models.empresa import Empresa
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, RegistroRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registro", response_model=TokenResponse, status_code=201)
def registrar(payload: RegistroRequest, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == payload.email).first():
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    if db.query(Empresa).filter(Empresa.cnpj == payload.empresa.cnpj).first():
        raise HTTPException(status_code=409, detail="CNPJ já cadastrado")

    empresa = Empresa(nome=payload.empresa.nome, cnpj=payload.empresa.cnpj)
    db.add(empresa)
    db.flush()

    usuario = Usuario(
        empresa_id=empresa.id,
        nome=payload.nome_usuario,
        email=payload.email,
        senha_hash=hash_senha(payload.senha),
        role="admin",
    )
    db.add(usuario)
    db.commit()

    token = criar_access_token(usuario.id, empresa.id)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == payload.email).first()
    if not usuario or not usuario.ativo or not verificar_senha(payload.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_access_token(usuario.id, usuario.empresa_id)
    return TokenResponse(access_token=token)
