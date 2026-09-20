
# Controle de Acesso e Segurança dos Dados

## 1. Objetivo

Este documento define os requisitos de controle de acesso e segurança
para o case de Engenharia de Dados desenvolvido como parte do PDI
de LGPD e Segurança aplicada à Engenharia de Dados.

A arquitetura considera o seguinte fluxo:

Raw Restrita → Proteção → Silver → Analytics

O objetivo é estabelecer quais processos e perfis devem acessar cada
camada, considerando a classificação dos dados, a finalidade do
tratamento e o princípio do menor privilégio.

---

## 2. Contexto do Projeto

O projeto utiliza um dataset sintético de clientes, gerado para
demonstrar a aplicação de mecanismos de proteção de dados.

A camada Raw contém os dados originais, incluindo identificadores
diretos e atributos classificados como dados pessoais sensíveis.

O processamento de proteção aplica as regras definidas em
`config/data_classification.yaml`, incluindo:

- Remoção de atributos;
- Pseudonimização de identificadores com HMAC-SHA256;
- Generalização de atributos;
- Preservação de campos necessários ao processamento.

A camada Protected é validada por meio da comparação com a Raw
e de expectativas de qualidade implementadas com Great Expectations.

Os dados da Protected continuam sendo tratados como dados pessoais
pseudonimizados. A pseudonimização não equivale à anonimização.

---

## 3. Classificação das Camadas

| Camada | Classificação | Conteúdo |
|---|---|---|
| Raw | Restrita | Dados originais, incluindo identificadores diretos e dados sensíveis. |
| Protected | Confidencial | Dados minimizados, pseudonimizados e generalizados. |
| Silver | Uso interno controlado | Dados tratados e estruturados para finalidades analíticas definidas. |
| Analytics | Acesso conforme finalidade | Indicadores e resultados analíticos, preferencialmente agregados. |

A classificação das camadas representa os requisitos definidos para
a arquitetura. Ela não implica que todas as restrições de acesso
estejam tecnicamente implementadas no ambiente local.

---


## 4. Matriz de Acesso Proposta

| Perfil profissional | Raw Restrita | Protected | Silver | Analytics |
|---|---|---|---|---|
| Engenheiro de Dados | Leitura e escrita | Leitura e escrita | Leitura e escrita | Leitura e escrita |
| Administrador de Banco de Dados (DBA) | Administração completa | Administração completa | Administração completa | Administração completa |
| Cientista de Dados | Sem acesso | Leitura autorizada | Leitura autorizada | Leitura autorizada |
| Analista de Negócios | Sem acesso | Sem acesso | Sem acesso direto | Leitura autorizada |

### 4.1 Diretrizes de Acesso

- **Engenharia de Dados:** responsável pela ingestão, proteção, transformação e disponibilização dos dados, com acesso completo às camadas do pipeline.
- **Administrador de Banco de Dados (DBA):** responsável pela administração dos recursos de armazenamento, permissões, disponibilidade e manutenção dos dados.
- **Ciência de Dados:** acesso aos dados protegidos e preparados para desenvolvimento de modelos, respeitando a finalidade do tratamento.
- **Análise de Negócios:** acesso aos indicadores e produtos analíticos disponibilizados na camada Analytics, sem necessidade de consultar dados individuais das camadas anteriores.

> **Observação:** esta matriz representa uma proposta de permissões para o case. Em produção, mesmo os acessos amplos de Engenharia de Dados e DBA devem ser individualizados, auditáveis e limitados às responsabilidades de cada função, seguindo o princípio do menor privilégio.

As permissões devem ser concedidas conforme a necessidade de cada
processo ou perfil, evitando acesso indiscriminado às camadas.

A matriz é uma proposta de arquitetura, não uma configuração de
permissões aplicada aos arquivos locais.

---

## 5. Requisitos de Segurança

### 5.1 Princípio do Menor Privilégio

Cada perfil ou serviço deve receber apenas as permissões necessárias
para executar suas atividades.

O acesso à Raw deve ser limitado aos processos responsáveis pela
proteção e aos administradores expressamente autorizados.

### 5.2 Segregação por Camada

Os dados originais devem permanecer separados dos dados protegidos
e dos produtos analíticos.

Os consumidores da Analytics não devem depender de acesso direto
à Raw para obter indicadores.

### 5.3 Gerenciamento de Segredos

A chave utilizada na pseudonimização HMAC-SHA256 não deve ser
armazenada diretamente no código-fonte ou versionada no repositório.

No ambiente local, a chave é fornecida por variável de ambiente.

Em um ambiente corporativo, recomenda-se utilizar um serviço de
gerenciamento de segredos, com permissões restritas aos processos
que necessitam da chave.

### 5.4 Rastreabilidade

Em uma implementação corporativa, devem ser registrados eventos
relevantes, como:

- Identidade do serviço ou usuário;
- Recurso acessado;
- Operação realizada;
- Data e horário;
- Resultado da operação.

Esses registros devem permitir a investigação de acessos indevidos
e a verificação da aplicação das políticas.

### 5.5 Retenção e Descarte

Os dados devem ser mantidos somente pelo período necessário às
finalidades definidas, observadas eventuais obrigações legais
aplicáveis.

O prazo de retenção, os responsáveis e os procedimentos de descarte
devem ser definidos para cada conjunto de dados.

No case local, a política de retenção será documentada como requisito
de arquitetura, sem alegar a existência de descarte automatizado.

---

## 6. Implementação Local e Limitações

O case é executado localmente, com Python e arquivos Parquet.

Os mecanismos efetivamente implementados incluem:

- Classificação dos dados por política YAML;
- Remoção de atributos definidos pela política;
- Pseudonimização com HMAC-SHA256;
- Generalização de atributos;
- Validação automatizada da camada Protected.

O projeto não implementa, até esta etapa, um mecanismo de autorização
capaz de impedir o acesso direto aos arquivos por usuários que já
possuam permissões no sistema operacional.

Portanto, a matriz de acesso apresentada neste documento representa
um requisito para a arquitetura, e não um controle efetivo do
armazenamento local.

---

## 7. Implementação em Ambiente Corporativo

Em um ambiente corporativo, os requisitos poderiam ser implementados
com os seguintes mecanismos:

| Requisito | Mecanismo proposto |
|---|---|
| Restrição de acesso às camadas | IAM, RBAC e permissões de armazenamento |
| Segregação de dados | Recursos, diretórios ou buckets separados |
| Proteção de segredos | Serviço de gerenciamento de segredos |
| Criptografia em repouso | Criptografia gerenciada pelo armazenamento |
| Criptografia em trânsito | Conexões seguras, como TLS |
| Rastreabilidade | Logs de acesso e auditoria |
| Retenção e descarte | Políticas de ciclo de vida e processos de exclusão |

A escolha e a configuração dos serviços dependem da plataforma
adotada e dos requisitos organizacionais.

---

## 8. Conclusão

O case demonstra a classificação e a aplicação de mecanismos de
proteção sobre dados fictícios, além de estabelecer os requisitos
de controle de acesso para uma arquitetura em camadas.

A implementação local comprova as transformações de dados, enquanto
os controles de autorização, auditoria e retenção são documentados
como requisitos para uma implantação corporativa.

Essa distinção evita apresentar controles conceituais como
mecanismos de segurança efetivamente implementados.