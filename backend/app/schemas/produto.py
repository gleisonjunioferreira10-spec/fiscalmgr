import uuid

from pydantic import BaseModel, ConfigDict


class ProdutoBase(BaseModel):
    sku: str
    descricao: str
    ncm: str | None = None
    cest: str | None = None
    cst_icms: str | None = None
    cst_pis: str | None = None
    cst_cofins: str | None = None
    cfop_padrao: str | None = None
    preco_custo: float | None = None
    preco_venda: float | None = None


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    descricao: str | None = None
    ncm: str | None = None
    cest: str | None = None
    cst_icms: str | None = None
    cst_pis: str | None = None
    cst_cofins: str | None = None
    cfop_padrao: str | None = None
    preco_custo: float | None = None
    preco_venda: float | None = None


class ProdutoOut(ProdutoBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    empresa_id: uuid.UUID
    cadastro_completo: bool
