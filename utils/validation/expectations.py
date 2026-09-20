"""
Protected Layer Expectations
============================

Defines Great Expectations rules for the Protected
customer dataset.
"""

import great_expectations as gx


def build_protected_expectation_suite(
    expected_columns: list[str],
) -> gx.ExpectationSuite:
    """
    Creates the Expectation Suite for the Protected layer.
    """

    suite = gx.ExpectationSuite(
        name="protected_customers_suite"
    )

    # --------------------------------------------------------
    # Schema
    # --------------------------------------------------------

    suite.add_expectation(
        gx.expectations.ExpectTableColumnsToMatchOrderedList(
            column_list=expected_columns,
        )
    )

    # --------------------------------------------------------
    # Customer ID
    # --------------------------------------------------------

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="customer_id",
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeUnique(
            column="customer_id",
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToMatchRegex(
            column="customer_id",
            regex=r"^[a-f0-9]{64}$",
        )
    )

    # --------------------------------------------------------
    # Generalized age
    # --------------------------------------------------------

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="faixa_etaria",
            value_set=[
                "18-24",
                "25-34",
                "35-44",
                "45-54",
                "55-64",
                "65+",
            ],
        )
    )

    # --------------------------------------------------------
    # Generalized income
    # --------------------------------------------------------

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="faixa_renda",
            value_set=[
                "Até 3.000",
                "3.001-5.000",
                "5.001-10.000",
                "10.001-20.000",
                "Acima de 20.000",
            ],
        )
    )

    # --------------------------------------------------------
    # CEP region
    # --------------------------------------------------------

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToMatchRegex(
            column="regiao_cep",
            regex=r"^\d{5}$",
        )
    )

    return suite