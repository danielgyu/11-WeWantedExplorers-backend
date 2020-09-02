from django.db import models

class Resume(models.Model):
    title             = models.CharField(max_length=150)
    writer_name       = models.CharField(max_length=100)
    email             = models.EmailField(null=True)
    description       = models.TextField(null=True)
    completion_status = models.CharField(max_length=100, null=True)
    is_fileupload     = models.BooleanField()
    fileurl           = models.URLField(null=True)
    created_at        = models.DateField(auto_now_add=True)
    user_information  = models.ForeignKey(UserInformation,on_delete=models.CASCADE, related_name='resume')
    
    class Meta:
        db_table = 'resumes'

class Career(models.Model): 
    company_name      = models.CharField(max_length=100)
    department        = models.CharField(max_length=100, null=True)
    position          = models.CharField(max_length=100, null=True)
    accomplishment    = models.CharField(max_length=1000, null=True)
    start_date        = models.DateField()
    end_date          = models.DateField()
    is_incumbent      = models.BooleanField()
    resume            = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='career')

    class Meta:
        db_table = 'careers'

class Education(models.Model):
    school_name       = models.CharField(max_length=100)
    major             = models.CharField(max_length=100)
    degree            = models.CharField(max_length=100)
    research_content  = models.CharField(max_length=1000, null=True)
    start_date        = models.DateField()
    end_date          = models.DateField()
    is_attending      = models.BooleanField()
    resume            = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')

    class Meta:
        db_table = 'educations'

class AwardHistory(models.Model):
    award_name  = models.CharField(max_length=100)
    detail      = models.CharField(max_length=800, null=True)
    date        = models.DateField()
    resume      = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='award_history')

    class Meta:
        db_table = 'award_histories'
class ForeignLanguage(models.Model):
    name    = models.CharField(max_length=150)
    level   = models.CharField(max_length=100)
    resume  = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='foreign_language')

    class Meta:
        db_table = 'foreign_language'

class LanguageTest(models.Model):
    name              = models.CharField(max_length=150)
    level             = models.CharField(max_length=100, null=True)
    score             = models.CharField(max_length=100, null=True)
    date              = models.DateField()
    foreignLanguage   = models.ForeignKey(ForeignLanguage, on_delete=models.CASCADE, related_name='language_test')

    class Meta:
        db_table = 'language_tests'

class Link(models.Model):
    url     = models.URLField()
    resume  = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='link')
    
    class Meta:
        db_table = 'links'