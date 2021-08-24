from django.core.exceptions import ValidationError


def validate_cpf(value):
    if len(value) != 11:
        raise ValidationError("CPF deve ter 11 dígitos")


def validate_cnpj(value):
    if len(value) != 14:
        raise ValidationError("CNPJ deve ter 14 dígitos")
