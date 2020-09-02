import re

from django.core.exceptions   import ValidationError
from django.core.validators   import RegexValidator

def Validate_email(email):
    email_reg = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    regex     = re.compile(email_reg)

    if not regex.match(email):
        raise ValidationError('올바른 이메일 형식을 입력해주세요.')


def Validate_password(password):
    if len(password) < 6:
        raise ValidationError('비밀번호는 6자 이상 입력해주세요.')


def Validate_phonenumber(phone_number):
    phonenumber_reg  = r"^\+?1?\d{9,15}$"
    regex     = re.compile(phonenumber_reg)

    if not regex.match(phone_number):
        raise ValidationError('올바른 전화번호를 입력해주세요.')  
