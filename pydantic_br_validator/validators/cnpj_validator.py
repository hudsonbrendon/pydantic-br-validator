import re

from .base_validator import FieldMaskValidator

__all__ = ["CNPJValidator"]


class CNPJValidator(FieldMaskValidator):
    def __init__(self, cnpj) -> None:
        self.cnpj = cnpj

    def validate_mask(self) -> bool:
        if len(self.cnpj) == 18:
            if (
                self.cnpj[2:3] == "."
                and self.cnpj[6:7] == "."
                and self.cnpj[10:11] == "/"
                and self.cnpj[15:16] == "-"
            ):
                return True
        return False

    def _get_char_value(self, char: str) -> int:
        """
        Retorna o valor do caractere para cálculo do dígito verificador.
        Para CNPJ alfanumérico, o valor é o código ASCII - 48.
        Números: 0-9 (valores 0-9)
        Letras: A-Z (valores 17-42)
        """
        return ord(char.upper()) - 48

    def _is_valid_cnpj_char(self, char: str) -> bool:
        """Verifica se o caractere é válido para CNPJ alfanumérico (0-9, A-Z)."""
        return char.isdigit() or (char.upper() >= "A" and char.upper() <= "Z")

    def _clean_cnpj(self, cnpj: str) -> str:
        """Remove caracteres de formatação (pontos, barras, hífens)."""
        return re.sub(r"[.\-/]", "", cnpj).upper()

    def validate(self) -> bool:
        cnpj = self._clean_cnpj(self.cnpj)

        if len(cnpj) != 14:
            return False

        # Verifica se os 12 primeiros caracteres são alfanuméricos válidos
        for char in cnpj[:12]:
            if not self._is_valid_cnpj_char(char):
                return False

        # Os 2 últimos dígitos devem ser numéricos
        if not cnpj[12:14].isdigit():
            return False

        first_digit = self._validate_first_digit(cnpj)
        second_digit = self._validate_second_digit(cnpj)
        return cnpj[12] == first_digit and cnpj[13] == second_digit

    def _validate_first_digit(self, cnpj: str) -> str:
        total = 0
        weight = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        for n in range(12):
            value = self._get_char_value(cnpj[n]) * weight[n]
            total = total + value

        check_digit = total % 11

        if check_digit < 2:
            first_digit = 0
        else:
            first_digit = 11 - check_digit
        return str(first_digit)

    def _validate_second_digit(self, cnpj: str) -> str:
        total = 0
        weight = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        for n in range(13):
            total = total + self._get_char_value(cnpj[n]) * weight[n]

        check_digit = total % 11

        if check_digit < 2:
            second_digit = 0
        else:
            second_digit = 11 - check_digit
        return str(second_digit)
