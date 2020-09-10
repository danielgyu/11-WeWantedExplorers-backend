from django.db       import models
from .validator      import (
    Validate_email, 
    Validate_phonenumber, 
    Validate_password
    )

from company.models  import Company

class UserAccount(models.Model):
    email          = models.CharField(max_length=100, validators=[Validate_email], unique=True)
    platform_type  = models.CharField(max_length=100)
    created_at     = models.DateTimeField(auto_now_add=True)
    is_deleted     = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_accounts'

class UserInformation(models.Model):
    name           = models.CharField(max_length=100)
    phone_number   = models.CharField(max_length=100, validators=[Validate_phonenumber], unique=True)
    password       = models.CharField(max_length=100, validators=[Validate_password])
    updated_at     = models.DateField(auto_now=True)
    is_deleted     = models.BooleanField(default=False)
    user_account   = models.ForeignKey('UserAccount',on_delete=models.CASCADE, related_name='userinfo')

    class Meta:
        db_table = 'user_information'

class MatchUpInformation(models.Model):
    job_group        = models.CharField(max_length=100, null=True)
    position         = models.CharField(max_length=100, null=True)
    career_year      = models.IntegerField(null=True)
    is_developer     = models.BooleanField(null=True)
    education        = models.CharField(max_length=500, null=True)
    company          = models.CharField(max_length=500, null=True)
    user_information = models.OneToOneField(UserInformation, on_delete=models.CASCADE)

    class Meta:
        db_table = 'match_up_information'

class JobSkill(models.Model):
    name                = models.CharField(max_length=200, null=True)
    matchup_information = models.ForeignKey(MatchUpInformation, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'jobskills'

class Recomender(models.Model):
    name             = models.CharField(max_length=100, null=True)
    user_information = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'recomenders'

class CompanyException(models.Model):
    name             = models.CharField(max_length=100, null=True)
    user_information = models.ForeignKey(UserInformation, on_delete=models.CASCADE)

    class Meta:
        db_table = 'company_exceptions'

class UserStatus(models.Model):
    name             = models.CharField(max_length=100, null=True)
    user_information = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
   
    class Meta:
        db_table = 'user_status'

class SuggestionStatus(models.Model):
    company_name     = models.CharField(max_length=200, null=True)
    process_status   = models.CharField(max_length=100, null=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    user_information = models.ForeignKey(UserInformation, on_delete=models.CASCADE)

    class Meta:
        db_table = 'suggest_status'

class ApplicationStatus(models.Model):
    company          = models.ForeignKey('position.Position', on_delete=models.CASCADE, related_name='status_company')
    position         = models.ForeignKey('position.Position', on_delete=models.CASCADE, related_name='status_position')
    logo_url         = models.ForeignKey('position.Position', on_delete=models.CASCADE, related_name='status_logo')
    process_status   = models.CharField(max_length=200)
    recommendation   = models.CharField(max_length=200, null=True)
    is_compensation  = models.BooleanField()
    created_at       = models.DateTimeField(auto_now_add=True)
    user_information = models.ForeignKey(UserInformation, on_delete=models.CASCADE)

    class Meta:
        db_table = 'application_status'

class BookMark(models.Model): 
    user_information = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    company          = models.ForeignKey(Company, on_delete=models.CASCADE)
