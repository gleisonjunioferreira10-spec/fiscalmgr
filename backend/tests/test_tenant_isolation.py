from tests.conftest import registrar_empresa


def test_empresa_nao_acessa_produto_de_outra_empresa(client):
    headers_a = registrar_empresa(client, "Empresa A", "11111111000111", "admin-a@empresa.com")
    headers_b = registrar_empresa(client, "Empresa B", "22222222000122", "admin-b@empresa.com")

    resposta = client.post(
        "/api/v1/produtos",
        json={"sku": "SKU-1", "descricao": "Produto da empresa A"},
        headers=headers_a,
    )
    assert resposta.status_code == 201
    produto_id = resposta.json()["id"]

    resposta = client.get(f"/api/v1/produtos/{produto_id}", headers=headers_b)
    assert resposta.status_code == 404

    resposta = client.patch(
        f"/api/v1/produtos/{produto_id}",
        json={"descricao": "Tentativa de alteração indevida"},
        headers=headers_b,
    )
    assert resposta.status_code == 404

    resposta = client.get(f"/api/v1/produtos/{produto_id}/sugestao-fiscal", headers=headers_b)
    assert resposta.status_code == 404


def test_listagem_de_produtos_e_isolada_por_empresa(client):
    headers_a = registrar_empresa(client, "Empresa A", "11111111000111", "admin-a@empresa.com")
    headers_b = registrar_empresa(client, "Empresa B", "22222222000122", "admin-b@empresa.com")

    client.post("/api/v1/produtos", json={"sku": "SKU-A", "descricao": "Produto A"}, headers=headers_a)
    client.post("/api/v1/produtos", json={"sku": "SKU-B", "descricao": "Produto B"}, headers=headers_b)

    produtos_a = client.get("/api/v1/produtos", headers=headers_a).json()
    produtos_b = client.get("/api/v1/produtos", headers=headers_b).json()

    assert [p["sku"] for p in produtos_a] == ["SKU-A"]
    assert [p["sku"] for p in produtos_b] == ["SKU-B"]


def test_empresa_nao_acessa_regra_uf_de_produto_de_outra_empresa(client):
    headers_a = registrar_empresa(client, "Empresa A", "11111111000111", "admin-a@empresa.com")
    headers_b = registrar_empresa(client, "Empresa B", "22222222000122", "admin-b@empresa.com")

    produto_a = client.post(
        "/api/v1/produtos", json={"sku": "SKU-1", "descricao": "Produto A"}, headers=headers_a
    ).json()

    resposta = client.post(
        "/api/v1/regras-uf",
        json={"produto_id": produto_a["id"], "uf_origem": "SP", "uf_destino": "RJ", "aliquota_icms": 0.12},
        headers=headers_b,
    )
    assert resposta.status_code == 404

    resposta = client.get("/api/v1/regras-uf", params={"produto_id": produto_a["id"]}, headers=headers_b)
    assert resposta.status_code == 404


def test_empresa_nao_valida_venda_de_produto_de_outra_empresa(client):
    headers_a = registrar_empresa(client, "Empresa A", "11111111000111", "admin-a@empresa.com")
    headers_b = registrar_empresa(client, "Empresa B", "22222222000122", "admin-b@empresa.com")

    produto_a = client.post(
        "/api/v1/produtos", json={"sku": "SKU-1", "descricao": "Produto A"}, headers=headers_a
    ).json()

    resposta = client.post(
        "/api/v1/validador/validar-venda",
        json={"produto_id": produto_a["id"], "uf_destino": "RJ", "preco_venda": 100.0},
        headers=headers_b,
    )
    assert resposta.status_code == 404


def test_dashboard_de_auditoria_e_isolado_por_empresa(client):
    headers_a = registrar_empresa(client, "Empresa A", "11111111000111", "admin-a@empresa.com")
    headers_b = registrar_empresa(client, "Empresa B", "22222222000122", "admin-b@empresa.com")

    client.post("/api/v1/produtos", json={"sku": "SKU-A1", "descricao": "Produto A1"}, headers=headers_a)
    client.post("/api/v1/produtos", json={"sku": "SKU-A2", "descricao": "Produto A2"}, headers=headers_a)
    client.post("/api/v1/produtos", json={"sku": "SKU-B1", "descricao": "Produto B1"}, headers=headers_b)

    auditoria_a = client.get("/api/v1/dashboard/auditoria", headers=headers_a).json()
    auditoria_b = client.get("/api/v1/dashboard/auditoria", headers=headers_b).json()

    assert auditoria_a["total_produtos"] == 2
    assert auditoria_b["total_produtos"] == 1


def test_acesso_sem_token_e_negado(client):
    resposta = client.get("/api/v1/produtos")
    assert resposta.status_code == 401
