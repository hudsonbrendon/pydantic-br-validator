import pytest
from pydantic import BaseModel, ValidationError

from pydantic_br_validator import (
    CEP,
    CEPDigits,
    CEPMask,
)
from pydantic_br_validator.field_erros import FieldInvalidError, FieldTypeError

cep_mock = [
    ("59151650", "59151-650", "59151650"),
    ("57602660", "57602-660", "57602660"),
    ("78735819", "78735-819", "78735819"),
    ("69315235", "69315-235", "69315235"),
    ("15056133", "15056-133", "15056133"),
    ("60761971", "60761-971", "60761971"),
    ("72760022", "72760-022", "72760022"),
    ("79020160", "79020-160", "79020160"),
    ("64040670", "64040-670", "64040670"),
    ("76965520", "76965-520", "76965520"),
]


@pytest.fixture
def address():
    class Address(BaseModel):
        cep: CEP
        cep_mask: CEPMask
        cep_digits: CEPDigits

    yield Address


@pytest.mark.parametrize("cep, cep_mask, cep_digits", cep_mock)
def test_must_cep_string(address, cep, cep_mask, cep_digits):
    address_1 = address(cep=cep, cep_mask=cep_mask, cep_digits=cep_digits)
    assert isinstance(address_1.cep, str)
    assert isinstance(address_1.cep_mask, str)
    assert isinstance(address_1.cep_digits, str)


@pytest.mark.parametrize("cep, cep_mask, cep_digits", cep_mock)
def test_must_accept_only_numbers(address, cep, cep_mask, cep_digits):
    address_1 = address(cep=cep, cep_mask=cep_mask, cep_digits=cep_digits)
    assert address_1.cep == cep
    assert address_1.cep_mask == cep_mask
    assert address_1.cep_digits == cep_digits


@pytest.mark.parametrize("cep, cep_mask, cep_digits", cep_mock)
def test_must_fail_when_use_another_type(address, cep, cep_mask, cep_digits):
    with pytest.raises(ValidationError) as e:
        address(
            cep=int(cep),
            cep_mask=str(cep_mask),
            cep_digits=int(cep_digits),
        )
    assert FieldTypeError.msg_template in str(e.value)


@pytest.mark.parametrize("cep, cep_mask, cep_digits", cep_mock)
def test_must_fail_when_use_invalid_cep(address, cep, cep_mask, cep_digits):
    with pytest.raises(ValidationError) as e:
        invalid_cep = cep[:5] + cep[6:]
        invalid_cep_mask = cep_mask[:5] + cep_mask[6:]
        invalid_cep_digits = cep_digits[:5] + cep_digits[6:]
        address(
            cep=invalid_cep,
            cep_mask=invalid_cep_mask,
            cep_digits=invalid_cep_digits,
        )
    assert FieldInvalidError.msg_template in str(e.value)


@pytest.mark.parametrize("cep, cep_mask, cep_digits", cep_mock)
def test_must_fail_when_use_digits_count_above_cep(address, cep, cep_mask, cep_digits):
    with pytest.raises(ValidationError) as e:
        address(cep=cep * 2, cep_mask=cep_mask * 2, cep_digits=cep_digits * 2)
    assert FieldInvalidError.msg_template in str(e.value)


@pytest.mark.parametrize("cep, cep_mask, cep_digits", cep_mock)
def test_must_fail_when_use_digits_count_below_cep(address, cep, cep_mask, cep_digits):
    with pytest.raises(ValidationError) as e:
        address(cep=cep[:5], cep_mask=cep_mask[:5], cep_digits=cep_digits[:5])
    assert FieldInvalidError.msg_template in str(e.value)


@pytest.mark.parametrize(
    "cep, cep_mask, cep_digits",
    [
        ("000000000000", "00000-000", "00000000"),
        ("111111111111", "11111-111", "11111111"),
        ("222222222222", "22222-222", "22222222"),
        ("333333333333", "33333-333", "33333333"),
        ("444444444444", "44444-444", "44444444"),
        ("555555555555", "55555-555", "55555555"),
        ("666666666666", "66666-666", "66666666"),
        ("777777777777", "77777-777", "77777777"),
        ("888888888888", "88888-888", "88888888"),
        ("999999999999", "99999-999", "99999999"),
    ],
)
def test_must_fail_when_use_sequecial_digits(address, cep, cep_mask, cep_digits):
    with pytest.raises(ValidationError) as e:
        address(
            cep=cep,
            cep_mask=cep_mask,
            cep_digits=cep_digits,
        )
    assert FieldInvalidError.msg_template in str(e.value)
