# Generated by Django 4.1.3 on 2022-11-21 01:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0028_glossary_type_translation_type_alter_glossary_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='glossary',
            options={'verbose_name': 'glossary', 'verbose_name_plural': 'glossaries'},
        ),
        migrations.RemoveIndex(
            model_name='glossary',
            name='archive_g_title_d378e8_idx',
        ),
    ]