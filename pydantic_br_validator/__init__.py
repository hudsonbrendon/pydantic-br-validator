from typing import TYPE_CHECKING

from .field_erros import *  # noqa

__version__ = "0.5.0"


if TYPE_CHECKING:
    CPF = str
    CNH = str
    CPFMask = str
    CPFDigits = str
    CNPJ = str
    CNPJDigits = str
    CNPJMask = str
    TE = str
    PIS = str
    PISMask = str
    PISDigits = str
    Certidao = str
    CertidaoMask = str
    CertidaoDigits = str
    CEP = str
    CEPMask = str
    CEPDigits = str
else:
    from .fields.cnpj_field import *  # noqa
    from .fields.cpf_field import *  # noqa
    from .fields.cep_field import *  # noqa
