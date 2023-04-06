from django.contrib import admin

from .models import (
    Entry, Glossary, Translation, Segment
)


class EntryAdmin(admin.ModelAdmin):
    list_display = (
        'source',
        'target',
        'glossary',
    )
    search_fields = ["source", "target"]


class SegmentAdmin(admin.ModelAdmin):
    list_display = (
        'source',
        'target',
        'translation',
    )
    search_fields = ["source", "target"]


class GlossaryAdmin(admin.ModelAdmin):
    fields = (
        "title",
        "notes",
        "type",
    )
    list_display = (
        'title',
        'notes',
    )


class TranslationAdmin(admin.ModelAdmin):
    fields = (
        "job_number",
        "field",
        "client",
        "translator",
        "notes",
        "type",
    )
    list_display = (
        'job_number',
        'field',
        'client',
        "translator",
    )


admin.site.register(Entry, EntryAdmin)
admin.site.register(Glossary, GlossaryAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(Segment, SegmentAdmin)
