"""Base de referência NCM/CEST. Placeholder para integração futura com tabela oficial (Convênio 142/2018)."""

NCM_CEST_MAP: dict[str, dict[str, str]] = {
    "22030000": {"cest": "03.002.00", "descricao": "Cervejas e chopes"},
    "30049099": {"cest": "13.001.00", "descricao": "Medicamentos"},
    "33051000": {"cest": "20.001.00", "descricao": "Shampoos"},
}


def sugerir_cest(ncm: str) -> str | None:
    item = NCM_CEST_MAP.get(ncm)
    return item["cest"] if item else None
