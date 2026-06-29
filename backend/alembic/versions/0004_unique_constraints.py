"""Constraints únicas para integridade de dados multi-tenant

Revision ID: 0004
Revises: 0003
Create Date: 2026-06-29

"""
from typing import Sequence, Union

from alembic import op

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("uq_produtos_empresa_sku", "produtos", ["empresa_id", "sku"])
    op.create_unique_constraint(
        "uq_regras_uf_produto_destino", "regras_tributarias_uf", ["produto_id", "uf_destino"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_regras_uf_produto_destino", "regras_tributarias_uf", type_="unique")
    op.drop_constraint("uq_produtos_empresa_sku", "produtos", type_="unique")
