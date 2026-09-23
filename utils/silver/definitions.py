
"""
Silver Layer Definitions
========================

Defines the expected schema for the Silver layer.
"""

# REQUIRED INPUT COLUMNS

SILVER_COLUMNS = [
    "customer_id",
    "faixa_etaria",
    "estado",
    "faixa_renda",
    "consentimento_marketing",
    "data_consentimento",
    "data_cadastro",
    "ultima_compra",
    "quantidade_compras",
    "valor_total_compras",
    "canal_preferido",
]


# DATE COLUMNS

DATE_COLUMNS = [
    "data_consentimento",
    "data_cadastro",
    "ultima_compra",
]


# DERIVED COLUMNS

DERIVED_COLUMNS = [
    "ticket_medio",
]


# OUTPUT SCHEMA

SILVER_OUTPUT_COLUMNS = (
    SILVER_COLUMNS + DERIVED_COLUMNS
)