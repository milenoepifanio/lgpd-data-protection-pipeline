
"""
Analytics Layer Definitions
===========================

Defines the analytical products and disclosure requirements.
"""

# ============================================================
# ANALYTICAL PRODUCTS
# ============================================================

ANALYTICS_PRODUCTS = {
    "customers_by_state": "estado",
    "customers_by_age": "faixa_etaria",
    "customers_by_income": "faixa_renda",
    "customers_by_channel": "canal_preferido",
}


# ============================================================
# REQUIRED SILVER COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
    "customer_id",
    "estado",
    "faixa_etaria",
    "faixa_renda",
    "canal_preferido",
    "quantidade_compras",
    "valor_total_compras",
]


# ============================================================
# DISCLOSURE POLICY
# ============================================================

MIN_GROUP_SIZE = 10


# ============================================================
# ANALYTICAL METRICS
# ============================================================

METRIC_COLUMNS = [
    "quantidade_clientes",
    "receita_total",
    "quantidade_compras",
    "ticket_medio",
]