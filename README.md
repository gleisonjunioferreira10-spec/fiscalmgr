# Gerente Fiscal

SaaS de inteligência e gestão fiscal para empresas de atacado, distribuição e varejo.
Previne erros tributários, automatiza validações fiscais e facilita o cadastro de produtos.

Nascido de uma necessidade real da MGR Atacado em lidar com operações fiscais complexas no atacado/distribuição.

## Módulos do MVP

1. **Cadastro de produtos** — SKU, NCM, CEST, CST ICMS/PIS/COFINS, CFOP.
2. **Motor tributário** — sugestão de classificação fiscal e cálculo de tributação por UF de destino (ICMS, ICMS-ST, DIFAL).
3. **Validador fiscal** — bloqueia/alerta vendas com cadastro incompleto, preço abaixo do custo ou regra de UF ausente.
4. **Regras fiscais por UF** — alíquotas de ICMS, MVA-ST, flags de ST/DIFAL/antecipação por produto e UF.
5. **Dashboard de auditoria fiscal** — indicadores de cadastro incompleto e validações por status.

Veja [docs/ARQUITETURA.md](docs/ARQUITETURA.md) para o desenho técnico completo.

## Stack

- Backend: Python + FastAPI + SQLAlchemy + Alembic
- Frontend: React + TypeScript + Vite
- Banco: PostgreSQL
- Infra: Docker / docker-compose

## Rodando localmente

```bash
docker-compose up --build
```

- API: http://localhost:8000 (docs em `/docs`)
- Frontend: http://localhost:5173

Para aplicar as migrations:

```bash
docker-compose exec backend alembic upgrade head
```

Antes de subir, copie `backend/.env.example` para `backend/.env` e gere uma `JWT_SECRET_KEY`
única (`python3 -c "import secrets; print(secrets.token_hex(32))"`) — a aplicação não inicia
sem esse valor configurado.

## Testes

```bash
cd backend
pip install -r requirements.txt
pytest
```

A suíte inclui testes de isolamento multi-tenant (`tests/test_tenant_isolation.py`), que
garantem que uma empresa nunca acessa dados de outra em nenhum endpoint.

## Estrutura

```
backend/
  app/
    api/v1/        # routers HTTP
    core/           # configuração
    db/             # sessão e base do SQLAlchemy
    models/         # entidades ORM
    schemas/        # contratos Pydantic
    modules/         # regras de negócio por módulo (tributário, validador, dashboard)
  alembic/          # migrations
frontend/
  src/
    pages/          # telas (Dashboard, Produtos)
    services/       # cliente HTTP
docs/
  ARQUITETURA.md    # arquitetura técnica do SaaS
```
