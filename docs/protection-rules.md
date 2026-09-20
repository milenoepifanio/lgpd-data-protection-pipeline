
# Regras de Proteção de Dados

## 1. Objetivo

Este documento descreve as regras de proteção implementadas no
pipeline de Engenharia de Dados, responsável pela transformação
da camada Raw Restrita para a camada Protected.

O objetivo é demonstrar a aplicação de mecanismos de minimização,
pseudonimização e generalização sobre dados sintéticos de clientes.

As regras são orientadas pela política definida em
`config/data_classification.yaml`.

---

## 2. Fluxo de Proteção

O processamento segue o fluxo:

Raw Restrita → Classificação → Proteção → Protected → Validação

### Entrada

`data/raw/customers.parquet`

### Saída

`data/protected/customers.parquet`

### Componentes principais

| Componente | Responsabilidade |
|---|---|
| `config/data_classification.yaml` | Definir a classificação e a ação de proteção de cada atributo. |
| `src/protect_data.py` | Executar o processo de proteção. |
| `utils/protection/processor.py` | Aplicar as regras e construir o esquema de saída. |
| `utils/protection/pseudonymization.py` | Implementar a pseudonimização. |
| `utils/protection/generalization.py` | Implementar as generalizações. |
| `src/validate_protection.py` | Executar a validação da camada Protected. |

---

## 3. Resumo das Transformações

O dataset original possui 10.000 registros e 24 colunas.

As ações configuradas são:

| Ação | Quantidade de atributos |
|---|---:|
| Preservação | 13 |
| Remoção | 7 |
| Generalização | 3 |
| Pseudonimização | 1 |
| **Total** | **24** |

Após o processamento, a camada Protected contém:

- 10.000 registros;
- 17 colunas.

A quantidade de registros é preservada, enquanto os sete atributos
configurados para remoção deixam de existir na saída.

Os campos generalizados substituem os atributos originais.

---

## 4. Remoção de Atributos

A remoção elimina campos que não são necessários para a finalidade
analítica do case.

Os seguintes atributos são removidos:

| Campo | Justificativa |
|---|---|
| `nome` | Identificador direto. |
| `cpf` | Identificador direto. |
| `email` | Informação de contato. |
| `telefone` | Informação de contato. |
| `raca_etnia` | Dado pessoal sensível. |
| `condicao_saude` | Dado pessoal sensível. |
| `tipo_sanguineo` | Dado pessoal sensível. |

Os atributos removidos não devem estar presentes no esquema da
camada Protected.

---

## 5. Pseudonimização

### 5.1 Campo protegido

`customer_id`

### 5.2 Mecanismo

O identificador é transformado utilizando HMAC-SHA256, com uma chave
secreta fornecida por variável de ambiente.

A transformação permite gerar um valor consistente para o mesmo
identificador, preservando a possibilidade de vinculação entre
registros quando necessário.

### 5.3 Gerenciamento da chave

A chave não deve ser escrita diretamente no código-fonte nem
versionada no repositório.

No ambiente local, ela é fornecida por meio de configuração de
ambiente.

Em uma implantação corporativa, o armazenamento e o acesso à chave
devem ser gerenciados por um mecanismo apropriado de proteção
de segredos.

### 5.4 Limitações

HMAC-SHA256 é utilizado como mecanismo de pseudonimização neste
projeto.

O resultado não deve ser considerado anônimo apenas porque o
identificador original foi substituído.

A camada Protected continua sujeita aos requisitos de proteção
aplicáveis aos dados pessoais.

---

## 6. Generalização

A generalização reduz a granularidade de atributos selecionados,
preservando sua utilidade analítica.

### 6.1 Data de nascimento

**Origem:** `data_nascimento`

**Saída:** `faixa_etaria`

A data completa é substituída por uma categoria de faixa etária.

A regra permite análises por grupos de idade sem disponibilizar
a data de nascimento original.

### 6.2 CEP

**Origem:** `cep`

**Saída:** `regiao_cep`

