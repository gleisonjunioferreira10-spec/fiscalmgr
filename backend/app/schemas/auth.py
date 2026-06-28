import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


class EmpresaCreate(BaseModel):
    nome: str
    cnpj: str


class RegistroRequest(BaseModel):
    empresa: EmpresaCreate
    nome_usuario: str
    email: EmailStr
    senha: str


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    empresa_id: uuid.UUID
    nome: str
    email: str
    role: str
