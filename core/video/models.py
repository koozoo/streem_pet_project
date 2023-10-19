from django.db import models
from django.urls import reverse

# Create your models here.
STATUS_CHOICES = [
    ("d", "Draft"),
    ("p", "Published"),
    ("w", "Withdrawn"),
]


class VideoCategories(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='category_images', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self):
        return f"ID: {self.pk}: {self.title}"


class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    subject = models.TextField(blank=True, null=True, verbose_name='Короткое описание')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Статус')
    image = models.ImageField(upload_to='course_images', blank=True, null=True)
    category_id = models.ForeignKey(to=ProductCategories, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('course', kwargs={'course_slug': self.slug})

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self):
        return f"ID: {self.pk}: {self.title}"


class Genre(models.Model):
    ...


class Tag(models.Model):
    ...


