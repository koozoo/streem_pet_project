from django.db import models
from django.urls import reverse


class Tags(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse('tags', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return f"TAG: ID: {self.pk} | slug: {self.slug} | title: {self.title}"
