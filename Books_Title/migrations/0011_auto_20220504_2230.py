# Generated by Django 3.0.7 on 2022-05-04 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books_Title', '0010_auto_20220504_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='dor',
            field=models.DateField(blank=True, null=True, verbose_name='Date of Return'),
        ),
        migrations.AlterField(
            model_name='log',
            name='edor',
            field=models.DateField(null=True, verbose_name='Expected Date of Return'),
        ),
    ]