# Generated by Django 4.1.3 on 2023-04-12 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0032_alter_glossary_title_alter_glossary_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='source',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='segment',
            name='target',
            field=models.TextField(blank=True),
        ),
    ]
