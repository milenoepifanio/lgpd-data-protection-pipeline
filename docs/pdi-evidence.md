
# Evidências do PDI — LGPD e Segurança Aplicada à Engenharia de Dados

## 1. Identificação

**Competência:** Hard Skills — Arquitetura de Dados (Data Warehouse, Data Lake etc.) — LGPD e Segurança aplicada à Engenharia de Dados.

**Projeto:** Case prático de proteção e preparação de dados sintéticos de clientes.

**Arquitetura:** Raw Restrita → Proteção → Protected → Silver → Analytics.

**Tecnologias:** Python, Pandas, Parquet, YAML, HMAC-SHA256 e Great Expectations.

---

## 2. Objetivo do PDI

Realizar capacitação em LGPD e Segurança da Informação aplicada à Engenharia de Dados, desenvolvendo competências para identificar, proteger e governar dados pessoais e sensíveis durante seu ciclo de vida.

As ações previstas incluem:

- Estudar fundamentos da LGPD e segurança aplicada a dados;
- Identificar e classificar dados pessoais e sensíveis;
- Aplicar conceitos de finalidade, minimização e retenção;
- Estudar anonimização, pseudonimização e criptografia;
- Aplicar práticas de controle de acesso e rastreabilidade;
- Desenvolver um case prático utilizando dados fictícios.

---

## 3. Tarefa 1 — Fundamentos de LGPD, Privacidade e Segurança de Dados

**Situação:** Concluída.

### Atividades realizadas

- Realização de capacitação sobre LGPD;
- Estudo dos principais conceitos e fundamentos da legislação;
- Produção de resumo para consulta.

### Evidências

- Registro de conclusão da capacitação;
- Material de estudo produzido.

---

## 4. Tarefa 2 — Classificação dos Dados e Definição de Requisitos de Proteção

**Situação:** Concluída.

### Atividades realizadas

- Geração de um dataset sintético de clientes;
- Identificação de atributos pessoais e sensíveis;
- Definição das ações de proteção por atributo;
- Criação de política de classificação em YAML;
- Documentação dos requisitos de proteção.

### Resultados

| Indicador | Resultado |
|---|---:|
| Registros gerados | 10.000 |
| Atributos na Raw | 24 |
| Atributos classificados como pessoais | 21 |
| Atributos classificados como sensíveis | 3 |

### Evidências

- `src/generate_data.py`
- `src/classify_data.py`
- `config/data_classification.yaml`
- `docs/data-classification.md`

---

## 5. Tarefa 3 — Aplicação de Mecanismos de Proteção

**Situação:** Implementação das transformações concluída; requisitos complementares de governança documentados.

### Atividades realizadas

- Remoção de identificadores diretos desnecessários;
- Remoção de atributos pessoais sensíveis fora da finalidade;
- Pseudonimização de `customer_id` com HMAC-SHA256;
- Generalização de data de nascimento, CEP e renda;
- Validação automatizada das transformações;
- Definição de matriz de acesso por perfil profissional.

### Resultados

| Ação | Quantidade de atributos |
|---|---:|
| Preservação | 13 |
| Remoção | 7 |
| Generalização | 3 |
| Pseudonimização | 1 |

A camada Protected foi gerada com 10.000 registros e 17 colunas.

### Evidência de validação

```text
Protection transformation validation
[PASSED] Protection transformations match the configured policy.

Great Expectations validation
[PASSED] expect_table_columns_to_match_ordered_list
[PASSED] expect_column_values_to_not_be_null
[PASSED] expect_column_values_to_be_unique
[PASSED] expect_column_values_to_match_regex
[PASSED] expect_column_values_to_be_in_set
[PASSED] expect_column_values_to_be_in_set
[PASSED] expect_column_values_to_match_regex

GREAT EXPECTATIONS VALIDATION SUCCESSFUL
PROTECTION VALIDATION SUCCESSFUL
```

### Evidências

- `src/protect_data.py`
- `src/validate_protection.py`
- `utils/protection/`
- `utils/validation/`
- `docs/protection-rules.md`
- `docs/security/access_control.md`

### Limitações

A pseudonimização não equivale à anonimização.

A matriz de acesso foi documentada, mas não foi implementado um mecanismo específico para impedir acesso direto aos arquivos locais.

A política de retenção e descarte permanece documentada como requisito, sem automação.

---

## 6. Tarefa 4 — Desenvolvimento do Case de Arquitetura

**Situação:** Pipeline implementado de ponta a ponta.

### Arquitetura

```text
Raw Restrita
    |
    v
Proteção
    |
    v
Protected
    |
    v
Silver
    |
    v
Analytics
```

### 6.1 Construção da Silver

A Silver foi desenvolvida para preparar os dados protegidos para consumo analítico.

Atividades realizadas:

