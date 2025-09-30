import re

import pytest
from faker import Faker
from pydantic import BaseModel, ValidationError

from pydantic_br_validator import (
    RG,
    FieldDigitError,
    FieldInvalidError,
    FieldMaskError,
    FieldTypeError,
    RGDigits,
    RGMask,
)

TOTAL_RG = 10
fake = Faker("pt-BR")


def format_rg_mask(rg: str) -> str:
    """Formata um RG sem máscara para o formato XX.XXX.XXX-X"""
    rg_clean = re.sub("[^0-9X]", "", rg)
    if len(rg_clean) == 9:
        return f"{rg_clean[:2]}.{rg_clean[2:5]}.{rg_clean[5:8]}-{rg_clean[8]}"
    elif len(rg_clean) == 8:
        return f"{rg_clean[:2]}.{rg_clean[2:5]}.{rg_clean[5:7]}-{rg_clean[7]}"
    return rg


def rg_digits():
    rgs = []
    while len(rgs) < TOTAL_RG:
        rg = re.sub("[^0-9X]", "", fake.rg())
        # Filtra RGs com 'X' para retornar apenas dígitos
        if "X" not in rg:
            rgs.append(rg)
    return rgs


def rg_mask():
    rgs = []
    while len(rgs) < TOTAL_RG:
        rg_raw = fake.rg()
        # Filtra RGs com 'X' para evitar problemas de validação
        if "X" not in rg_raw:
            rgs.append(format_rg_mask(rg_raw))
    return rgs


def rg_mixed():
    rgs = []
    # Metade com máscara
    while len(rgs) < int(TOTAL_RG / 2):
        rg_raw = fake.rg()
        if "X" not in rg_raw:
            rgs.append(format_rg_mask(rg_raw))
    # Metade sem máscara
    while len(rgs) < TOTAL_RG:
        rg = re.sub("[^0-9X]", "", fake.rg())
        if "X" not in rg:
            rgs.append(rg)
    return rgs


@pytest.fixture
def person():
    class Person(BaseModel):
        rg: RG

    yield Person


@pytest.fixture
def person_masks():
    class Person(BaseModel):
        rg: RGMask

    yield Person


@pytest.fixture
def person_digits():
    class Person(BaseModel):
        rg: RGDigits

    yield Person


@pytest.mark.parametrize("rg", rg_mixed())
def test_must_be_string(person, rg):
    p1 = person(rg=rg)
    assert isinstance(p1.rg, str)


@pytest.mark.parametrize("rg", rg_mask())
def test_mascara_must_be_string(person_masks, rg):
    p1 = person_masks(rg=rg)
    assert isinstance(p1.rg, str)


@pytest.mark.parametrize("rg", rg_digits())
def test_digits_must_be_string(person_digits, rg):
    p1 = person_digits(rg=rg)
    assert isinstance(p1.rg, str)


@pytest.mark.parametrize("rg", rg_mask())
def test_must_accept_with_mask(person_masks, rg):
    p1 = person_masks(rg=rg)
    assert p1.rg == rg


@pytest.mark.parametrize("rg", rg_digits())
def test_must_accept_only_numbers(person_digits, rg):
    p1 = person_digits(rg=rg)
    assert p1.rg == rg


@pytest.mark.parametrize("rg", rg_digits())
def test_must_fail_when_use_digits_in_mask_class(person_masks, rg):
    with pytest.raises(ValidationError) as e:
        person_masks(rg=rg)
    assert FieldMaskError.msg_template in str(e.value)


@pytest.mark.parametrize("rg", rg_mask())
def test_must_fail_when_use_mask_in_digits_class(person_digits, rg):
    with pytest.raises(ValidationError) as e:
        person_digits(rg=rg)
    assert FieldDigitError.msg_template in str(e.value)


@pytest.mark.parametrize("rg", rg_digits())
def test_must_fail_when_use_another_type(person_digits, rg):
    with pytest.raises(ValidationError) as e:
        person_digits(rg=int(rg.replace("X", "0")))
    assert FieldTypeError.msg_template in str(e.value)


@pytest.mark.parametrize("rg", rg_digits())
def test_must_fail_when_use_invalid_rgs(person, rg):
    with pytest.raises(ValidationError) as e:
        person(rg=rg[-1])
    assert FieldInvalidError.msg_template in str(e.value)


@pytest.mark.parametrize("rg", rg_mixed())
def test_must_fail_when_use_digits_count_above_rgs(person, rg):
    with pytest.raises(ValidationError) as e:
        person(rg=rg * 2)
    assert FieldInvalidError.msg_template in str(e.value)


@pytest.mark.parametrize("rg", rg_mixed())
def test_must_fail_when_use_digits_count_below_rgs(person, rg):
    with pytest.raises(ValidationError) as e:
        person(rg=rg[:5])
    assert FieldInvalidError.msg_template in str(e.value)
