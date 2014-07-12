from django.db import models


class TestModel(models.Model):
    text_field = models.TextField(name="text_field")
