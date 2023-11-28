from django.db import models


class DummyModel(models.Model):
    name = models.CharField(default="Hello", max_length=23)
