import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ValidacaoFiscalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    produto_id: uuid.UUID
    status: str
    codigo: str
    mensagem: str
    criado_em: datetime


class ValidarVendaRequest(BaseModel):
    produto_id: uuid.UUID
    uf_destino: str
    preco_venda: float
