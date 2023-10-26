from django.db import models
from django.urls import reverse


class Showrunner(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='category_images', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('showrunner', kwargs={'showrunner_slug': self.slug})

    def __str__(self):
        return self.title
