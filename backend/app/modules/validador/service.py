from sqlalchemy.orm import Session

from app.models.produto import Produto, RegraTributariaUF
from app.models.validacao import ValidacaoFiscal


class ValidacaoBloqueadaError(Exception):
    def __init__(self, ocorrencias: list[dict]):
        self.ocorrencias = ocorrencias
        super().__init__("Venda bloqueada por inconsistência fiscal")


def _checar_cadastro(produto: Produto) -> list[dict]:
    ocorrencias = []
    campos_obrigatorios = {
        "ncm": "NCM não cadastrado",
        "cst_icms": "CST ICMS não cadastrado",
        "cst_pis": "CST PIS não cadastrado",
        "cst_cofins": "CST COFINS não cadastrado",
        "cfop_padrao": "CFOP padrão não cadastrado",
    }
    for campo, mensagem in campos_obrigatorios.items():
        if not getattr(produto, campo):
            ocorrencias.append({"status": "bloqueado", "codigo": f"CADASTRO_{campo.upper()}", "mensagem": mensagem})
    return ocorrencias


def _checar_preco(produto: Produto, preco_venda: float) -> list[dict]:
    ocorrencias = []
    if produto.preco_custo and preco_venda < float(produto.preco_custo):
        ocorrencias.append({
            "status": "bloqueado",
            "codigo": "PRECO_ABAIXO_CUSTO",
            "mensagem": "Preço de venda abaixo do custo cadastrado",
        })
    return ocorrencias


def _checar_regra_uf(regra: RegraTributariaUF | None, uf_destino: str) -> list[dict]:
    if regra is None:
        return [{
            "status": "alerta",
            "codigo": "REGRA_UF_AUSENTE",
            "mensagem": f"Nenhuma regra tributária cadastrada para UF de destino {uf_destino}",
        }]
    return []


def validar_venda(
    db: Session,
    produto: Produto,
    uf_destino: str,
    preco_venda: float,
) -> list[ValidacaoFiscal]:
    """Executa as regras de validação fiscal antes de autorizar uma venda."""
    regra = next((r for r in produto.regras_uf if r.uf_destino == uf_destino), None)

    ocorrencias = (
        _checar_cadastro(produto)
        + _checar_preco(produto, preco_venda)
        + _checar_regra_uf(regra, uf_destino)
    )

    if not ocorrencias:
        ocorrencias = [{"status": "ok", "codigo": "VALIDACAO_OK", "mensagem": "Venda liberada"}]

    registros = []
    for ocorrencia in ocorrencias:
        registro = ValidacaoFiscal(produto_id=produto.id, **ocorrencia)
        db.add(registro)
        registros.append(registro)
    db.commit()

    if any(o["status"] == "bloqueado" for o in ocorrencias):
        raise ValidacaoBloqueadaError(ocorrencias)

    return registros
