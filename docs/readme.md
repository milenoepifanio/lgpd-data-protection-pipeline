 # Documentação do Projeto LGPD

Repositório central da documentação de arquitetura, classificação,
proteção, governança, validação e disponibilização analítica do projeto.

O projeto utiliza dados sintéticos de clientes e demonstra um pipeline
de Engenharia de Dados orientado pelos princípios de minimização,
pseudonimização, generalização, controle de acesso e rastreabilidade.

| Área | Conteúdo |
| --- | --- |
| [Arquitetura](./architecture.md) | Visão geral da solução, camadas, responsabilidades e fluxo técnico. |
| [Controle de acesso](./access-control.md) | Classificação das camadas, perfis de acesso e requisitos de segurança. |
| [Classificação de dados](./data-classification.md) | Classificação de dados pessoais e sensíveis e requisitos de proteção. |
| [Regras de proteção](./protection-rules.md) | Remoção, generalização, pseudonimização e rastreabilidade dos dados. |
| [Regras da Silver](./silver-rules.md) | Seleção de atributos, padronização, validações e métricas derivadas. |
| [Regras da Analytics](./analytics-rules.md) | Produtos agregados, métricas, dimensões e regras de divulgação. |
| [Evidências do PDI](./pdi-evidence.md) | Atividades, resultados e evidências produzidas durante o projeto. |

## Estrutura

```text
docs/
├── readme.md
├── architecture.md
├── access-control.md
├── data-classification.md
├── protection-rules.md
├── silver-rules.md
├── analytics-rules.md
└── pdi-evidence.md
```

## Fluxo documentado

```text
Raw Restrita
	├── Proteção ──> Protected ──> Silver ──> Analytics
	└── Rastreamento restrito: customer_identity_map.parquet
```

## Objetivo

Centralizar a documentação técnica e de governança do projeto, separando
arquitetura, classificação, execução das transformações, regras de acesso,
validação e evidências de aprendizagem.

O dataset é sintético e foi criado exclusivamente para fins educacionais.
A camada `data/restricted/` contém dados pessoais completos para
rastreabilidade autorizada e deve receber controles de acesso mais rígidos
que as camadas `Protected`, `Silver` e `Analytics`.

## Ordem sugerida de leitura

1. [Arquitetura](./architecture.md)
2. [Classificação de dados](./data-classification.md)
3. [Regras de proteção](./protection-rules.md)
4. [Controle de acesso](./access-control.md)
5. [Regras da Silver](./silver-rules.md)
6. [Regras da Analytics](./analytics-rules.md)
7. [Evidências do PDI](./pdi-evidence.md)