- Seleção dos atributos necessários;
- Conversão de datas;
- Validação de consistência;
- Cálculo do ticket médio;
- Gravação do resultado em Parquet.

**Comando de execução:**

```powershell
python -m src.build_silver
```

**Log registrado:**

```text
BUILDING SILVER LAYER
[PASSED] Input rows: 10000
[PASSED] Silver rows: 10000
[PASSED] Silver columns: 12
[PASSED] Output: C:\Users\Mileno\Downloads\Projeto LGPD\data\silver\customers.parquet
SILVER LAYER SUCCESSFULLY BUILT
```

**Resultado:** 10.000 registros e 12 colunas.

### 6.2 Construção da Analytics

A Analytics foi desenvolvida para produzir indicadores comerciais agregados a partir da Silver.

Atividades realizadas:

- Agregação por estado;
- Agregação por faixa etária;
- Agregação por faixa de renda;
- Agregação por canal preferido;
- Cálculo de clientes distintos, receita, quantidade de compras e ticket médio;
- Aplicação de limite mínimo de 10 clientes por grupo;
- Gravação dos produtos em Parquet.

**Comando de execução:**

```powershell
python -m src.build_analytics
```

**Resultado registrado:**

```text
BUILDING ANALYTICS LAYER
[PASSED] Input rows: 10000
[INFO] Minimum group size: 10
[PASSED] customers_by_age: 6 groups
[PASSED] customers_by_income: 5 groups
[PASSED] customers_by_channel: 4 groups
ANALYTICS LAYER SUCCESSFULLY BUILT
```

O arquivo `customers_by_state.parquet` também foi gerado e lido com sucesso, contendo 27 grupos.

### 6.3 Produtos Gerados

| Produto | Grupos |
|---|---:|
| Clientes por estado | 27 |
| Clientes por faixa etária | 6 |
| Clientes por faixa de renda | 5 |
| Clientes por canal preferido | 4 |

Os produtos não disponibilizam o identificador individual de cliente.

### 6.4 Evidências

- `src/build_silver.py`
- `utils/silver/`
- `data/silver/customers.parquet`
- `src/build_analytics.py`
- `utils/analytics/`
- `data/analytics/`
- `docs/silver-rules.md`
- `docs/analytics-rules.md`
- `docs/architecture.md`

---

## 7. Resultado Consolidado

| Camada | Registros ou grupos | Colunas |
|---|---:|---:|
| Raw | 10.000 registros | 24 |
| Protected | 10.000 registros | 17 |
| Silver | 10.000 registros | 12 |
| Analytics — Estado | 27 grupos | 5 |
| Analytics — Faixa etária | 6 grupos | 5 |
| Analytics — Faixa de renda | 5 grupos | 5 |
| Analytics — Canal preferido | 4 grupos | 5 |

O pipeline demonstra a aplicação progressiva de minimização, proteção e preparação analítica.

---

## 8. Competências Desenvolvidas

O case proporcionou a aplicação prática de conceitos relacionados a:

- Classificação de dados pessoais e sensíveis;
- Finalidade e minimização;
- Pseudonimização;
- Generalização;
- Gerenciamento de segredos;
- Validação de transformações;
- Organização de pipelines por camadas;
- Preparação de dados para consumo analítico;
- Definição de requisitos de controle de acesso;
- Documentação técnica e de governança.

---

## 9. Limitações do Case

O projeto utiliza dados sintéticos e processamento local.

Os controles de acesso foram documentados, mas não aplicados efetivamente ao armazenamento.

Não foram implementados mecanismos completos de auditoria de acesso nem descarte automatizado.

A Protected e a Silver contêm dados pseudonimizados.

A Analytics contém dados agregados e aplica um limite mínimo de grupo, mas não foi demonstrada anonimização irreversível.

As transformações e validações implementadas representam um case educacional e não substituem uma avaliação de privacidade e segurança para dados reais.

---

## 10. Entregáveis do PDI

| Entregável previsto | Evidência |
|---|---|
| Curso ou capacitação em LGPD e Segurança | Capacitação concluída e resumo produzido. |
| Case prático utilizando dados fictícios | Pipeline Python com Raw, Protected, Silver e Analytics. |
| Arquitetura da solução | `docs/architecture.md` e documentação complementar. |

---

## 11. Conclusão

O case demonstra a aplicação de conceitos de LGPD e Segurança da Informação em um pipeline de Engenharia de Dados, desde a classificação dos dados até a geração de produtos analíticos agregados.

A implementação contempla mecanismos de minimização, pseudonimização e generalização, além de validações automatizadas e documentação dos requisitos de governança.

O projeto também explicita os limites da implementação local, distinguindo as transformações efetivamente executadas dos controles de segurança previstos para uma eventual implantação corporativa.