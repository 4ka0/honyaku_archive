from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username}"
