# Generated by Django 4.0.3 on 2022-11-28 18:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0004_alter_employee_options_alter_employee_is_supervisor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='job_time',
            field=models.CharField(choices=[('1', '1'), ('3/4', '3/4'), ('1/2', '1/2'), ('1/4', '1/4')], max_length=3,
                                   verbose_name='Wymiar etatu'),
        ),
    ]
