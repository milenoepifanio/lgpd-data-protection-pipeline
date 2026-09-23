
"""
Analytics Layer Definitions
===========================

Defines the analytical products and disclosure requirements.
"""

# ANALYTICAL PRODUCTS

ANALYTICS_PRODUCTS = {
    "customers_by_health_condition": [
        "condicao_saude",
    ],
    "customers_by_state": [
        "condicao_saude",
        "estado",
    ],
    "customers_by_age": [
        "condicao_saude",
        "faixa_etaria",
    ],
    "customers_by_income": [
        "condicao_saude",
        "faixa_renda",
    ],
    "customers_by_channel": [
        "condicao_saude",
        "canal_preferido",
    ],
}


# REQUIRED SILVER COLUMNS

REQUIRED_COLUMNS = [
    "customer_id",
    "condicao_saude",
    "estado",
    "faixa_etaria",
    "faixa_renda",
    "canal_preferido",
    "quantidade_compras",
    "valor_total_compras",
]


# DISCLOSURE POLICY

MIN_GROUP_SIZE = 10


# HEALTH ANALYTICS COHORT

TARGET_HEALTH_CONDITIONS = frozenset(
    {
        "Diabetes",
        "Hipertensão",
        "Obesidade",
    }
)


# ANALYTICAL METRICS

METRIC_COLUMNS = [
    "quantidade_clientes",
    "receita_total",
    "quantidade_compras",
    "ticket_medio",
]