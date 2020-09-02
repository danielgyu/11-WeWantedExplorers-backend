import re

from django.core.exceptions         import ValidationError

def Validate_email(input_email):
    email_reg = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    regex     = re.compile(email_reg)

    if not regex.match(input_email):
        raise ValidationError('올바른 이메일 형식을 입력해주세요.')
    if UserAccount.objects.filter(email = input_email).exists():
        raise ValidationError('이미 존재하는 이메일입니다.')


def Validate_password(input_password):
    password_reg  = r"^(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,30}$"
    regex     = re.compile(password_reg)

    if not regex.match(input_password):
        raise ValidationError('영문자, 숫자, 특수문자만 사용하여 6자 이상 입력해주세요.')


def Validate_phonenumber(input_phonenumber):
    phonenumber_reg  = r"^(010|011)\d{4}\d{4}[0-9]{11}$"
    regex     = re.compile(phonenumber_reg)

    if not regex.match(input_phonenumber):
        raise ValidationError('올바른 전화번호를 입력해주세요.')  
