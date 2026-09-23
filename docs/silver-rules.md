
# Regras de Preparação da Camada Silver

## 1. Objetivo

Este documento descreve as regras implementadas na camada Silver do case de LGPD e Segurança aplicada à Engenharia de Dados.

A Silver é responsável por preparar os dados protegidos para a finalidade analítica definida, realizando seleção de atributos, padronização de tipos, validação de consistência e criação de métricas derivadas.

O processamento não acessa diretamente a Raw e não reaplica as transformações de proteção.

---

## 2. Entrada e Saída

### Entrada

`data/protected/customers.parquet`

A entrada contém 10.000 registros e 18 colunas.

### Saída

`data/silver/customers.parquet`

A saída contém 10.000 registros e 13 colunas.

### Script de execução

`src/build_silver.py`

### Módulos

| Módulo | Responsabilidade |
|---|---|
| `utils/silver/definitions.py` | Definir as colunas de entrada, datas e esquema de saída. |
| `utils/silver/validator.py` | Validar o esquema e as regras de consistência. |
| `utils/silver/processor.py` | Padronizar datas, derivar métricas e construir a Silver. |

---

## 3. Contrato de Dados

A Silver mantém 11 atributos provenientes da Protected e acrescenta um atributo derivado.

| Campo | Tipo esperado | Regra |
|---|---|---|
| `customer_id` | String | Preservar o identificador pseudonimizado. |
| `condicao_saude` | String | Preservar para o recorte controlado da Analytics. |
| `faixa_etaria` | String | Preservar. |
| `estado` | String | Preservar. |
| `faixa_renda` | String | Preservar. |
| `consentimento_marketing` | Boolean | Preservar. |
| `data_consentimento` | Datetime | Converter para data. |
| `data_cadastro` | Datetime | Converter para data. |
| `ultima_compra` | Datetime | Converter para data. |
| `quantidade_compras` | Inteiro | Preservar e validar. |
| `valor_total_compras` | Float | Preservar e validar. |
| `canal_preferido` | String | Preservar. |
| `ticket_medio` | Float | Calcular a partir das métricas comerciais. |

O identificador continua pseudonimizado.

A Silver não deve ser considerada anônima.

---

## 4. Minimização de Atributos

A Silver mantém somente os atributos necessários aos produtos analíticos definidos para o case.

Os seguintes campos existentes na Protected não avançam para a Silver:

- `sexo`;
- `cidade`;
- `regiao_cep`;
- `profissao`;
- `estado_civil`;
- `possui_filhos`.

Esses atributos permanecem na Protected, mas não são necessários às agregações comerciais atualmente implementadas.

A exclusão da Silver não altera as regras de proteção originais.

---

## 5. Padronização de Datas

As seguintes colunas são convertidas utilizando `pd.to_datetime()`:

- `data_consentimento`;
- `data_cadastro`;
- `ultima_compra`.

A conversão utiliza:

```python
pd.to_datetime(
    dataframe[column],
    errors="raise",
)
```

Valores inválidos provocam uma exceção, interrompendo o processamento.

O script não substitui silenciosamente datas inválidas por valores nulos.

O tipo resultante é `datetime64[ns]`, conforme a conversão realizada pelo Pandas.

---

## 6. Validação do Esquema

Antes das transformações, o processamento verifica se todas as colunas obrigatórias estão presentes na Protected.

Caso alguma coluna esteja ausente, o processo gera um `ValueError` com a relação dos campos faltantes.

A verificação é implementada em:

`utils/silver/validator.py`

---

## 7. Regras de Consistência

O processamento verifica:

| Campo | Regra |
|---|---|
| `customer_id` | Não pode conter valores nulos. |
| `customer_id` | Não pode conter valores duplicados. |
| `quantidade_compras` | Não pode conter valores nulos. |
| `quantidade_compras` | Não pode conter valores negativos. |
| `valor_total_compras` | Não pode conter valores nulos. |
| `valor_total_compras` | Não pode conter valores negativos. |

Quando uma regra é violada, o processamento é interrompido com uma mensagem específica.

Essas verificações representam as regras implementadas nesta etapa. Não constituem uma validação completa de todas as relações temporais ou regras comerciais possíveis.

---

## 8. Cálculo do Ticket Médio

A Silver cria o atributo:

`ticket_medio`

A fórmula utilizada é:

```text
ticket_medio = valor_total_compras / quantidade_compras
```

O cálculo é aplicado somente aos clientes com quantidade de compras maior que zero.

Para clientes sem compras, o valor atribuído é `0.0`.

Essa é uma convenção do case para representar ausência de compras e evitar divisão por zero.

O cálculo é implementado em:

`utils/silver/processor.py`

### Exemplo

| Quantidade de compras | Valor total de compras | Ticket médio |
|---:|---:|---:|
| 4 | 1.000,00 | 250,00 |
| 10 | 2.500,00 | 250,00 |
| 0 | 0,00 | 0,00 |

---

## 9. Granularidade

A Silver mantém a granularidade de um registro por cliente.

A quantidade de registros não é alterada pelo processamento.

O `customer_id` pseudonimizado é preservado para permitir a identificação lógica dos registros durante as etapas internas do pipeline.

Ele não será disponibilizado nas tabelas agregadas da Analytics.

---

## 10. Execução

O processamento é executado na raiz do projeto com:

```powershell
python -m src.build_silver
```

### Resultado registrado

```text
BUILDING SILVER LAYER
[PASSED] Input rows: 10000
[PASSED] Silver rows: 10000
[PASSED] Silver columns: 12
[PASSED] Output: C:\Users\Mileno\Downloads\Projeto LGPD\data\silver\customers.parquet
SILVER LAYER SUCCESSFULLY BUILT
```

A execução registrada concluiu com sucesso.

---

## 11. Limitações

A Silver mantém dados pessoais pseudonimizados e não deve ser considerada anônima.

O projeto utiliza `float64` para valores comerciais. Essa representação é suficiente para o case, mas não oferece precisão decimal exata para cálculos financeiros de produção.

O processamento valida as regras implementadas, mas não cobre todas as possíveis inconsistências de negócio.

O controle de acesso ao armazenamento local não foi implementado especificamente pelo projeto.

---

## 12. Referências Internas

- `src/build_silver.py`
- `utils/silver/definitions.py`
- `utils/silver/validator.py`
- `utils/silver/processor.py`
- `docs/protection-rules.md`
- `docs/analytics-rules.md`
- `docs/architecture.md`