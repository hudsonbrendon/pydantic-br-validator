# Pydantic BR Validator

Uma biblioteca python com modelos de validação para os principais documentos brasileiros.

# Instalação

```bash
pip install pydantic_br_validator
```

# Campos disponíveis

## CPF

```python
from pprint import pprint

from pydantic import BaseModel

from pydantic_br_validator import CPF, CPFDigits, CPFMask


class Cliente(BaseModel):
    nome: str
    cpf: CPF  # aceita CPF válidos com ou sem máscara
    cpf_mask: CPFMask  # aceita CPF válido apenas com máscara
    cpf_digits: CPFDigits  # aceita CPF válido apenas com dígitos


cliente = Cliente(
    nome="Hudson", cpf="04120039021", cpf_mask="041.200.390-21", cpf_digits="04120039021"
)


pprint(cliente.dict())
```

## CNPJ

```python
from pprint import pprint

from pydantic import BaseModel

from pydantic_br_validator import CNPJ, CNPJDigits, CNPJMask


class Cliente(BaseModel):
    nome: str
    cnpj: CNPJ  # aceita CNPJ válidos com ou sem máscara
    cnpj_mask: CNPJMask  # aceita CNPJ válido apenas com máscara
    cnpj_digits: CNPJDigits  # aceita CNPJ válido apnas com dígitos


cliente = Cliente(
    nome="Hudson", cnpj="47895328000187", cnpj_mask="47.895.328/0001-87", cnpj_digits="47895328000187"
)


pprint(cliente.dict())
```

# Contribua 🚀
