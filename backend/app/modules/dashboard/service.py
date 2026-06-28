import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.models.validacao import ValidacaoFiscal


def resumo_auditoria(db: Session, empresa_id: uuid.UUID) -> dict:
    """Consolida indicadores fiscais para o dashboard de auditoria preventiva."""
    total_produtos = db.scalar(
        select(func.count()).select_from(Produto).where(Produto.empresa_id == empresa_id)
    ) or 0

    produtos_incompletos = db.scalar(
        select(func.count())
        .select_from(Produto)
        .where(Produto.empresa_id == empresa_id, Produto.cadastro_completo.is_(False))
    ) or 0

    alertas_por_status = db.execute(
        select(ValidacaoFiscal.status, func.count())
        .join(Produto, Produto.id == ValidacaoFiscal.produto_id)
        .where(Produto.empresa_id == empresa_id)
        .group_by(ValidacaoFiscal.status)
    ).all()

    return {
        "total_produtos": total_produtos,
        "produtos_cadastro_incompleto": produtos_incompletos,
        "validacoes_por_status": {status: total for status, total in alertas_por_status},
    }
