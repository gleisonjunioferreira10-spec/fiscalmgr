"""Base de referência NCM/CEST.

ATENÇÃO: este é um conjunto reduzido de exemplos para fins de demonstração do motor de
sugestão fiscal — não é uma cópia integral do anexo do Convênio ICMS 142/2018. A tabela
oficial tem milhares de NCMs segmentados por UF e muda por convênio/protocolo. Antes de
usar em produção, substitua `NCM_CEST_MAP` pela tabela oficial vigente (ex.: carregada de
um CSV publicado pela SEFAZ/CONFAZ), mantendo a mesma assinatura de `sugerir_cest`.
"""

NCM_CEST_MAP: dict[str, dict[str, str]] = {
    "22030000": {"cest": "03.002.00", "descricao": "Cervejas e chopes"},
    "22021000": {"cest": "03.001.00", "descricao": "Águas, inclusive minerais, e refrigerantes"},
    "22029900": {"cest": "03.003.00", "descricao": "Bebidas energéticas e isotônicas"},
    "24022000": {"cest": "07.002.00", "descricao": "Cigarros contendo tabaco"},
    "30049099": {"cest": "13.001.00", "descricao": "Medicamentos"},
    "33051000": {"cest": "20.001.00", "descricao": "Shampoos"},
    "34022000": {"cest": "20.038.00", "descricao": "Detergentes e produtos de limpeza"},
    "40111000": {"cest": "01.001.00", "descricao": "Pneus novos de borracha para automóveis"},
    "85061000": {"cest": "12.001.00", "descricao": "Pilhas e baterias elétricas"},
}


def sugerir_cest(ncm: str) -> str | None:
    item = NCM_CEST_MAP.get(ncm)
    return item["cest"] if item else None
