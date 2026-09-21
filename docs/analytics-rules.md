
# Regras de Construção da Camada Analytics

## 1. Objetivo

Este documento descreve as regras implementadas na camada Analytics do case de LGPD e Segurança aplicada à Engenharia de Dados.

A Analytics é responsável por disponibilizar indicadores comerciais agregados a partir da Silver, evitando a exposição desnecessária de registros individuais de clientes.

A camada produz quatro produtos analíticos:

- Clientes por estado;
- Clientes por faixa etária;
- Clientes por faixa de renda;
- Clientes por canal preferido.

---

## 2. Entrada e Saídas

### Entrada

`data/silver/customers.parquet`

A entrada contém 10.000 registros e 12 colunas.

### Diretório de saída

`data/analytics/`

### Produtos gerados

| Arquivo | Dimensão | Grupos gerados |
|---|---|---:|
| `customers_by_state.parquet` | `estado` | 27 |
| `customers_by_age.parquet` | `faixa_etaria` | 6 |
| `customers_by_income.parquet` | `faixa_renda` | 5 |
| `customers_by_channel.parquet` | `canal_preferido` | 4 |

### Script de execução

`src/build_analytics.py`

### Módulos

| Módulo | Responsabilidade |
|---|---|
| `utils/analytics/definitions.py` | Definir produtos, colunas obrigatórias, métricas e limite mínimo de grupo. |
| `utils/analytics/validator.py` | Validar os dados necessários às agregações. |
| `utils/analytics/processor.py` | Construir as tabelas agregadas. |

---

## 3. Finalidade Analítica

A finalidade da Analytics é produzir indicadores comerciais agregados para acompanhar características gerais da base de clientes e seu comportamento de compra.

Os produtos são organizados por dimensões relevantes para análise de negócio.

Os resultados não incluem o identificador individual de cliente.

---

## 4. Contrato de Saída

Cada produto contém uma dimensão de agrupamento e quatro indicadores.

| Campo | Descrição |
|---|---|
| Dimensão | Estado, faixa etária, faixa de renda ou canal preferido. |
| `quantidade_clientes` | Quantidade de clientes distintos no grupo. |
| `receita_total` | Soma do valor total de compras dos clientes do grupo. |
| `quantidade_compras` | Soma da quantidade de compras dos clientes do grupo. |
| `ticket_medio` | Receita total dividida pela quantidade de compras do grupo. |

O `customer_id` é utilizado internamente para a contagem de clientes distintos, mas não integra o esquema de saída.

---

## 5. Regras de Agregação

### 5.1 Quantidade de clientes

A quantidade de clientes é calculada pela contagem distinta de `customer_id` em cada grupo.

```text
quantidade_clientes = COUNT DISTINCT(customer_id)
```

### 5.2 Receita total

A receita total é calculada pela soma de `valor_total_compras`.

```text
receita_total = SUM(valor_total_compras)
```

### 5.3 Quantidade de compras

A quantidade de compras é calculada pela soma de `quantidade_compras`.

```text
quantidade_compras = SUM(quantidade_compras)
```

### 5.4 Ticket médio

O ticket médio agregado é calculado pela divisão da receita total pela quantidade de compras do grupo.

```text
ticket_medio = receita_total / quantidade_compras
```

O cálculo é realizado somente quando a quantidade de compras do grupo é maior que zero.

Quando não há compras, o valor atribuído é `0.0`.

O ticket médio agregado não é calculado pela média simples dos tickets médios individuais.

---

## 6. Regra de Divulgação

Foi definido um limite mínimo de 10 clientes por grupo.

A configuração está localizada em:

`utils/analytics/definitions.py`

```python
MIN_GROUP_SIZE = 10
```

A regra é aplicada após a agregação:

```python
aggregated = aggregated.loc[
    aggregated["quantidade_clientes"] >= MIN_GROUP_SIZE
].copy()
```

Grupos com menos de 10 clientes não são publicados.

O limite é uma escolha didática do case para reduzir a exposição de grupos pequenos.

Ele não representa uma garantia de anonimização.

O risco de identificação indireta depende também da granularidade dos dados, da combinação entre resultados e da disponibilidade de outras fontes.

---

## 7. Validação dos Dados de Entrada

Antes da agregação, o processamento verifica:

- Presença das colunas obrigatórias;
- Ausência de valores nulos em `customer_id`;
- Ausência de identificadores duplicados;
- Ausência de valores nulos nas dimensões utilizadas;
- Ausência de valores nulos nas métricas comerciais;
- Tipos numéricos nas métricas comerciais;
- Ausência de valores numéricos não finitos;
- Ausência de valores negativos nas métricas comerciais.

Quando uma regra é violada, o processamento é interrompido com uma mensagem específica.

---

## 8. Produtos Analíticos

### 8.1 Clientes por Estado

**Arquivo:**

`data/analytics/customers_by_state.parquet`

**Dimensão:**

`estado`

**Resultado registrado:**

27 grupos.

O produto permite analisar a distribuição dos clientes e das métricas comerciais entre os estados.

### 8.2 Clientes por Faixa Etária

**Arquivo:**

`data/analytics/customers_by_age.parquet`

**Dimensão:**

`faixa_etaria`

**Resultado registrado:**

6 grupos.

O produto permite analisar o comportamento comercial por faixa etária, sem disponibilizar a data de nascimento original.

### 8.3 Clientes por Faixa de Renda

**Arquivo:**

`data/analytics/customers_by_income.parquet`

**Dimensão:**

`faixa_renda`

**Resultado registrado:**

5 grupos.

O produto permite analisar o comportamento comercial por faixa de renda, sem disponibilizar o valor original da renda mensal.

### 8.4 Clientes por Canal Preferido

**Arquivo:**

`data/analytics/customers_by_channel.parquet`

**Dimensão:**

`canal_preferido`

**Resultado registrado:**

4 grupos.

O produto permite analisar a distribuição dos clientes e das métricas comerciais por canal preferido.

---

## 9. Execução

O processamento é executado na raiz do projeto com:

```powershell
python -m src.build_analytics
```

### Resultado registrado

```text
BUILDING ANALYTICS LAYER
[PASSED] Input rows: 10000
[INFO] Minimum group size: 10
[PASSED] customers_by_age: 6 groups
[PASSED] customers_by_income: 5 groups
[PASSED] customers_by_channel: 4 groups
ANALYTICS LAYER SUCCESSFULLY BUILT
```

A execução também gerou o produto `customers_by_state.parquet`, posteriormente lido com sucesso, contendo 27 grupos.

---

## 10. Resultado da Divulgação

Os grupos publicados possuem pelo menos 10 clientes.

No dataset utilizado, todos os grupos apresentados nas quatro tabelas atendem ao limite configurado.

Nenhum produto disponibiliza `customer_id`.

As saídas permanecem classificadas como produtos analíticos de acesso controlado.

---

## 11. Limitações

A agregação e a aplicação do limite mínimo de grupo não comprovam anonimização irreversível.

A combinação entre diferentes tabelas, outras fontes de dados ou resultados complementares pode aumentar o risco de identificação indireta.

Os indicadores financeiros utilizam valores `float64`, que não oferecem precisão decimal exata para cálculos financeiros de produção.

O case não implementa permissões efetivas de acesso ao armazenamento local nem auditoria completa de consultas aos produtos analíticos.

---

## 12. Referências Internas

- `src/build_analytics.py`
- `utils/analytics/definitions.py`
- `utils/analytics/validator.py`
- `utils/analytics/processor.py`
- `docs/silver-rules.md`
- `docs/security/access_control.md`
- `docs/architecture.md`