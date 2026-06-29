import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import get_current_empresa_id, get_db_tenant
from app.models.produto import Produto
from app.modules.produtos.importacao import ImportacaoInvalidaError, importar_produtos_csv
from app.modules.tributario.service import sugerir_classificacao_fiscal
from app.schemas.produto import ProdutoCreate, ProdutoOut, ProdutoUpdate

router = APIRouter(prefix="/produtos", tags=["produtos"])

CAMPOS_OBRIGATORIOS = ("ncm", "cst_icms", "cst_pis", "cst_cofins", "cfop_padrao")


def _atualizar_status_cadastro(produto: Produto) -> None:
    produto.cadastro_completo = all(getattr(produto, campo) for campo in CAMPOS_OBRIGATORIOS)


def _obter_produto_da_empresa(db: Session, produto_id: uuid.UUID, empresa_id: uuid.UUID) -> Produto:
    produto = db.get(Produto, produto_id)
    if not produto or produto.empresa_id != empresa_id:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@router.post("", response_model=ProdutoOut, status_code=201)
def criar_produto(
    payload: ProdutoCreate,
    db: Session = Depends(get_db_tenant),
    empresa_id: uuid.UUID = Depends(get_current_empresa_id),
):
    produto = Produto(**payload.model_dump(), empresa_id=empresa_id)
    _atualizar_status_cadastro(produto)
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


@router.get("", response_model=list[ProdutoOut])
def listar_produtos(
    db: Session = Depends(get_db_tenant),
    empresa_id: uuid.UUID = Depends(get_current_empresa_id),
):
    return db.query(Produto).filter(Produto.empresa_id == empresa_id).all()


@router.post("/importar")
async def importar_produtos(
    arquivo: UploadFile,
    db: Session = Depends(get_db_tenant),
    empresa_id: uuid.UUID = Depends(get_current_empresa_id),
):
    conteudo = await arquivo.read()
    try:
        return importar_produtos_csv(db, empresa_id, conteudo)
    except ImportacaoInvalidaError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/{produto_id}", response_model=ProdutoOut)
def obter_produto(
    produto_id: uuid.UUID,
    db: Session = Depends(get_db_tenant),
    empresa_id: uuid.UUID = Depends(get_current_empresa_id),
):
    return _obter_produto_da_empresa(db, produto_id, empresa_id)


@router.patch("/{produto_id}", response_model=ProdutoOut)
def atualizar_produto(
    produto_id: uuid.UUID,
    payload: ProdutoUpdate,
    db: Session = Depends(get_db_tenant),
    empresa_id: uuid.UUID = Depends(get_current_empresa_id),
):
    produto = _obter_produto_da_empresa(db, produto_id, empresa_id)

    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(produto, campo, valor)

    _atualizar_status_cadastro(produto)
    db.commit()
    db.refresh(produto)
    return produto


@router.get("/{produto_id}/sugestao-fiscal")
def sugestao_fiscal(
    produto_id: uuid.UUID,
    db: Session = Depends(get_db_tenant),
    empresa_id: uuid.UUID = Depends(get_current_empresa_id),
):
    produto = _obter_produto_da_empresa(db, produto_id, empresa_id)
    return sugerir_classificacao_fiscal(produto)
