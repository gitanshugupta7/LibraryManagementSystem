# Generated by Django 3.0.7 on 2022-06-15 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books_Title', '0017_auto_20220615_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='student_id',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
