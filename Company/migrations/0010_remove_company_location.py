# Generated by Django 4.2.3 on 2024-05-10 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0009_alter_company_options_company_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='location',
        ),
    ]
