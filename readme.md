# Projeto LGPD

Pipeline educacional de Engenharia de Dados para demonstrar classificação, proteção, validação e disponibilização analítica de dados conforme conceitos da Lei Geral de Proteção de Dados (LGPD).

O projeto utiliza uma base sintética de clientes de e-commerce e arquivos Parquet organizados em camadas:

```text
Raw Restrita -> Protected -> Silver -> Analytics
```

Nenhum dado pessoal real é necessário para executar o projeto.

## Objetivos

- Gerar dados sintéticos para estudo.
- Classificar colunas conforme a política de dados do projeto.
- Aplicar minimização, generalização e pseudonimização.
- Validar as transformações realizadas na camada Protected.
- Preparar a camada Silver para consumo analítico.
- Criar produtos analíticos agregados sem identificadores individuais.

## Estrutura

```text
config/       Política de classificação e proteção
data/raw/     Dataset sintético original
data/protected/ Dataset com as proteções aplicadas
data/silver/  Dataset preparado para análise
data/analytics/ Produtos analíticos agregados
docs/         Arquitetura e regras das camadas
notebooks/    Consultas e validações exploratórias
src/          Scripts executáveis do pipeline
tests/        Testes automatizados
utils/        Regras e componentes reutilizáveis
```

## Requisitos

- Python 3.10 ou superior
- `pip`
- PowerShell, Terminal ou shell compatível

As dependências estão em [requirements.txt](requirements.txt): pandas, PyArrow, Faker, PyYAML, python-dotenv e Great Expectations.

## Instalação

Clone o repositório, acesse a pasta do projeto e crie um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Para shells Unix, a ativação pode ser feita com:

```bash
source .venv/bin/activate
```

## Configuração

O processo de proteção utiliza uma chave para pseudonimização com HMAC-SHA256. Copie o arquivo de exemplo e defina uma chave local:

```powershell
Copy-Item .env.example .env
```

No arquivo `.env`, configure:

```text
PSEUDONYMIZATION_KEY=uma-chave-local-forte
```

Não versione `.env` nem compartilhe a chave. A mesma chave deve ser utilizada quando for necessário reproduzir os identificadores pseudonimizados.

## Execução do pipeline

Execute os módulos a partir da raiz do projeto, na ordem abaixo. O uso de `-m` mantém os imports internos do projeto funcionando corretamente:

### 1. Gerar dados sintéticos

```powershell
python -m src.generate_data
```

Saída: `data/raw/customers.parquet`.

### 2. Validar a classificação

```powershell
python -m src.classify_data
```

O script verifica se todas as colunas possuem classificação, nível de proteção, necessidade analítica e ação de proteção válidos.

### 3. Aplicar a proteção

```powershell
python -m src.protect_data
```

Saída: `data/protected/customers.parquet`.

As transformações podem incluir remoção de atributos, generalização e pseudonimização. A camada Protected ainda pode conter dados pessoais pseudonimizados e não deve ser tratada como anonimizada.

### 4. Validar a proteção

```powershell
python -m src.validate_protection
```

O processo compara as camadas Raw e Protected e executa as validações de qualidade configuradas.

### 5. Construir a camada Silver

```powershell
python -m src.build_silver
```

Saída: `data/silver/customers.parquet`.

### 6. Construir a camada Analytics

```powershell
python -m src.build_analytics
```

Saídas em `data/analytics/`, com agregações por estado, faixa etária, faixa de renda e canal preferido.

## Testes

Execute os testes com:

```powershell
pytest
```

Também é possível consultar a camada protegida pelo notebook [query_protected_validate.ipynb](notebooks/query_protected_validate.ipynb).

## Documentação

- [Arquitetura](docs/architecture.md)
- [Regras de classificação](docs/data-classification.md)
- [Regras de proteção](docs/protection-rules.md)
- [Regras da camada Silver](docs/silver-rules.md)
- [Regras da camada Analytics](docs/analytics-rules.md)
- [Evidências do PDI](docs/pdi-evidence.md)
- [Guia de contribuição](contributing)
- [Política de segurança](security.md)
- [Código de conduta](code_of_conduct.md)
- [Licença](license)

## Privacidade e segurança

Este projeto é demonstrativo e não substitui uma avaliação de segurança, privacidade ou conformidade para produção. Use somente dados sintéticos ou devidamente anonimizados, mantenha os segredos fora do controle de versão e aplique controles de acesso adequados ao ambiente real.

## Licença

Distribuído sob a [Licença MIT](license).
