"""
Validadores personalizados para campos brasileiros (CPF, CNPJ, etc.)
"""

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_cpf(value):
    """
    Valida se o CPF é válido.
    """
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', value)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        raise ValidationError(_('CPF deve ter 11 dígitos.'))
    
    # Verifica se não é uma sequência de números iguais
    if cpf == cpf[0] * 11:
        raise ValidationError(_('CPF inválido.'))
    
    # Calcula os dígitos verificadores
    def calculate_digit(cpf, weight):
        total = sum(int(cpf[i]) * weight[i] for i in range(len(weight)))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
    
    # Verifica primeiro dígito
    first_digit = calculate_digit(cpf, [10, 9, 8, 7, 6, 5, 4, 3, 2])
    if int(cpf[9]) != first_digit:
        raise ValidationError(_('CPF inválido.'))
    
    # Verifica segundo dígito
    second_digit = calculate_digit(cpf, [11, 10, 9, 8, 7, 6, 5, 4, 3, 2])
    if int(cpf[10]) != second_digit:
        raise ValidationError(_('CPF inválido.'))


def validate_cnpj(value):
    """
    Valida se o CNPJ é válido.
    """
    # Remove caracteres não numéricos
    cnpj = re.sub(r'\D', '', value)
    
    # Verifica se tem 14 dígitos
    if len(cnpj) != 14:
        raise ValidationError(_('CNPJ deve ter 14 dígitos.'))
    
    # Verifica se não é uma sequência de números iguais
    if cnpj == cnpj[0] * 14:
        raise ValidationError(_('CNPJ inválido.'))
    
    # Calcula primeiro dígito verificador
    weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(int(cnpj[i]) * weights[i] for i in range(12))
    remainder = total % 11
    first_digit = 0 if remainder < 2 else 11 - remainder
    
    if int(cnpj[12]) != first_digit:
        raise ValidationError(_('CNPJ inválido.'))
    
    # Calcula segundo dígito verificador
    weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(int(cnpj[i]) * weights[i] for i in range(13))
    remainder = total % 11
    second_digit = 0 if remainder < 2 else 11 - remainder
    
    if int(cnpj[13]) != second_digit:
        raise ValidationError(_('CNPJ inválido.'))


def validate_phone(value):
    """
    Valida se o telefone está em formato brasileiro válido.
    """
    # Remove caracteres não numéricos
    phone = re.sub(r'\D', '', value)
    
    # Verifica se tem 10 ou 11 dígitos
    if len(phone) not in [10, 11]:
        raise ValidationError(_('Telefone deve ter 10 ou 11 dígitos.'))
    
    # Verifica se o DDD é válido (11 a 99)
    ddd = int(phone[:2])
    if ddd < 11 or ddd > 99:
        raise ValidationError(_('DDD inválido.'))
    
    # Se for celular (11 dígitos), o primeiro dígito após o DDD deve ser 9
    if len(phone) == 11 and phone[2] != '9':
        raise ValidationError(_('Número de celular deve começar com 9.'))


def validate_cep(value):
    """
    Valida se o CEP está no formato brasileiro correto.
    """
    # Remove caracteres não numéricos
    cep = re.sub(r'\D', '', value)
    
    # Verifica se tem 8 dígitos
    if len(cep) != 8:
        raise ValidationError(_('CEP deve ter 8 dígitos.'))
    
    # Verifica se não é uma sequência de zeros
    if cep == '00000000':
        raise ValidationError(_('CEP inválido.'))


def clean_cpf(value):
    """
    Remove formatação do CPF, mantendo apenas números.
    """
    if value:
        return re.sub(r'\D', '', value)
    return value


def clean_cnpj(value):
    """
    Remove formatação do CNPJ, mantendo apenas números.
    """
    if value:
        return re.sub(r'\D', '', value)
    return value


def clean_phone(value):
    """
    Remove formatação do telefone, mantendo apenas números.
    """
    if value:
        return re.sub(r'\D', '', value)
    return value


def clean_cep(value):
    """
    Remove formatação do CEP, mantendo apenas números.
    """
    if value:
        return re.sub(r'\D', '', value)
    return value


def format_cpf(value):
    """
    Formata CPF para exibição (000.000.000-00).
    """
    if not value:
        return value
    
    cpf = clean_cpf(value)
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return value


def format_cnpj(value):
    """
    Formata CNPJ para exibição (00.000.000/0000-00).
    """
    if not value:
        return value
    
    cnpj = clean_cnpj(value)
    if len(cnpj) == 14:
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return value


def format_phone(value):
    """
    Formata telefone para exibição ((00) 00000-0000 ou (00) 0000-0000).
    """
    if not value:
        return value
    
    phone = clean_phone(value)
    if len(phone) == 11:
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    elif len(phone) == 10:
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    return value


def format_cep(value):
    """
    Formata CEP para exibição (00000-000).
    """
    if not value:
        return value
    
    cep = clean_cep(value)
    if len(cep) == 8:
        return f"{cep[:5]}-{cep[5:]}"
    return value