import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ValidacaoFiscal(Base):
    __tablename__ = "validacoes_fiscais"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    produto_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("produtos.id"), nullable=False, index=True)

    status: Mapped[str] = mapped_column(String(16), nullable=False)  # ok | alerta | bloqueado
    codigo: Mapped[str] = mapped_column(String(64), nullable=False)
    mensagem: Mapped[str] = mapped_column(String(255), nullable=False)

    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
