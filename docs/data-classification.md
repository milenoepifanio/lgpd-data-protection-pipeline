
# Classificação de Dados e Requisitos de Proteção

## 1. Objetivo

Este documento apresenta a classificação dos dados utilizados no case
de LGPD e Segurança aplicada à Engenharia de Dados.

O objetivo é identificar os atributos que exigem proteção, definir
os tratamentos necessários e estabelecer requisitos de privacidade
para o processamento dos dados ao longo do pipeline.

A classificação é utilizada como referência para a política técnica
definida em `config/data_classification.yaml`.

---

## 2. Contexto do Projeto

O case utiliza um dataset sintético de clientes de um e-commerce,
gerado com Python para fins de estudo.

A arquitetura proposta contempla o fluxo:

Raw Restrita → Proteção → Silver → Analytics

O dataset original contém 10.000 registros e 24 colunas.

A classificação identificou:

- 21 atributos classificados como dados pessoais;
- 3 atributos classificados como dados pessoais sensíveis.

Essa classificação considera o contexto de uso dos atributos no
dataset. Dados pseudonimizados ou generalizados podem continuar
sendo dados pessoais quando houver possibilidade de identificação
direta ou indireta.

---

## 3. Finalidade do Tratamento

A finalidade do case é demonstrar a aplicação de mecanismos de
proteção em um pipeline de Engenharia de Dados e produzir informações
analíticas sobre uma base fictícia de clientes.

As finalidades técnicas e analíticas incluem:

- Demonstrar a identificação e classificação de dados pessoais;
- Aplicar minimização e proteção de atributos;
- Preparar dados para análises comerciais;
- Produzir indicadores agregados;
- Documentar requisitos de segurança e governança.

A disponibilização de dados deve ser compatível com a finalidade
definida para cada camada.

---

## 4. Critérios de Classificação

### 4.1 Dados pessoais

São informações relacionadas a uma pessoa natural identificada ou
identificável.

No contexto do case, essa categoria inclui identificadores diretos
e atributos que podem contribuir para identificação indireta.

Exemplos:

- Nome;
- CPF;
- E-mail;
- Telefone;
- Data de nascimento;
- CEP;
- Identificador de cliente.

### 4.2 Dados pessoais sensíveis

São atributos enquadrados nas categorias de dados pessoais sensíveis
previstas na LGPD.

No dataset, foram classificados como sensíveis:

- `raca_etnia`;
- `condicao_saude`;
- `tipo_sanguineo`.

Esses atributos não são necessários para a finalidade analítica
definida no case e, por isso, são removidos durante a proteção.

### 4.3 Dados pseudonimizados

São dados submetidos a uma transformação que reduz a associação
direta com a identidade original.

No projeto, o campo `customer_id` é pseudonimizado com HMAC-SHA256.

A pseudonimização não equivale à anonimização. O resultado continua
sujeito aos requisitos de proteção aplicáveis aos dados pessoais.

---

## 5. Inventário e Tratamento dos Atributos

A política técnica de classificação está definida em:

`config/data_classification.yaml`

O dataset contém 24 atributos, distribuídos pelas seguintes ações:

| Ação | Quantidade | Objetivo |
|---|---:|---|
| Preservar | 13 | Manter atributos necessários ao processamento. |
| Remover | 7 | Eliminar atributos desnecessários à finalidade. |
| Generalizar | 3 | Reduzir a granularidade de informações. |
| Pseudonimizar | 1 | Substituir o identificador original por um valor derivado. |
| **Total** | **24** | |

### 5.1 Atributos removidos

| Campo | Classificação | Justificativa |
|---|---|---|
| `nome` | Dado pessoal | Identificador direto desnecessário para a análise. |
| `cpf` | Dado pessoal | Identificador direto desnecessário para a análise. |
| `email` | Dado pessoal | Informação de contato desnecessária para a análise. |
| `telefone` | Dado pessoal | Informação de contato desnecessária para a análise. |
| `raca_etnia` | Dado pessoal sensível | Não é necessário para a finalidade do case. |
| `condicao_saude` | Dado pessoal sensível | Não é necessário para a finalidade do case. |
| `tipo_sanguineo` | Dado pessoal sensível | Não é necessário para a finalidade do case. |

