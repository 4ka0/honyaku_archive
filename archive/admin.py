from django.contrib import admin

from .models import (
    Entry, Glossary, Translation, Segment, Item, Resource
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
        "title",
        "field",
        "client",
        "translator",
        "notes",
        "type",
    )
    list_display = (
        'title',
        'field',
        'client',
        "translator",
    )


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'source',
        'target',
        'resource',
    )
    search_fields = ["source", "target"]


class ResourceAdmin(admin.ModelAdmin):
    fields = (
        "resource_type",
        "title",
        "field",
        "client",
        "translator",
        "notes",
    )
    list_display = (
        "title",
        "resource_type",
        "field",
        "client",
        "translator",
    )
    search_fields = ["title"]


admin.site.register(Entry, EntryAdmin)
admin.site.register(Glossary, GlossaryAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(Segment, SegmentAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Resource, ResourceAdmin)
