"""Alíquotas e classificação regional oficiais dos estados brasileiros.

Fontes:
- Alíquota interna "geral" de ICMS de cada UF (legislação estadual vigente, regra geral —
  produtos específicos podem ter alíquota diferenciada e não estão cobertos aqui).
- Classificação regional para a regra interestadual da Resolução do Senado nº 13/2012
  e do Convênio ICMS 153/2015 (4%/7%/12%), implementada em `aliquota_interestadual`.
"""

REGIAO_SUL_SUDESTE = {"SP", "RJ", "MG", "PR", "SC", "RS"}
ESTADOS = {
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
    "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
}

ALIQUOTA_INTERNA_GERAL: dict[str, float] = {
    "AC": 0.19, "AL": 0.19, "AP": 0.18, "AM": 0.20, "BA": 0.205, "CE": 0.20,
    "DF": 0.20, "ES": 0.17, "GO": 0.19, "MA": 0.22, "MT": 0.17, "MS": 0.17,
    "MG": 0.18, "PA": 0.19, "PB": 0.20, "PR": 0.195, "PE": 0.205, "PI": 0.21,
    "RJ": 0.22, "RN": 0.18, "RS": 0.17, "RO": 0.195, "RR": 0.20, "SC": 0.17,
    "SP": 0.18, "SE": 0.19, "TO": 0.20,
}


def aliquota_interna(uf: str) -> float | None:
    return ALIQUOTA_INTERNA_GERAL.get(uf.upper())


def aliquota_interestadual(uf_origem: str, uf_destino: str, importado: bool = False) -> float | None:
    """Alíquota de ICMS para operação interestadual, conforme Resolução do Senado nº 13/2012.

    - 4% para bens e mercadorias importados do exterior (ou com conteúdo de importação > 40%).
    - 7% quando a origem é Sul/Sudeste (exceto ES) e o destino é Norte, Nordeste, Centro-Oeste ou ES.
    - 12% nos demais casos interestaduais.
    - Operação dentro da mesma UF não é interestadual: retorna None (usar `aliquota_interna`).
    """
    origem = uf_origem.upper()
    destino = uf_destino.upper()

    if origem not in ESTADOS or destino not in ESTADOS:
        return None
    if origem == destino:
        return None
    if importado:
        return 0.04
    if origem in REGIAO_SUL_SUDESTE and origem != "ES" and destino not in REGIAO_SUL_SUDESTE:
        return 0.07
    if origem in REGIAO_SUL_SUDESTE and origem != "ES" and destino == "ES":
        return 0.07
    return 0.12
