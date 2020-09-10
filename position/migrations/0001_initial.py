# Generated by Django 3.0.3 on 2020-09-10 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('expiry_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.SubCategory')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company')),
                ('experience', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='position.Experience')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.ManyToManyField(through='position.Label', to='position.Position')),
            ],
        ),
        migrations.AddField(
            model_name='label',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='position.Position'),
        ),
        migrations.AddField(
            model_name='label',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='position.Tag'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=3000)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='position.Position')),
            ],
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro', models.TextField()),
                ('duty', models.TextField()),
                ('qualification', models.TextField()),
                ('preference', models.TextField()),
                ('benefit', models.TextField()),
                ('position', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='position.Position')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('line', models.CharField(max_length=200)),
                ('latitude', models.DecimalField(decimal_places=7, max_digits=9, null=True)),
                ('longtitude', models.DecimalField(decimal_places=7, max_digits=10, null=True)),
                ('position', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='position.Position')),
            ],
        ),
    ]
