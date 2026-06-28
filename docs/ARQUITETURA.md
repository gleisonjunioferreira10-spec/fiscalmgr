# Arquitetura Técnica — Gerente Fiscal

## Visão geral

SaaS multi-tenant (isolamento lógico por `empresa_id`) API-first, pensado para integração
com ERPs de atacado/distribuição e para escalar a milhões de SKUs.

```
┌─────────────┐      HTTPS/JSON       ┌──────────────────┐
│  Frontend   │ ────────────────────▶ │  FastAPI (API)   │
│  React/Vite │ ◀──────────────────── │  /api/v1/*        │
└─────────────┘                       └─────────┬────────┘
                                                  │ SQLAlchemy
                                                  ▼
                                       ┌──────────────────┐
                                       │   PostgreSQL      │
                                       └──────────────────┘

ERPs externos ──▶ mesma API (/api/v1/*) ──▶ mesmos módulos de negócio
```

## Camadas do backend

- `app/api/v1`: routers HTTP, validação de entrada/saída via Pydantic. Sem regra de negócio.
- `app/modules/*`: regra de negócio por domínio (tributário, validador, dashboard). Recebem
  sessão de banco e entidades, retornam dados — sem dependência do FastAPI.
- `app/models`: entidades SQLAlchemy (fonte da verdade do schema).
- `app/schemas`: contratos de API (separados das entidades de banco, permitindo evoluir
  independentemente).
- `app/db`: engine/sessão e `Base` declarativa.
- `app/core`: configuração via variáveis de ambiente (`pydantic-settings`).

Essa separação (API / módulos de negócio / persistência) permite expor os mesmos módulos
por outros canais no futuro (ex.: worker assíncrono, job de IA) sem duplicar regra de negócio.

## Multi-tenant

Toda entidade de domínio carrega `empresa_id`. Os endpoints de listagem e o dashboard
exigem esse parâmetro. Para v2, considerar:
- Row-Level Security no Postgres por `empresa_id`.
- Autenticação/autorização (JWT) anexando `empresa_id` ao contexto da requisição.

## Módulos de negócio (MVP)

| Módulo | Responsabilidade | Local |
|---|---|---|
| Cadastro de produtos | CRUD de produto e cálculo de `cadastro_completo` | `api/v1/produtos.py` |
| Motor tributário | Sugestão de CEST/CST e cálculo de ICMS/ICMS-ST/DIFAL | `modules/tributario` |
| Validador fiscal | Bloqueia/alerta venda antes do faturamento | `modules/validador` |
| Regras fiscais por UF | CRUD de alíquotas/MVA/flags por UF de destino | `models/produto.py::RegraTributariaUF`, `api/v1/regras_uf.py` |
| Dashboard de auditoria | Indicadores agregados de inconsistências | `modules/dashboard` |

## Modelo de dados (essencial)

- `produtos`: dados fiscais do produto (NCM, CEST, CSTs, CFOP) + flag `cadastro_completo`.
- `regras_tributarias_uf`: regra tributária de um produto por par origem/destino de UF
  (alíquota ICMS, ICMS-ST, MVA-ST, flags de ST/DIFAL/antecipação).
- `validacoes_fiscais`: histórico de execuções do validador fiscal (status `ok` | `alerta`
  | `bloqueado`), usado tanto para auditoria preventiva quanto para o dashboard.

## Preparação para escala e IA futura

- Índices em `empresa_id`, `sku`, `ncm`, `cest` para consultas em catálogos grandes.
- UUID como chave primária (evita colisão em cenários de importação/replicação multi-tenant).
- Base de NCM↔CEST isolada em `modules/tributario/ncm_cest_base.py`, propositalmente
  desacoplada da lógica de sugestão — facilita troca futura por um serviço de IA/ML sem
  alterar a API pública.
- Camada de módulos de negócio sem dependência do framework HTTP, podendo ser reaproveitada
  por jobs assíncronos (ex.: reclassificação fiscal em lote via IA).

## Roadmap de evolução

1. Autenticação multi-tenant (JWT) e RBAC.
2. Importação em lote de produtos (CSV/integração ERP).
3. Motor tributário com base oficial de NCM/CEST/ST por UF.
4. Fila assíncrona (ex.: Celery/RQ) para revalidação fiscal em massa.
5. Camada de sugestão fiscal assistida por IA sobre o motor tributário atual.
