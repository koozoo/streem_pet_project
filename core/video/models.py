from django.db import models
from django.urls import reverse

# Create your models here.
STATUS_CHOICES = [
    ("d", "Draft"),
    ("p", "Published"),
    ("w", "Withdrawn"),
]


class VideoGroup(models.Model):
    title = models.CharField(max_length=255)


class VideoCategories(models.Model):
    title = models.CharField(max_length=255)
    system_title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='category_images', null=True, blank=True)
    video_group_id = models.ForeignKey(to=VideoGroup, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self):
        return f"ID: {self.pk}: {self.title}"


class Genre(models.Model):
    ...


class Tag(models.Model):
    ...


class VideoTag(models.Model):

    ...


class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Статус')
    image = models.ImageField(upload_to='video_images', blank=True, null=True)
    storage_path = models.FilePathField(path='video_files', verbose_name='путь до файла')
    category_id = models.ForeignKey(to=VideoCategories, on_delete=models.PROTECT)



