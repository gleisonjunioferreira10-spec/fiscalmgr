import csv
import io
import uuid

from sqlalchemy.orm import Session

from app.models.produto import Produto

COLUNAS_OBRIGATORIAS = {"sku", "descricao"}
CAMPOS_TEXTO = ("ncm", "cest", "cst_icms", "cst_pis", "cst_cofins", "cfop_padrao")
CAMPOS_OBRIGATORIOS_FISCAL = ("ncm", "cst_icms", "cst_pis", "cst_cofins", "cfop_padrao")


class ImportacaoInvalidaError(Exception):
    pass


def _parse_decimal(valor: str | None) -> float | None:
    if not valor or not valor.strip():
        return None
    return float(valor.replace(",", "."))


def _atualizar_status_cadastro(produto: Produto) -> None:
    produto.cadastro_completo = all(getattr(produto, campo) for campo in CAMPOS_OBRIGATORIOS_FISCAL)


def importar_produtos_csv(db: Session, empresa_id: uuid.UUID, conteudo: bytes) -> dict:
    """Importa/atualiza produtos em lote a partir de um CSV (upsert por SKU dentro da empresa)."""
    texto = conteudo.decode("utf-8-sig")
    leitor = csv.DictReader(io.StringIO(texto))

    if leitor.fieldnames is None or not COLUNAS_OBRIGATORIAS.issubset(set(leitor.fieldnames)):
        raise ImportacaoInvalidaError("CSV precisa conter ao menos as colunas: sku, descricao")

    criados = 0
    atualizados = 0
    erros: list[dict] = []

    for numero_linha, linha in enumerate(leitor, start=2):
        sku = (linha.get("sku") or "").strip()
        descricao = (linha.get("descricao") or "").strip()

        if not sku or not descricao:
            erros.append({"linha": numero_linha, "mensagem": "sku e descricao são obrigatórios"})
            continue

        try:
            preco_custo = _parse_decimal(linha.get("preco_custo"))
            preco_venda = _parse_decimal(linha.get("preco_venda"))
        except ValueError:
            erros.append({"linha": numero_linha, "mensagem": "preco_custo/preco_venda inválido"})
            continue

        produto = (
            db.query(Produto)
            .filter(Produto.empresa_id == empresa_id, Produto.sku == sku)
            .first()
        )
        if produto is None:
            produto = Produto(empresa_id=empresa_id, sku=sku, descricao=descricao)
            db.add(produto)
            criados += 1
        else:
            produto.descricao = descricao
            atualizados += 1

        for campo in CAMPOS_TEXTO:
            valor = (linha.get(campo) or "").strip()
            if valor:
                setattr(produto, campo, valor)

        produto.preco_custo = preco_custo if preco_custo is not None else produto.preco_custo
        produto.preco_venda = preco_venda if preco_venda is not None else produto.preco_venda

        _atualizar_status_cadastro(produto)

    db.commit()

    return {"criados": criados, "atualizados": atualizados, "erros": erros}
