import re

import pytest
from faker import Faker
from pydantic import BaseModel, ValidationError

from pydantic_br_validator import (
    CNPJ,
    CNPJDigits,
    CNPJMask,
    FieldDigitError,
    FieldInvalidError,
    FieldMaskError,
    FieldTypeError,
)

TOTAL_CNPJ = 10
fake = Faker("pt-BR")


def _get_char_value(char: str) -> int:
    """Retorna o valor do caractere para cálculo do DV (ASCII - 48)."""
    return ord(char.upper()) - 48


def generate_alphanumeric_cnpj(base: str) -> str:
    """
    Gera um CNPJ alfanumérico válido a partir de uma base de 12 caracteres.
    Calcula os dígitos verificadores corretamente.
    """
    base = base.upper()[:12]

    # Calcula primeiro dígito verificador
    weight1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    total1 = sum(_get_char_value(base[i]) * weight1[i] for i in range(12))
    check1 = total1 % 11
    first_digit = "0" if check1 < 2 else str(11 - check1)

    # Calcula segundo dígito verificador
    base_with_first = base + first_digit
    weight2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    total2 = sum(_get_char_value(base_with_first[i]) * weight2[i] for i in range(13))
    check2 = total2 % 11
    second_digit = "0" if check2 < 2 else str(11 - check2)

    return base + first_digit + second_digit


# CNPJs alfanuméricos válidos para testes
VALID_ALPHANUMERIC_CNPJS = [
    generate_alphanumeric_cnpj("12ABC34501DE"),
    generate_alphanumeric_cnpj("ABCD12340001"),
    generate_alphanumeric_cnpj("1A2B3C4D0001"),
    generate_alphanumeric_cnpj("ZZZZZZZZ0001"),
    generate_alphanumeric_cnpj("A1B2C3D40001"),
]


def cnpj_digits():
    cnpjs = [re.sub("[^0-9]", "", fake.cnpj()) for _ in range(TOTAL_CNPJ)]
    return cnpjs


def cnpj_mask():
    cnpjs = [fake.cnpj() for _ in range(TOTAL_CNPJ)]
    return cnpjs


def cnpj_mixed():
    cnpjs = [fake.cnpj() for _ in range(int(TOTAL_CNPJ / 2))]
    cnpjs += [re.sub("[^0-9]", "", fake.cnpj()) for _ in range(int(TOTAL_CNPJ / 2))]
    return cnpjs


@pytest.fixture
def company():
    class Company(BaseModel):
        cnpj: CNPJ

    yield Company


@pytest.fixture
def company_masks():
    class Company(BaseModel):
        cnpj: CNPJMask

    yield Company


@pytest.fixture
def company_digits():
    class Company(BaseModel):
        cnpj: CNPJDigits

    yield Company


@pytest.mark.parametrize("cnpj", cnpj_mixed())
def test_must_be_string(company, cnpj):
    c1 = company(cnpj=cnpj)
    assert isinstance(c1.cnpj, str)


@pytest.mark.parametrize("cnpj", cnpj_mask())
def test_mascara_must_be_string(company_masks, cnpj):
    c1 = company_masks(cnpj=cnpj)
    assert isinstance(c1.cnpj, str)


@pytest.mark.parametrize("cnpj", cnpj_digits())
def test_digits_must_be_string(company_digits, cnpj):
    c1 = company_digits(cnpj=cnpj)
    assert isinstance(c1.cnpj, str)


@pytest.mark.parametrize("cnpj", cnpj_mask())
def test_must_accept_with_mask(company_masks, cnpj):
    c1 = company_masks(cnpj=cnpj)
    assert c1.cnpj == cnpj


@pytest.mark.parametrize("cnpj", cnpj_digits())
def test_must_accept_only_numbers(company_digits, cnpj):
    c1 = company_digits(cnpj=cnpj)
    assert c1.cnpj == cnpj


@pytest.mark.parametrize("cnpj", cnpj_digits())
def test_must_fail_when_use_digits_in_mask_class(company_masks, cnpj):
    with pytest.raises(ValidationError) as e:
        company_masks(cnpj=cnpj)
    assert FieldMaskError.msg_template in str(e.value)


@pytest.mark.parametrize("cnpj", cnpj_mask())
def test_must_fail_when_use_mask_in_digits_class(company_digits, cnpj):
    with pytest.raises(ValidationError) as e:
        company_digits(cnpj=cnpj)
    assert FieldDigitError.msg_template in str(e.value)


