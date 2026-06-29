import uuid

from pydantic import BaseModel, ConfigDict


class RegraTributariaUFBase(BaseModel):
    uf_origem: str
    uf_destino: str
    aliquota_icms: float | None = None
    aliquota_icms_st: float | None = None
    mva_st: float | None = None
    aplica_st: bool = False
    aplica_difal: bool = False
    aplica_antecipacao: bool = False


class RegraTributariaUFCreate(RegraTributariaUFBase):
    produto_id: uuid.UUID


class RegraTributariaUFOut(RegraTributariaUFBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    produto_id: uuid.UUID
