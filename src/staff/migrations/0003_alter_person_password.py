# Generated by Django 4.2 on 2024-06-12 19:14

import django.contrib.auth.password_validation
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_rename_person_staff_person_ptr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='password',
            field=models.CharField(max_length=128, validators=[django.contrib.auth.password_validation.validate_password]),
        ),
    ]
