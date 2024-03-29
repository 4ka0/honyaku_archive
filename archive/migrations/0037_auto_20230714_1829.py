# Generated by Django 4.1.3 on 2023-07-14 09:29

from django.db import migrations


def add_translations_as_resources(apps, schema_editor):

    Translation = apps.get_model("archive", "Translation")
    Resource = apps.get_model("archive", "Resource")

    for translation in Translation.objects.all():
        resource = Resource(
            resource_type="TRANSLATION",
            title=translation.title,
            field=translation.field,
            client=translation.client,
            translator=translation.translator,
            notes=translation.notes,
            created_on=translation.created_on,
            created_by=translation.created_by,
            updated_on=translation.created_on,
            updated_by=translation.created_by,
        )
        resource.save()


class Migration(migrations.Migration):
    dependencies = [
        ("archive", "0036_auto_20230714_1753"),
    ]

    operations = [
        migrations.RunPython(add_translations_as_resources)
    ]
