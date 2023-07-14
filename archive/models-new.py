from django.conf import settings
from django.db import models
from django.urls import reverse


class Resource(models.Model):

    upload_file = models.FileField(
        null=True,
        upload_to="uploaded_resources",
    )

    RESOURCE_TYPES = (
        ("GLOSSARY", "用語集"),
        ("TRANSLATION", "翻訳"),
    )
    resource_type = models.CharField(
        choices=RESOURCE_TYPES,
        max_length=20,
    )

    title = models.CharField(max_length=100)
    field = models.CharField(max_length=100, blank=True)
    client = models.CharField(max_length=100, blank=True)
    translator = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_resources",
        null=True,
        on_delete=models.SET_NULL,
    )
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="updated_resources",
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "resource"
        verbose_name_plural = "resources"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("resource_detail", args=[str(self.id)])


class Item(models.Model):

    resource = models.ForeignKey(
        Resource,
        related_name="items",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    source = models.TextField(blank=True)
    target = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_items",
        null=True,
        on_delete=models.SET_NULL,
    )
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="updated_items",
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "item"
        verbose_name_plural = "items"

    def __str__(self):
        return f"{self.source} : {self.target}"

    def get_absolute_url(self):
        return reverse("item_detail", args=[str(self.id)])
