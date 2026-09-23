# Configuração de Classificação e Proteção

Esta pasta contém a política declarativa utilizada para classificar os
atributos da base de clientes e definir o tratamento aplicado em cada
camada do pipeline.

## Arquivo

| Arquivo | Finalidade |
| --- | --- |
| `data_classification.yaml` | Define classificação, identificação, nível de proteção, finalidade e ação técnica por coluna. |

## Conteúdo da política

A política descreve:

- metadados do dataset e seu domínio de negócio;
- classificações `non_personal_data`, `personal_data` e `sensitive_personal_data`;
- níveis de proteção de `low` a `critical`;
- necessidade analítica de cada atributo;
- ações `retain`, `remove`, `pseudonymize` e `generalize`;
- métodos e colunas de saída das transformações.

## Regras atuais

O `customer_id` é pseudonimizado com HMAC-SHA256. Identificadores diretos
como nome, CPF, e-mail e telefone são removidos da Protected. Datas de
nascimento, CEP e renda mensal são generalizados. `condicao_saude` é
preservada na Protected exclusivamente para a coorte analítica autorizada
de Diabetes, Hipertensão e Obesidade; os demais dados sensíveis são removidos.

O registro restrito mantém os dados originais para rastreabilidade autorizada;
isso não altera a política de exposição da camada Protected.

## Uso

A política é carregada e validada pelos módulos de classificação e utilizada
durante a proteção:

```powershell
python -m src.classify_data
python -m src.protect_data
```

Alterações neste arquivo podem modificar o schema, as transformações e os
requisitos de validação. Toda mudança deve ser acompanhada de validação do
dataset e revisão das regras de privacidade.
