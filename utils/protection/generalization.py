"""
Data Generalization
===================

Provides generalization functions used to reduce data
granularity while preserving analytical usefulness.
"""

from datetime import date, datetime
from typing import Optional

import pandas as pd


# AGE RANGE

def generalize_age(
    birth_date: object,
) -> Optional[str]:
    """
    Converts a birth date into an age range.
    """

    if pd.isna(birth_date):
        return None

    if isinstance(birth_date, datetime):
        birth_date = birth_date.date()

    today = date.today()

    age = (
        today.year
        - birth_date.year
        - (
            (today.month, today.day)
            < (birth_date.month, birth_date.day)
        )
    )

    if age < 25:
        return "18-24"

    if age < 35:
        return "25-34"

    if age < 45:
        return "35-44"

    if age < 55:
        return "45-54"

    if age < 65:
        return "55-64"

    return "65+"


# CEP REGION

def generalize_cep(
    cep: object,
) -> Optional[str]:
    """
    Reduces CEP granularity by retaining only
    the first five digits.
    """

    if pd.isna(cep):
        return None

    normalized_cep = (
        str(cep)
        .replace("-", "")
        .replace(".", "")
        .strip()
    )

    return normalized_cep[:5]


# INCOME RANGE

def generalize_income(
    income: object,
) -> Optional[str]:
    """
    Converts exact monthly income into an income range.
    """

    if pd.isna(income):
        return None

    income = float(income)

    if income <= 3_000:
        return "Até 3.000"

    if income <= 5_000:
        return "3.001-5.000"

    if income <= 10_000:
        return "5.001-10.000"

    if income <= 20_000:
        return "10.001-20.000"

    return "Acima de 20.000"