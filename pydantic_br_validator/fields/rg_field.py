from typing import Any, Callable, Generator

from ..field_erros import FieldDigitError, FieldInvalidError, RGDigitError
from ..get_versions import get_pydantic_version
from ..validators.rg_validator import RGValidator
from .base_field import Base, BaseDigits, BaseMask

__all__ = [
    "RG",
    "RGMask",
    "RGDigits",
]

AnyCallable = Callable[..., Any]
CallableGenerator = Generator[AnyCallable, None, None]

pydantic_version = get_pydantic_version()


class RG(Base):
    """
    Accepts string of RG with or without mask.

    Attributes:
        number (str): RG number.

    """

    format = "rg"
    Validator = RGValidator


class RGMask(BaseMask):
    """
    Only Accepts string of RG with mask.

    Attributes:
        number (str): RG number.
    """

    format = "rg mask"
    Validator = RGValidator


class RGDigits(BaseDigits):
    """
    Only Accepts string of RG with digits.

    Attributes:
        number (str): RG number.
    """

    format = "rg digits"
    Validator = RGValidator

    @classmethod
    def __get_validators__(cls) -> CallableGenerator:
        yield cls.validate_type
        yield cls.validate_rg_digits
        yield cls.validate

    @classmethod
    def validate_rg_digits(cls, value: str) -> str:
        # First check if it contains mask characters (should fail with FieldDigitError)
        if "." in value or "-" in value:
            if pydantic_version.value == 1:
                raise FieldDigitError()
            if pydantic_version.value == 2:
                raise FieldDigitError(FieldDigitError.msg_template)

        # Special case for RG: Allow 'X' only in the last position
        if len(value) != 9:
            if pydantic_version.value == 1:
                raise FieldInvalidError()
            if pydantic_version.value == 2:
                raise FieldInvalidError(FieldInvalidError.msg_template)

        # Check if all characters except the last one are digits
        if not value[:-1].isdigit():
            if pydantic_version.value == 1:
                raise RGDigitError()
            if pydantic_version.value == 2:
                raise RGDigitError(RGDigitError.msg_template)

        # Check if the last character is a digit or 'X'
        if not (value[-1].isdigit() or value[-1] == "X"):
            if pydantic_version.value == 1:
                raise RGDigitError()
            if pydantic_version.value == 2:
                raise RGDigitError(RGDigitError.msg_template)

        return value
