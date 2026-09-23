# Componentes Reutilizáveis

Esta pasta concentra as funções e regras compartilhadas pelos scripts de
execução. Os módulos são organizados por responsabilidade e não devem
conter lógica específica de um único comando quando ela puder ser
reutilizada.

## Organização

| Diretório ou módulo | Responsabilidade |
| --- | --- |
| `classification/` | Carregamento, validação e resumo da política de classificação. |
| `protection/` | Generalização, masking, pseudonimização, proteção e rastreabilidade restrita. |
| `silver/` | Definições, transformações e validações da camada Silver. |
| `analytics/` | Definições, agregações e validações dos produtos Analytics. |
| `validation/` | Comparadores e expectativas de validação da camada Protected. |
| `classification.py` | Funções legadas ou centralizadas de classificação. |
| `config.py` | Caminhos do projeto, parâmetros e arquivos de entrada e saída. |
| `dataset.py` | Geração, leitura e gravação de datasets Parquet. |
| `domains.py` | Domínios e valores permitidos usados na geração sintética. |
| `generators.py` | Geração dos atributos sintéticos dos clientes. |

## Fluxo dos componentes

```text
loader + validator
	↓
protection processor ──> restricted tracking
	↓
silver processor
	↓
analytics processor
```

Os scripts em `src/` usam esses módulos para manter a orquestração
separada das regras de transformação e validação.

## Convenções

- funções de transformação recebem e retornam `pandas.DataFrame` quando aplicável;
- caminhos e constantes compartilhados ficam em `utils/config.py`;
- regras de proteção devem seguir `config/data_classification.yaml`;
- dados restritos não devem ser impressos por funções de processamento;
- mudanças nos módulos compartilhados devem ser acompanhadas por testes.
