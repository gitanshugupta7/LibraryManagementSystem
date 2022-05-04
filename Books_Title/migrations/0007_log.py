# Generated by Django 3.0.7 on 2022-05-04 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Books_Title', '0006_auto_20210603_0908'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('log_index', models.AutoField(primary_key=True, serialize=False)),
                ('acc_no', models.IntegerField(default=0)),
                ('doi', models.DateField(auto_now_add=True)),
                ('dor', models.DateField()),
                ('issue_mode', models.CharField(choices=[('Reading', 'Reading'), ('Book Bank', 'Book Bank'), ('15 Days', '15 Days')], max_length=15)),
                ('edor', models.DateField()),
                ('registration_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Books_Title.StudentProfile')),
            ],
        ),
    ]