# Generated by Django 3.0.7 on 2022-06-15 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books_Title', '0015_auto_20220506_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='student_id',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='dept',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
