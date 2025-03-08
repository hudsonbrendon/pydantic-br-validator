import re

from .base_validator import FieldMaskValidator

__all__ = ["RGValidator"]


class RGValidator(FieldMaskValidator):
    def __init__(self, rg: str) -> None:
        self.rg = rg

    def validate_mask(self) -> bool:
        """Valida se o RG tem a máscara correta (XX.XXX.XXX-X)."""
        if len(self.rg) != 12:
            return False

        mask_pattern = r"^\d{2}\.\d{3}\.\d{3}-[\dX]$"
        return bool(re.match(mask_pattern, self.rg))

    def validate(self) -> bool:
        """Valida se o RG tem 9 caracteres numéricos, permitindo máscara."""
        rg_clean = self.rg.replace(".", "").replace("-", "")

        # Check if it has a valid length
        if len(rg_clean) != 9:
            return False

        # Check if it has all repeated digits
        if len(set(rg_clean)) == 1:
            return False

        # Accept both digits and 'X' in the last position
        if not rg_clean[:-1].isdigit():
            return False

        if not (rg_clean[-1].isdigit() or rg_clean[-1] == "X"):
            return False

        # If it's a masked format, validate the mask
        if "." in self.rg and "-" in self.rg:
            return self.validate_mask()

        return True

    def _validate_digit_verify(self, rg: str) -> str:
        """Valida o dígito verificador do RG."""
        sum = 0
        for i in range(8):
            sum += int(rg[i]) * (9 - i)

        check_digit = sum % 11
        if check_digit == 10:
            return "X"
        return str(check_digit)
