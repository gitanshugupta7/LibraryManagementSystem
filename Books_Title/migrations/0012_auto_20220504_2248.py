# Generated by Django 3.0.7 on 2022-05-04 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books_Title', '0011_auto_20220504_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='registration_no',
            field=models.CharField(default='', max_length=10),
        ),
    ]
