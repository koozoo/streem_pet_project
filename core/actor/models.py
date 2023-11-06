from django.db import models
from django.urls import reverse


class Actors(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    bio = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('actors', kwargs={'actors_slug': self.slug})
