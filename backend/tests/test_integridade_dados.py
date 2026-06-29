from tests.conftest import registrar_empresa


def test_sku_duplicado_na_mesma_empresa_e_rejeitado(client):
    headers = registrar_empresa(client, "Empresa A", "11111111000111", "admin@empresa.com")

    resposta = client.post("/api/v1/produtos", json={"sku": "SKU-1", "descricao": "Produto 1"}, headers=headers)
    assert resposta.status_code == 201

    resposta = client.post("/api/v1/produtos", json={"sku": "SKU-1", "descricao": "Outro produto"}, headers=headers)
    assert resposta.status_code == 409


def test_mesmo_sku_em_empresas_diferentes_e_permitido(client):
    headers_a = registrar_empresa(client, "Empresa A", "11111111000111", "admin-a@empresa.com")
    headers_b = registrar_empresa(client, "Empresa B", "22222222000122", "admin-b@empresa.com")

    resposta_a = client.post("/api/v1/produtos", json={"sku": "SKU-1", "descricao": "Produto A"}, headers=headers_a)
    resposta_b = client.post("/api/v1/produtos", json={"sku": "SKU-1", "descricao": "Produto B"}, headers=headers_b)

    assert resposta_a.status_code == 201
    assert resposta_b.status_code == 201


def test_regra_uf_duplicada_para_mesma_uf_destino_e_rejeitada(client):
    headers = registrar_empresa(client, "Empresa A", "11111111000111", "admin@empresa.com")

    produto = client.post(
        "/api/v1/produtos", json={"sku": "SKU-1", "descricao": "Produto 1"}, headers=headers
    ).json()

    payload = {"produto_id": produto["id"], "uf_origem": "SP", "uf_destino": "RJ", "aliquota_icms": 0.12}
    resposta = client.post("/api/v1/regras-uf", json=payload, headers=headers)
    assert resposta.status_code == 201

    resposta = client.post("/api/v1/regras-uf", json=payload, headers=headers)
    assert resposta.status_code == 409
