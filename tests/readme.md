# Testes

Esta pasta é destinada aos testes automatizados do pipeline de proteção
de dados.

## Estado atual

O arquivo `test_data_protection.py` está reservado para os testes do
projeto, mas ainda não contém casos implementados. Portanto, a execução
de `pytest` não representa atualmente uma cobertura funcional completa.

## Escopo recomendado

Os testes devem cobrir, pelo menos:

- aplicação correta das ações `retain`, `remove`, `pseudonymize` e `generalize`;
- construção do schema Protected;
- geração do mapa restrito com todas as colunas da Raw;
- correspondência entre `customer_id_protected` e o ID da Silver;
- rejeição de políticas de classificação inválidas;
- validação de regras de negócio da Silver e Analytics.

## Execução

Na raiz do projeto:

```powershell
pytest
```

Os testes devem usar dados sintéticos e fixtures temporárias, evitando
expor ou versionar os Parquets gerados no diretório `data/`.
