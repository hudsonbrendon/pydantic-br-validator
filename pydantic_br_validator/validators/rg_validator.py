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
        # Primeira parte: 2 dígitos, Segunda parte: 3 dígitos, Terceira parte: XXX-X (3 dígitos + hífen + 1 dígito)
        if len(parts[0]) != 2 or len(parts[1]) != 3 or len(parts[2]) != 5:
            return False
        if parts[2][3] != "-":
            return False
        return all(part.replace("-", "").isdigit() for part in parts)

    def validate(self) -> bool:
        """Valida se o RG tem 8 ou 9 caracteres, permitindo máscara e X no final."""
        rg_clean = self.rg.replace(".", "").replace("-", "")
        # RG pode ter 8 ou 9 caracteres
        if len(rg_clean) not in [8, 9]:
            return False
        # Pode conter X no final (alguns estados brasileiros)
        if rg_clean[-1].upper() == "X":
            if not rg_clean[:-1].isdigit():
                return False
        elif not rg_clean.isdigit():
            return False
        # Se tem pontos ou hífen, valida a máscara
        if "." in self.rg or "-" in self.rg:
            return self.validate_mask()
        return True

    def _validate_digit_verify(self, rg: str) -> str:
        """Valida o dígito verificador do RG."""
        sum = 0
        for i in range(9, 1, -1):
            sum += int(rg[9 - i]) * i
        sum = sum % 11
        if sum == 10:
            sum = 0
        return str(sum)
