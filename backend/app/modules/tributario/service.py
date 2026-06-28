from app.models.produto import Produto, RegraTributariaUF
from app.modules.tributario.aliquotas_uf import aliquota_interestadual, aliquota_interna
from app.modules.tributario.ncm_cest_base import sugerir_cest


def sugerir_classificacao_fiscal(produto: Produto) -> dict:
    """Sugere CEST e aponta lacunas de classificação fiscal com base no NCM cadastrado."""
    sugestoes: dict[str, str] = {}

    if produto.ncm and not produto.cest:
        cest_sugerido = sugerir_cest(produto.ncm)
        if cest_sugerido:
            sugestoes["cest"] = cest_sugerido

    if not produto.cst_icms:
        sugestoes.setdefault("cst_icms", "00")
    if not produto.cst_pis:
        sugestoes.setdefault("cst_pis", "01")
    if not produto.cst_cofins:
        sugestoes.setdefault("cst_cofins", "01")

    return sugestoes


def sugerir_regra_uf(uf_origem: str, uf_destino: str, importado: bool = False) -> dict:
    """Sugere a alíquota de ICMS e a necessidade de DIFAL para um par de UFs,
    com base na Resolução do Senado nº 13/2012 e nas alíquotas internas vigentes.
    """
    interna_destino = aliquota_interna(uf_destino)

    if uf_origem.upper() == uf_destino.upper():
        return {
            "aliquota_icms": interna_destino,
            "aplica_difal": False,
            "observacao": "Operação interna — não há DIFAL.",
        }

    interestadual = aliquota_interestadual(uf_origem, uf_destino, importado=importado)
    aplica_difal = interestadual is not None and interna_destino is not None and interna_destino > interestadual

    return {
        "aliquota_icms": interestadual,
        "aliquota_interna_destino": interna_destino,
        "aplica_difal": aplica_difal,
        "diferencial_aliquota": round(interna_destino - interestadual, 4) if aplica_difal else 0.0,
    }


def calcular_tributacao_destino(regra: RegraTributariaUF, valor_operacao: float) -> dict:
    """Aplica a regra tributária de uma UF de destino sobre o valor da operação."""
    resultado = {
        "valor_icms": 0.0,
        "valor_icms_st": 0.0,
        "valor_difal": 0.0,
    }

    if regra.aliquota_icms:
        resultado["valor_icms"] = round(valor_operacao * float(regra.aliquota_icms), 2)

    if regra.aplica_st and regra.aliquota_icms_st and regra.mva_st:
        base_st = valor_operacao * (1 + float(regra.mva_st))
        resultado["valor_icms_st"] = round(base_st * float(regra.aliquota_icms_st), 2)

    if regra.aplica_difal and regra.aliquota_icms:
        interna_destino = aliquota_interna(regra.uf_destino)
        if interna_destino and interna_destino > float(regra.aliquota_icms):
            diferencial = interna_destino - float(regra.aliquota_icms)
            resultado["valor_difal"] = round(valor_operacao * diferencial, 2)

    return resultado
