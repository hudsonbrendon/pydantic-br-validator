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


def generate_valid_rg():
    """Generate a valid RG with 9 digits."""
    # Since Faker doesn't have a built-in RG generator,
    # we'll create a simple function that generates valid formatted RGs
    rg_digits = "".join([str(fake.random_digit()) for _ in range(8)])
    # Calculate check digit (simple example - actual calculation may vary by state)
    sum_digits = sum(int(d) * (9 - i) for i, d in enumerate(rg_digits))
    check_digit = str(sum_digits % 11)
    if check_digit == "10":
        check_digit = "X"
    return rg_digits + check_digit


def rg_digits():
    """Generate RG numbers without mask."""
    rgs = [generate_valid_rg() for _ in range(TOTAL_RG)]
    return rgs


def rg_mask():
    """Generate RG numbers with mask."""
    rgs = []
    for _ in range(TOTAL_RG):
        rg = generate_valid_rg()
        # Format as XX.XXX.XXX-X
        formatted_rg = f"{rg[:2]}.{rg[2:5]}.{rg[5:8]}-{rg[8]}"
        rgs.append(formatted_rg)
    return rgs


def rg_mixed():
    """Generate a mix of RG numbers with and without masks."""
    rgs = rg_mask()[: int(TOTAL_RG / 2)]
    rgs += rg_digits()[: int(TOTAL_RG / 2)]
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
        person_digits(rg=int(re.sub(r"[^0-9]", "", rg)))
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


@pytest.mark.parametrize(
    "rg",
    [
        "000000000",
        "111111111",
        "222222222",
        "333333333",
        "444444444",
        "555555555",
        "666666666",
        "777777777",
        "888888888",
        "999999999",
    ],
)
def test_must_fail_when_use_sequecial_digits(person, rg):
    with pytest.raises(ValidationError) as e:
        person(rg=rg)
    assert FieldInvalidError.msg_template in str(e.value)
