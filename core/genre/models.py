from django.db import models
from django.urls import reverse

STATUS_CHOICES = [
    ("d", "Draft"),
    ("p", "Published"),
    ("w", "Withdrawn"),
]


class Genre(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='genre_images', null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p', verbose_name='Статус')

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})

    def __str__(self):
        return self.title