@pytest.mark.parametrize("cnpj", cnpj_digits())
def test_must_fail_when_use_another_type(company_digits, cnpj):
    with pytest.raises(ValidationError) as e:
        company_digits(cnpj=int(cnpj))
    assert FieldTypeError.msg_template in str(e.value)


@pytest.mark.parametrize("cnpj", cnpj_digits())
def test_must_fail_when_use_invalid_cnpjs(company, cnpj):
    with pytest.raises(ValidationError) as e:
        company(cnpj=cnpj[-1])
    assert FieldInvalidError.msg_template in str(e.value)


@pytest.mark.parametrize("cnpj", cnpj_mixed())
def test_must_fail_when_use_digits_cont_above_cnpjs(company, cnpj):
    with pytest.raises(ValidationError) as e:
        company(cnpj=cnpj * 2)
    assert FieldInvalidError.msg_template in str(e.value)


@pytest.mark.parametrize("cnpj", cnpj_mixed())
def test_must_fail_when_use_digits_cont_below_cnpjs(company, cnpj):
    with pytest.raises(ValidationError) as e:
        company(cnpj=cnpj[:5])
    assert FieldInvalidError.msg_template in str(e.value)


# Testes para CNPJ Alfanumérico
@pytest.mark.parametrize("cnpj", VALID_ALPHANUMERIC_CNPJS)
def test_alphanumeric_cnpj_must_be_valid(company, cnpj):
    """Testa que CNPJs alfanuméricos válidos são aceitos."""
    c1 = company(cnpj=cnpj)
    assert isinstance(c1.cnpj, str)
    assert c1.cnpj == cnpj


@pytest.mark.parametrize("cnpj", VALID_ALPHANUMERIC_CNPJS)
def test_alphanumeric_cnpj_digits_must_be_valid(company_digits, cnpj):
    """Testa que CNPJs alfanuméricos são aceitos no campo CNPJDigits."""
    c1 = company_digits(cnpj=cnpj)
    assert isinstance(c1.cnpj, str)
    assert c1.cnpj == cnpj


def test_alphanumeric_cnpj_with_mask_must_be_valid(company_masks):
    """Testa CNPJ alfanumérico com máscara."""
    cnpj_base = generate_alphanumeric_cnpj("12ABC34501DE")
    cnpj_with_mask = f"{cnpj_base[:2]}.{cnpj_base[2:5]}.{cnpj_base[5:8]}/{cnpj_base[8:12]}-{cnpj_base[12:14]}"
    c1 = company_masks(cnpj=cnpj_with_mask)
    assert isinstance(c1.cnpj, str)


def test_alphanumeric_cnpj_lowercase_must_be_valid(company):
    """Testa que CNPJs alfanuméricos em minúsculas são aceitos e normalizados."""
    cnpj_base = generate_alphanumeric_cnpj("12ABC34501DE")
    c1 = company(cnpj=cnpj_base.lower())
    assert isinstance(c1.cnpj, str)


def test_alphanumeric_cnpj_invalid_check_digit_must_fail(company):
    """Testa que CNPJs alfanuméricos com dígito verificador inválido são rejeitados."""
    invalid_cnpj = "12ABC34501DE99"  # Dígitos verificadores inválidos
    with pytest.raises(ValidationError) as e:
        company(cnpj=invalid_cnpj)
    assert FieldInvalidError.msg_template in str(e.value)


def test_alphanumeric_cnpj_with_special_chars_must_fail(company_digits):
    """Testa que CNPJs com caracteres especiais são rejeitados no campo CNPJDigits."""
    with pytest.raises(ValidationError) as e:
        company_digits(cnpj="12ABC345@1DE00")
    assert FieldDigitError.msg_template in str(e.value)


def test_mixed_numeric_and_alphanumeric_cnpj(company):
    """Testa que tanto CNPJs numéricos quanto alfanuméricos são aceitos."""
    # CNPJ numérico tradicional (gerado pelo faker)
    numeric_cnpj = re.sub("[^0-9]", "", fake.cnpj())
    c1 = company(cnpj=numeric_cnpj)
    assert isinstance(c1.cnpj, str)

    # CNPJ alfanumérico
    alphanumeric_cnpj = generate_alphanumeric_cnpj("ABCD12340001")
    c2 = company(cnpj=alphanumeric_cnpj)
    assert isinstance(c2.cnpj, str)
