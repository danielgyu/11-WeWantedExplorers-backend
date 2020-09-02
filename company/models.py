from django.db import models

class MainCategory(models.Model):
    name = models.CharField(max_length = 100)

class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete = models.CASCADE)
    name          = models.CharField(max_length = 100)
    image         = models.URLField(max_length = 3000, null = True)

class Company(models.Model):
    sub_category = models.ManyToManyField(SubCategory, through = 'CategoryToCompany')
    name         = models.CharField(max_length = 100)
    field        = models.CharField(max_length = 100)
    logo_url     = models.URLField(max_length = 2000)

class CategoryToCompany(models.Model):
    category = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
    company  = models.ForeignKey(Company, on_delete = models.CASCADE)
