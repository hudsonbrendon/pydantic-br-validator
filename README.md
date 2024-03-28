# Pydantic BR Validator

<p align="center">
  <a href="https://sqlmodel.tiangolo.com"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/1600px-Flag_of_Brazil.svg.png" alt="Pydantic BR Validator"></a>
</p>
<p align="center">
    <em>Uma biblioteca python com modelos de validação para os principais documentos brasileiros.</em>
</p>
<p align="center">
<a href="https://github.com/hudsonbrendon/pydantic-br-validator/actions/workflows/pythonpackage.yml" target="_blank">
    <img src="https://github.com/hudsonbrendon/pydantic-br-validator/actions/workflows/pythonpackage.yml/badge.svg?branch=master" alt="Test">
</a>
<a href="https://pypi.org/project/pydantic-br-validator" target="_blank">
    <img src="https://img.shields.io/pypi/v/pydantic-br-validator?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/pydantic-br-validator" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/pydantic-br-validator.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

# Instalação

```bash
pip install pydantic-br-validator
```

# Campos disponíveis

- [x] CPF
- [x] CNPJ
- [ ] RG
- [ ] CNH
- [ ] DUT
- [ ] Título de eleitor
- [ ] PIS
- [ ] Certidão de nascimento
- [ ] Renavam
- [ ] Placa
- [ ] ISBN
- [ ] CEP

# Exemplos

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

# Licença

Este projeto está licenciado sob os termos da licença do [MIT licença](https://en.wikipedia.org/wiki/MIT_License)
