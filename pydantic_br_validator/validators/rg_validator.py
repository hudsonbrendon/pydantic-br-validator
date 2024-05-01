from .base_validator import FieldMaskValidator

__all__ = ["RGValidator"]


class RGValidator(FieldMaskValidator):
    def __init__(self, rg: str) -> None:
        self.rg = rg

    def validate_mask(self) -> bool:
        """Valida se o RG tem a máscara correta (XX.XXX.XXX-X)."""
        parts = self.rg.split(".")
        if len(parts) != 3:
            return False
        if not all(len(part) == 3 for part in parts[:2]) or len(parts[2]) != 3:
            return False
        if parts[2][2] != "-":
            return False
        return all(part.replace("-", "").isdigit() for part in parts)

    def validate(self) -> bool:
        """Valida se o RG tem 9 caracteres numéricos, permitindo máscara."""
        rg_clean = self.rg.replace(".", "").replace("-", "")
        if len(rg_clean) != 9:
            return False
        if not rg_clean.isdigit():
            return False
        return self.validate_mask()

    def _validate_digit_verify(self, rg: str) -> str:
        """Valida o dígito verificador do RG."""
        sum = 0
        for i in range(9, 1, -1):
            sum += int(rg[9 - i]) * i
        sum = sum % 11
        if sum == 10:
            sum = 0
        return str(sum)
