# Notebooks de Consulta e Validação

Esta pasta contém notebooks exploratórios para consultar datasets do
pipeline e verificar o resultado das transformações. Eles não substituem
as validações automatizadas dos scripts.

## Notebooks

| Notebook | Finalidade |
| --- | --- |
| `query_protected_validate.ipynb` | Consulta o schema e amostras da camada Protected. |
| `trace_customer_identity.ipynb` | Relaciona o registro restrito com a Silver pelo ID protegido e valida a rastreabilidade. |
| `view_customer_identity_map.ipynb` | Consulta exclusivamente o `customer_identity_map.parquet`. |

## Execução

Abra o notebook no VS Code ou em outro ambiente Jupyter com acesso à raiz
do projeto. Os notebooks localizam a raiz a partir da pasta `utils` ou
`data` e usam caminhos relativos para os Parquets.

## Segurança

`trace_customer_identity.ipynb` e `view_customer_identity_map.ipynb` podem
exibir nome, CPF, e-mail, telefone e dados sensíveis. Execute-os somente em
ambiente autorizado e não versione outputs que contenham dados pessoais.

O notebook de rastreabilidade faz a ligação entre:

```text
customer_id_protected no mapa restrito
	↕
customer_id na camada Silver
```
