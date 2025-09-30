from typing import TYPE_CHECKING

from .field_erros import *  # noqa

__version__ = "0.7.0"


if TYPE_CHECKING:
    CPF = str
    CPFMask = str
    CPFDigits = str
    RG = str
    RGMask = str
    RGDigits = str
    CNPJ = str
    CNPJDigits = str
    CNPJMask = str
    CEP = str
    CEPMask = str
    CEPDigits = str
else:
    from .fields.cnpj_field import *  # noqa
    from .fields.cnh_field import *  # noqa
    from .fields.cpf_field import *  # noqa
    from .fields.cep_field import *  # noqa
    from .fields.rg_field import *  # noqa
