"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-06-28

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "produtos",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("empresa_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sku", sa.String(64), nullable=False),
        sa.Column("descricao", sa.String(255), nullable=False),
        sa.Column("ncm", sa.String(8)),
        sa.Column("cest", sa.String(7)),
        sa.Column("cst_icms", sa.String(3)),
        sa.Column("cst_pis", sa.String(2)),
        sa.Column("cst_cofins", sa.String(2)),
        sa.Column("cfop_padrao", sa.String(4)),
        sa.Column("preco_custo", sa.Numeric(14, 4)),
        sa.Column("preco_venda", sa.Numeric(14, 4)),
        sa.Column("cadastro_completo", sa.Boolean, server_default=sa.false(), nullable=False),
    )
    op.create_index("ix_produtos_empresa_id", "produtos", ["empresa_id"])
    op.create_index("ix_produtos_sku", "produtos", ["sku"])
    op.create_index("ix_produtos_ncm", "produtos", ["ncm"])
    op.create_index("ix_produtos_cest", "produtos", ["cest"])

    op.create_table(
        "regras_tributarias_uf",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("produto_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("produtos.id"), nullable=False),
        sa.Column("uf_origem", sa.String(2), nullable=False),
        sa.Column("uf_destino", sa.String(2), nullable=False),
        sa.Column("aliquota_icms", sa.Numeric(6, 4)),
        sa.Column("aliquota_icms_st", sa.Numeric(6, 4)),
        sa.Column("mva_st", sa.Numeric(6, 4)),
        sa.Column("aplica_st", sa.Boolean, server_default=sa.false(), nullable=False),
        sa.Column("aplica_difal", sa.Boolean, server_default=sa.false(), nullable=False),
        sa.Column("aplica_antecipacao", sa.Boolean, server_default=sa.false(), nullable=False),
    )
    op.create_index("ix_regras_tributarias_uf_produto_id", "regras_tributarias_uf", ["produto_id"])

    op.create_table(
        "validacoes_fiscais",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("produto_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("produtos.id"), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("codigo", sa.String(64), nullable=False),
        sa.Column("mensagem", sa.String(255), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_validacoes_fiscais_produto_id", "validacoes_fiscais", ["produto_id"])


def downgrade() -> None:
    op.drop_table("validacoes_fiscais")
    op.drop_table("regras_tributarias_uf")
    op.drop_table("produtos")
