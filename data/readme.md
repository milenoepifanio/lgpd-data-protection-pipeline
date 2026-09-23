# Dados do Pipeline

Esta pasta armazena os datasets Parquet gerados pelo pipeline de proteção
de dados. Os arquivos são derivados da execução local e não devem ser
versionados quando contiverem registros.

## Camadas

| Diretório | Camada | Conteúdo |
| --- | --- | --- |
| `raw/` | Raw Restrita | Dataset sintético original, com dados pessoais e sensíveis. |
| `restricted/` | Rastreamento restrito | Registro completo do cliente e vínculo com o ID protegido. |
| `protected/` | Protected | Dados minimizados, generalizados e pseudonimizados. |
| `silver/` | Silver | Dados protegidos selecionados e preparados para análise. |
| `analytics/` | Analytics | Produtos agregados por dimensões comerciais. |

## Artefatos principais

```text
data/
├── raw/customers.parquet
├── restricted/customer_identity_map.parquet
├── protected/customers.parquet
├── silver/customers.parquet
└── analytics/
	├── customers_by_state.parquet
	├── customers_by_age.parquet
	├── customers_by_income.parquet
	└── customers_by_channel.parquet
```

O `customer_identity_map.parquet` preserva dados pessoais completos para
rastreabilidade autorizada. Ele deve ter acesso mais restrito que as demais
camadas e não deve ser compartilhado com consumidores analíticos.

Os arquivos gerados são ignorados pelo Git; os arquivos `.gitkeep` mantêm
a estrutura dos diretórios no repositório.

## Ordem de construção

```text
Raw Restrita → Protected → Silver → Analytics
```

O mapa da área `restricted/` é produzido durante a proteção e acompanha a
relação entre `customer_id` original e `customer_id_protected`.
