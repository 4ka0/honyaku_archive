# Generated by Django 4.0.5 on 2022-06-21 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0024_delete_glossaryuploadfile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translation',
            name='translation_file',
            field=models.FileField(null=True, upload_to='translation_files'),
        ),
    ]
