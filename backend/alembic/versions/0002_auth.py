"""empresas e usuarios (multi-tenant auth)

Revision ID: 0002
Revises: 0001
Create Date: 2026-06-29

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "empresas",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("nome", sa.String(255), nullable=False),
        sa.Column("cnpj", sa.String(14), nullable=False, unique=True),
    )

    op.create_table(
        "usuarios",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("empresa_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("empresas.id"), nullable=False),
        sa.Column("nome", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("senha_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(32), server_default="admin", nullable=False),
        sa.Column("ativo", sa.Boolean, server_default=sa.true(), nullable=False),
    )
    op.create_index("ix_usuarios_empresa_id", "usuarios", ["empresa_id"])
    op.create_index("ix_usuarios_email", "usuarios", ["email"])

    op.create_foreign_key(
        "fk_produtos_empresa_id", "produtos", "empresas", ["empresa_id"], ["id"]
    )


def downgrade() -> None:
    op.drop_constraint("fk_produtos_empresa_id", "produtos", type_="foreignkey")
    op.drop_table("usuarios")
    op.drop_table("empresas")
