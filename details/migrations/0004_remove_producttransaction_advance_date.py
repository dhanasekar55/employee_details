# Generated by Django 5.1.3 on 2024-12-03 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0003_alter_employee_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producttransaction',
            name='advance_date',
        ),
    ]