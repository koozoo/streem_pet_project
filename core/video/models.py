from django.db import models
from django.urls import reverse

# Create your models here.
STATUS_CHOICES = [
    ("d", "Draft"),
    ("p", "Published"),
    ("w", "Withdrawn"),
]


class Actors(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    bio = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('actors', kwargs={'actors_slug': self.slug})


class Categories(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Статус')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self):
        return f"{self.title}"


class Genre(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='genre_images', null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Статус')

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=255)


class Rating(models.Model):
    rate = models.IntegerField()


class Showrunner(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='category_images', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('showrunner', kwargs={'showrunner_slug': self.slug})

    def __str__(self):
        return self.title


_messages = {
    'error_validate': "Ошибка при загрузке фалйла, пожалуйста убедитесь что файл с рашрением .mp4"
}



    
