from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from embed_video.fields import EmbedVideoField
from video import models as video_models

from video.models import Genre

# Create your models here.
STATUS_CHOICES = [
    ("d", "Draft"),
    ("p", "Published"),
    ("w", "Withdrawn"),
]

_messages = {
    'error_validate': "Ошибка при загрузке фалйла, пожалуйста убедитесь что файл с рашрением .mp4"
}


class Shows(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    subject = models.TextField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='shows/images/%Y/%m/%d', null=True, blank=True)
    category_id = models.ForeignKey(to=video_models.Categories, on_delete=models.PROTECT)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Статус')
    total_watch = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    publish_social = models.BooleanField(default=False)
    trailer_link = EmbedVideoField()
    seasons = models.IntegerField(default=1)
    premier_dt = models.DateField()
    showrunner = models.ForeignKey(to=video_models.Showrunner, on_delete=models.PROTECT)
    genre = models.ManyToManyField(to=Genre)

    def __str__(self):
        return f"{self.title} | ID:{self.pk}"


class ShowsItem(models.Model):
    title = models.CharField(max_length=255)
    season = models.IntegerField()
    series = models.IntegerField()
    premier_dt = models.DateField()
    shows_id = models.ForeignKey(to=Shows, on_delete=models.PROTECT)
    video = models.FileField(upload_to='shows/video/%Y/%m/%d',
                             validators=[FileExtensionValidator(allowed_extensions=['mp4'],
                                                                message=_messages['error_validate'])])
    total_watch = models.IntegerField(default=0)
    duration_in_seconds = models.IntegerField(default=0)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='w', verbose_name='Статус')

    def __str__(self):
        return f"Shows_id: {self.shows_id} | {self.title} | season: {self.season} | series {self.series}"

    class Meta:
        ordering = ['season', 'series']


class GenreShows(models.Model):
    shows_id = models.ForeignKey(to=Shows, on_delete=models.PROTECT)
    genre_id = models.ForeignKey(to=video_models.Genre, on_delete=models.PROTECT)


class ActorShows(models.Model):
    actor_id = models.ForeignKey(to=video_models.Actors, on_delete=models.PROTECT)
    shows_id = models.ForeignKey(to=Shows, on_delete=models.PROTECT)


class RatingShows(models.Model):
    shows_id = models.ForeignKey(to=Shows, on_delete=models.PROTECT)
    rating = models.DecimalField(max_digits=1, decimal_places=1, default=0)
    total_vote = models.ImageField(default=0)


class RatingShowsUser(models.Model):
    shows_id = models.ForeignKey(to=Shows, on_delete=models.PROTECT)
    rating = models.DecimalField(max_digits=1, decimal_places=1, default=0)
