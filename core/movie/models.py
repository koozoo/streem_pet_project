from django.db import models
from django.urls import reverse
from video import models as video_models
# Create your models here.
STATUS_CHOICES = [
    ("d", "Draft"),
    ("p", "Published"),
    ("w", "Withdrawn"),
]


class Movie(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    subject = models.TextField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='movie_images', null=True, blank=True)
    video = models.FileField(upload_to='movie_video/%y/%m/%d')
    actors = models.TextField(blank=True, null=True)
    category_id = models.ForeignKey(to=video_models.Categories, on_delete=models.PROTECT)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Статус')
    # total_watch = models.DecimalField(max_digits=12, decimal_places=0)

    def get_absolute_url(self):
        return reverse('movie', kwargs={'movie_slug': self.slug})

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self):
        return f"ID: {self.pk}: {self.title}"


class MovieTrailer(models.Model):
    movie_id = models.ForeignKey(to=Movie, on_delete=models.PROTECT)
    images = models.ImageField(upload_to='trailer_images', null=True, blank=True)
    video = models.FileField(upload_to='movie_trailer/%y/%m/%d')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Статус')


class ActorMovie(models.Model):
    actor_id = models.ForeignKey(to=video_models.Actors, on_delete=models.PROTECT)
    movie_id = models.ForeignKey(to=Movie, on_delete=models.PROTECT)