### 5.2 Atributo pseudonimizado

| Campo de origem | Tratamento | Finalidade |
|---|---|---|
| `customer_id` | HMAC-SHA256 | Permitir a vinculação consistente de registros sem expor o identificador original. |

### 5.3 Atributos generalizados

| Campo de origem | Campo resultante | Finalidade |
|---|---|---|
| `data_nascimento` | `faixa_etaria` | Analisar perfis etários sem disponibilizar a data completa. |
| `cep` | `regiao_cep` | Reduzir a granularidade da localização. |
| `renda_mensal` | `faixa_renda` | Permitir análises por faixa de renda sem disponibilizar o valor original. |

Os limites das faixas e as regras exatas de transformação devem
seguir a implementação de `utils/protection/generalization.py`.

### 5.4 Atributos preservados

Os 13 atributos restantes são mantidos conforme a política YAML.

A relação nominal desses campos e suas respectivas justificativas
devem ser conferidas diretamente em `config/data_classification.yaml`.

A preservação na camada Protected não implica necessidade de
disponibilização integral nas camadas Silver e Analytics.

---

## 6. Requisitos de Proteção

Os requisitos definidos para o case são:

1. Remover identificadores diretos que não sejam necessários;
2. Remover dados pessoais sensíveis fora da finalidade analítica;
3. Pseudonimizar o identificador de cliente;
4. Generalizar atributos selecionados;
5. Preservar somente os campos necessários em cada etapa;
6. Restringir o acesso conforme a responsabilidade profissional;
7. Evitar exposição de dados individuais nos produtos analíticos;
8. Documentar retenção, descarte e rastreabilidade.

As regras efetivamente implementadas são detalhadas em
`docs/protection-rules.md`.

A matriz de acesso proposta está documentada em
`docs/security/access_control.md`.

---

## 7. Minimização por Camada

| Camada | Diretriz de minimização |
|---|---|
| Raw Restrita | Manter os dados sintéticos originais necessários à demonstração do processo. |
| Protected | Aplicar remoção, pseudonimização e generalização. |
| Silver | Selecionar os atributos necessários às transformações e análises definidas. |
| Analytics | Disponibilizar indicadores agregados, evitando identificadores individuais desnecessários. |

A minimização deve ser reavaliada a cada mudança de finalidade
ou inclusão de um novo produto analítico.

---

## 8. Retenção e Descarte

A retenção dos dados deve ser compatível com a finalidade do
tratamento e com eventuais obrigações aplicáveis.

Para o case, propõem-se as seguintes diretrizes:

- Raw: conservar somente enquanto necessária à demonstração e
  à reprodução do processo de proteção;
- Protected: conservar enquanto necessária à execução e validação
  das transformações posteriores;
- Silver: conservar conforme a necessidade de processamento e
  atualização dos produtos analíticos;
- Analytics: conservar conforme a necessidade de consulta e
  atualização dos indicadores.

O projeto ainda não implementa descarte automatizado nem define
prazos numéricos de retenção.

Esses pontos permanecem como requisitos de governança para uma
eventual implantação corporativa.

---

## 9. Limitações

O dataset é sintético e foi criado para fins educacionais.

A classificação e as transformações demonstram práticas de
proteção, mas não comprovam anonimização irreversível.

A camada Protected continua sendo tratada como contendo dados
pessoais pseudonimizados.

Os controles de acesso documentados representam requisitos de
arquitetura e não permissões efetivamente aplicadas ao armazenamento
local.

---

## 10. Referências Internas

- `config/data_classification.yaml`
- `src/generate_data.py`
- `src/classify_data.py`
- `src/protect_data.py`
- `docs/protection-rules.md`
- `docs/security/access_control.md`
- `docs/architecture.md`