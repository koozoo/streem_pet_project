from django.db import models


class Rating(models.Model):
    rate = models.IntegerField()