O CEP completo é substituído por uma representação regional
de menor granularidade.

A regra implementada utiliza os cinco primeiros dígitos do CEP.

Essa redução não garante anonimização e ainda pode representar
uma localização relativamente específica.

### 6.3 Renda mensal

**Origem:** `renda_mensal`

**Saída:** `faixa_renda`

O valor numérico original é substituído por uma categoria
de faixa de renda.

A transformação permite análises de distribuição de renda
sem disponibilizar o valor exato.

### 6.4 Regras técnicas

Os limites das faixas etárias e de renda, assim como o tratamento
de valores ausentes ou inválidos, devem ser consultados em:

`utils/protection/generalization.py`

Esse módulo é a referência para o comportamento efetivamente
implementado.

---

## 7. Preservação de Atributos

Os 13 atributos configurados com a ação de preservação são
mantidos sem transformação de valor durante a etapa de proteção.

A lista nominal é definida em:

`config/data_classification.yaml`

A preservação na Protected não implica disponibilização automática
nas camadas posteriores.

Na Silver e na Analytics, os atributos deverão ser selecionados
conforme a finalidade de cada processamento.

---

## 8. Construção do Esquema de Saída

O esquema da camada Protected é construído a partir da política
de classificação.

O processamento deve:

1. Manter os campos configurados para preservação;
2. Excluir os campos configurados para remoção;
3. Substituir os campos generalizados pelos atributos resultantes;
4. Aplicar a pseudonimização ao identificador configurado;
5. Organizar as colunas conforme o esquema esperado.

A lógica de construção do esquema está implementada em:

`utils/protection/processor.py`

---

## 9. Validação da Proteção

A validação é executada por:

`src/validate_protection.py`

O processo combina a comparação entre Raw e Protected com
expectativas de qualidade implementadas com Great Expectations.

### 9.1 Comparação entre Raw e Protected

A validação verifica:

- Preservação da quantidade de registros;
- Presença das colunas esperadas;
- Ausência das colunas removidas;
- Valores dos atributos preservados;
- Valores pseudonimizados esperados;
- Valores generalizados esperados.

### 9.2 Great Expectations

As expectativas utilizadas verificam aspectos como:

- Ordem das colunas;
- Ausência de valores nulos nos campos definidos;
- Unicidade de identificadores;
- Formato dos valores pseudonimizados;
- Domínios permitidos para atributos categóricos.

### 9.3 Resultado observado

A execução da validação retornou:

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

O resultado demonstra que a saída produzida corresponde às
transformações configuradas e às expectativas implementadas.

Ele não constitui prova de anonimização irreversível.

---

## 10. Segurança e Controle de Acesso

O controle de acesso por perfil profissional foi definido
em documento específico:

`docs/security/access_control.md`

A matriz contempla:

- Engenheiro de Dados;
- Administrador de Banco de Dados;
- Cientista de Dados;
- Analista de Negócios.

No ambiente local, essa matriz representa um requisito
de arquitetura.

Não foi implementado um mecanismo que impeça o acesso direto
aos arquivos por usuários que já possuam permissão no
sistema operacional.

---

## 11. Limitações e Evolução

Os mecanismos implementados demonstram proteção de atributos
durante a transformação Raw → Protected.

Permanecem como pontos de evolução:

- Implementação efetiva de permissões no armazenamento;
- Auditoria de acessos;
- Política operacional de retenção e descarte;
- Avaliação de risco de identificação indireta nos produtos analíticos;
- Construção das camadas Silver e Analytics.

A eventual anonimização de produtos analíticos deverá ser avaliada
considerando o conteúdo final disponibilizado e o risco de
reidentificação.

---

## 12. Referências Internas

- `config/data_classification.yaml`
- `src/protect_data.py`
- `src/validate_protection.py`
- `utils/protection/processor.py`
- `utils/protection/pseudonymization.py`
- `utils/protection/generalization.py`
- `utils/validation/comparator.py`
- `docs/data-classification.md`
- `docs/security/access_control.md`
- `docs/architecture.md`