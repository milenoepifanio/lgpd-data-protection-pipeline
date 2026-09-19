import random

from faker import Faker

from utils.config import SEED
from utils.domains import (
    BLOOD_TYPES,
    BRAZILIAN_STATES,
    ETHNICITY,
    GENDERS,
    HEALTH_CONDITIONS,
    MARITAL_STATUS,
    PREFERRED_CHANNELS,
    PROFESSIONS,
)


# INITIALIZATION

random.seed(SEED)

fake = Faker("pt_BR")
Faker.seed(SEED)


# FIELD GENERATORS
def generate_cpf() -> str:
    """
    Generates a synthetic CPF.
    """

    return fake.cpf()


def generate_income() -> float:
    """
    Generates a fictitious monthly income using a triangular
    distribution.
    """

    return round(
        random.triangular(
            low=1_500,
            high=30_000,
            mode=5_000,
        ),
        2,
    )


# CUSTOMER GENERATOR
def generate_customer() -> dict:
    """
    Generates one synthetic customer record.
    """

    birth_date = fake.date_of_birth(
        minimum_age=18,
        maximum_age=85,
    )

    registration_date = fake.date_between(
        start_date="-5y",
        end_date="today",
    )

    consent_marketing = random.choice(
        [True, False]
    )

    consent_date = (
        fake.date_between(
            start_date=registration_date,
            end_date="today",
        )
        if consent_marketing
        else None
    )

    last_purchase = fake.date_between(
        start_date=registration_date,
        end_date="today",
    )

    purchase_quantity = random.randint(
        1,
        100,
    )

    total_purchase_value = round(
        random.uniform(
            100,
            50_000,
        ),
        2,
    )

    return {
        "customer_id": fake.uuid4(),
        "nome": fake.name(),
        "cpf": generate_cpf(),
        "email": fake.email(),
        "telefone": fake.phone_number(),
        "data_nascimento": birth_date,
        "sexo": random.choice(GENDERS),
        "raca_etnia": random.choice(ETHNICITY),
        "cidade": fake.city(),
        "estado": random.choice(BRAZILIAN_STATES),
        "cep": fake.postcode(),
        "profissao": random.choice(PROFESSIONS),
        "renda_mensal": generate_income(),
        "estado_civil": random.choice(MARITAL_STATUS),
        "possui_filhos": random.choice([True, False]),
        "condicao_saude": random.choice(HEALTH_CONDITIONS),
        "tipo_sanguineo": random.choice(BLOOD_TYPES),
        "consentimento_marketing": consent_marketing,
        "data_consentimento": consent_date,
        "data_cadastro": registration_date,
        "ultima_compra": last_purchase,
        "quantidade_compras": purchase_quantity,
        "valor_total_compras": total_purchase_value,
        "canal_preferido": random.choice(PREFERRED_CHANNELS),
    }