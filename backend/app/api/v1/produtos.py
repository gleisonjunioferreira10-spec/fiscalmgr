import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.produto import Produto
from app.modules.tributario.service import sugerir_classificacao_fiscal
from app.schemas.produto import ProdutoCreate, ProdutoOut, ProdutoUpdate

router = APIRouter(prefix="/produtos", tags=["produtos"])

CAMPOS_OBRIGATORIOS = ("ncm", "cst_icms", "cst_pis", "cst_cofins", "cfop_padrao")


def _atualizar_status_cadastro(produto: Produto) -> None:
    produto.cadastro_completo = all(getattr(produto, campo) for campo in CAMPOS_OBRIGATORIOS)


@router.post("", response_model=ProdutoOut, status_code=201)
def criar_produto(payload: ProdutoCreate, db: Session = Depends(get_db)):
    produto = Produto(**payload.model_dump())
    _atualizar_status_cadastro(produto)
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


@router.get("", response_model=list[ProdutoOut])
def listar_produtos(empresa_id: uuid.UUID, db: Session = Depends(get_db)):
    return db.query(Produto).filter(Produto.empresa_id == empresa_id).all()


@router.get("/{produto_id}", response_model=ProdutoOut)
def obter_produto(produto_id: uuid.UUID, db: Session = Depends(get_db)):
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@router.patch("/{produto_id}", response_model=ProdutoOut)
def atualizar_produto(produto_id: uuid.UUID, payload: ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(produto, campo, valor)

    _atualizar_status_cadastro(produto)
    db.commit()
    db.refresh(produto)
    return produto


@router.get("/{produto_id}/sugestao-fiscal")
def sugestao_fiscal(produto_id: uuid.UUID, db: Session = Depends(get_db)):
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return sugerir_classificacao_fiscal(produto)
