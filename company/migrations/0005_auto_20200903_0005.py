# Generated by Django 3.1.1 on 2020-09-03 00:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20200902_1452'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='logo',
            new_name='logo_url',
        ),
    ]
