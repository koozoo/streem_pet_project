from django.db import models
from django.urls import reverse

STATUS_CHOICES = [
    ("d", "Draft"),
    ("p", "Published"),
    ("w", "Withdrawn"),
]


class Tags(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    images = models.ImageField(upload_to='tags_images/%Y/%m/%d', null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p', verbose_name='Статус')

    def get_absolute_url(self):
        return reverse('tags', kwargs={'tags_slug': self.slug})

    def __str__(self):
        return f"TAG: ID: {self.pk} | slug: {self.slug} | title: {self.title}"
