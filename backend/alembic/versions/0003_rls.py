"""Row-Level Security por empresa_id (defesa em profundidade multi-tenant)

Revision ID: 0003
Revises: 0002
Create Date: 2026-06-28

"""
from typing import Sequence, Union

from alembic import op

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE produtos ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE produtos FORCE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY tenant_isolation_produtos ON produtos
        USING (empresa_id = current_setting('app.current_empresa_id', true)::uuid)
        WITH CHECK (empresa_id = current_setting('app.current_empresa_id', true)::uuid)
        """
    )

    op.execute("ALTER TABLE regras_tributarias_uf ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE regras_tributarias_uf FORCE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY tenant_isolation_regras_uf ON regras_tributarias_uf
        USING (produto_id IN (
            SELECT id FROM produtos
            WHERE empresa_id = current_setting('app.current_empresa_id', true)::uuid
        ))
        WITH CHECK (produto_id IN (
            SELECT id FROM produtos
            WHERE empresa_id = current_setting('app.current_empresa_id', true)::uuid
        ))
        """
    )

    op.execute("ALTER TABLE validacoes_fiscais ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE validacoes_fiscais FORCE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY tenant_isolation_validacoes ON validacoes_fiscais
        USING (produto_id IN (
            SELECT id FROM produtos
            WHERE empresa_id = current_setting('app.current_empresa_id', true)::uuid
        ))
        WITH CHECK (produto_id IN (
            SELECT id FROM produtos
            WHERE empresa_id = current_setting('app.current_empresa_id', true)::uuid
        ))
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY tenant_isolation_validacoes ON validacoes_fiscais")
    op.execute("ALTER TABLE validacoes_fiscais NO FORCE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE validacoes_fiscais DISABLE ROW LEVEL SECURITY")

    op.execute("DROP POLICY tenant_isolation_regras_uf ON regras_tributarias_uf")
    op.execute("ALTER TABLE regras_tributarias_uf NO FORCE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE regras_tributarias_uf DISABLE ROW LEVEL SECURITY")

    op.execute("DROP POLICY tenant_isolation_produtos ON produtos")
    op.execute("ALTER TABLE produtos NO FORCE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE produtos DISABLE ROW LEVEL SECURITY")
