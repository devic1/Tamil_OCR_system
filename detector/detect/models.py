from django.db import models

# Create your models here.

class TextPrediction(models.Model):
    textdata = models.TextField(max_length=None)

    def __str__(self):
        return f"id -> {self.id}\n text -> {self.textdata}"

