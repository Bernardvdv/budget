from django.db import models


class Items(models.Model):
    name = models.CharField(max_length=180, unique=True)
    value = models.CharField(max_length=20)
