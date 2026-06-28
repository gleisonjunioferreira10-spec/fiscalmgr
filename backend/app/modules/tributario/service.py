from app.models.produto import Produto, RegraTributariaUF
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
        resultado["valor_difal"] = round(valor_operacao * float(regra.aliquota_icms) * 0.5, 2)

    return resultado
