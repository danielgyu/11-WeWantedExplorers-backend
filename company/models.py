from django.db        import models
from django.db.models import Avg

class MainCategory(models.Model):
    name = models.CharField(max_length = 100)
    @classmethod
    def salary_average(cls, id, year):
        average = cls.objects.get(id= id).subcategory_set.filter(salary__year = year).\
aggregate(Avg('salary__payroll')).get('salary__payroll__avg')
        return average

class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete = models.CASCADE)
    name          = models.CharField(max_length = 100)
    image         = models.URLField(max_length = 3000, null = True)

class Company(models.Model):
    sub_category = models.ManyToManyField(SubCategory, through = 'CategoryToCompany')
    name         = models.CharField(max_length = 100)
    field        = models.CharField(max_length = 100)
    logo_url     = models.URLField(max_length = 2000)
    is_premium   = models.BooleanField(default = False)
    banner_url   = models.CharField(max_length = 2000, null = True)

class Salary(models.Model):
    category = models.ManyToManyField(SubCategory, through = 'CategoryToSalary')
    year = models.PositiveSmallIntegerField()
    payroll = models.IntegerField()

class CategoryToCompany(models.Model):
    category = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
    company  = models.ForeignKey(Company, on_delete = models.CASCADE)
    
class CategoryToSalary(models.Model):
    category = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
    salary = models.ForeignKey(Salary, on_delete = models.CASCADE)
