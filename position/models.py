from django.db import models

class Position(models.Model):
    category    = models.ForeignKey('company.SubCategory', on_delete = models.CASCADE)
    company     = models.ForeignKey('company.Company', on_delete = models.CASCADE)
    experience  = models.ForeignKey('Experience', on_delete = models.CASCADE)
    like        = models.IntegerField()
    title       = models.CharField(max_length = 100)
    expiry_date = models.DateField()
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

class Experience(models.Model):
    year = models.PositiveSmallIntegerField()

class Description(models.Model):
    position      = models.OneToOneField(Position, on_delete = models.CASCADE)
    intro         = models.TextField()
    duty          = models.TextField()
    qualification = models.TextField()
    preference    = models.TextField()
    benefit       = models.TextField()

class Image(models.Model):
    position = models.ForeignKey(Position, on_delete = models.CASCADE)
    url      = models.URLField(max_length = 3000)

class Address(models.Model):
    position   = models.OneToOneField(Position, on_delete = models.CASCADE)
    country    = models.CharField(max_length = 100)
    city       = models.CharField(max_length = 100)
    line       = models.CharField(max_length = 200)
    latitude   = models.DecimalField(max_digits = 25, decimal_places = 15, null = True)
    longtitude = models.DecimalField(max_digits = 25, decimal_places = 15, null = True)

class Tag(models.Model):
    name     = models.CharField(max_length = 100)
    position = models.ManyToManyField(Position, through = 'Label')

    def __str__(self):
        return self.name

class Label(models.Model):
    position = models.ForeignKey(Position, on_delete = models.CASCADE)
    tag      = models.ForeignKey(Tag, on_delete = models.CASCADE)

