# Entradas do Pipeline

Esta pasta contém os scripts executáveis que orquestram a geração,
classificação, proteção, validação e construção das camadas analíticas.
Execute os módulos a partir da raiz do projeto.

## Scripts

| Módulo | Responsabilidade | Comando |
| --- | --- | --- |
| `generate_data.py` | Gera o dataset sintético na Raw. | `python -m src.generate_data` |
| `classify_data.py` | Valida a política de classificação contra a Raw. | `python -m src.classify_data` |
| `protect_data.py` | Aplica remoção, generalização e pseudonimização; salva Protected e o mapa restrito. | `python -m src.protect_data` |
| `validate_protection.py` | Compara Raw e Protected e executa validações Great Expectations. | `python -m src.validate_protection` |
| `build_silver.py` | Constrói a Silver a partir da Protected. | `python -m src.build_silver` |
| `build_analytics.py` | Gera produtos agregados a partir da Silver. | `python -m src.build_analytics` |

## Ordem recomendada

```text
generate_data
	↓
classify_data
	↓
protect_data ──> data/restricted/customer_identity_map.parquet
	↓
validate_protection
	↓
build_silver
	↓
build_analytics
```

Os comandos dependem da configuração do ambiente, especialmente de
`PSEUDONYMIZATION_KEY` para o processo de proteção e validação.
