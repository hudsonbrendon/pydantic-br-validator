from ..validators.cnpj_validator import CNPJValidator
from .base_field import Base, BaseAlphanumeric, BaseMask

__all__ = [
    "CNPJ",
    "CNPJMask",
    "CNPJDigits",
]


class CNPJ(Base):
    """
    Accepts string of CNPJ with or without mask.
    Supports both numeric and alphanumeric CNPJ formats.

    Attributes:
        number (str): CNPJ number.

    """

    format = "cnpj"
    Validator = CNPJValidator


class CNPJMask(BaseMask):
    """
    Only Accepts string of CNPJ with mask.
    Supports both numeric and alphanumeric CNPJ formats.

    Attributes:
        number (str): CNPJ number.
    """

    format = "cnpj"
    Validator = CNPJValidator


class CNPJDigits(BaseAlphanumeric):
    """
    Only Accepts string of CNPJ without mask (digits/alphanumeric only).
    Supports both numeric and alphanumeric CNPJ formats.

    Attributes:
        number (str): CNPJ number.
    """

    format = "cnpj"
    Validator = CNPJValidator
