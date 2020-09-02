from django.core.exceptions   import ValidationError

def Validate_title(title):
    if len(title) < 1:
        raise ValidationError('필수정보를 입력해주세요')

def Validate_writername(writer_name):
    if len(writer_name) < 1:
        raise ValidationError('필수정보를 입력해주세요')

def Validate_email(email):
    if len(email) < 1:
        raise ValidationError('필수정보를 입력해주세요')

def Validate_phone_number(phone_number):
    if len(phone_number) < 1:
        raise ValidationError('필수정보를 입력해주세요')

def length_counter(*args) :
    return sum([len(arg) for arg in args])
    