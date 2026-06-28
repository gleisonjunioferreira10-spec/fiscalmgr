import uuid

from sqlalchemy import String, Numeric, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)

    sku: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)

    ncm: Mapped[str | None] = mapped_column(String(8), index=True)
    cest: Mapped[str | None] = mapped_column(String(7), index=True)
    cst_icms: Mapped[str | None] = mapped_column(String(3))
    cst_pis: Mapped[str | None] = mapped_column(String(2))
    cst_cofins: Mapped[str | None] = mapped_column(String(2))
    cfop_padrao: Mapped[str | None] = mapped_column(String(4))

    preco_custo: Mapped[float | None] = mapped_column(Numeric(14, 4))
    preco_venda: Mapped[float | None] = mapped_column(Numeric(14, 4))

    cadastro_completo: Mapped[bool] = mapped_column(Boolean, default=False)

    regras_uf: Mapped[list["RegraTributariaUF"]] = relationship(back_populates="produto")


class RegraTributariaUF(Base):
    __tablename__ = "regras_tributarias_uf"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    produto_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("produtos.id"), nullable=False, index=True)

    uf_origem: Mapped[str] = mapped_column(String(2), nullable=False)
    uf_destino: Mapped[str] = mapped_column(String(2), nullable=False)

    aliquota_icms: Mapped[float | None] = mapped_column(Numeric(6, 4))
    aliquota_icms_st: Mapped[float | None] = mapped_column(Numeric(6, 4))
    mva_st: Mapped[float | None] = mapped_column(Numeric(6, 4))
    aplica_st: Mapped[bool] = mapped_column(Boolean, default=False)
    aplica_difal: Mapped[bool] = mapped_column(Boolean, default=False)
    aplica_antecipacao: Mapped[bool] = mapped_column(Boolean, default=False)

    produto: Mapped["Produto"] = relationship(back_populates="regras_uf")
