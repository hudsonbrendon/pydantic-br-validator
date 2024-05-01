from ..validators.rg_validator import RGValidator
from .base_field import Base, BaseDigits, BaseMask

__all__ = [
    "RG",
    "RGMask",
    "RGDigits",
]


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
