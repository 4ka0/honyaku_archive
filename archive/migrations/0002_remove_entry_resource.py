# Generated by Django 3.2.6 on 2021-09-19 03:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='resource',
        ),
    ]
