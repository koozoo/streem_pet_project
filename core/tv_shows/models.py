from django.db import models
from django.core.validators import FileExtensionValidator
from embed_video.fields import EmbedVideoField

from actor.models import Actors
from categories.models import Categories
from genre.models import Genre
from showrunner.models import Showrunner

from video.models import Video

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
    category_id = models.ForeignKey(to=Categories, on_delete=models.PROTECT)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Статус')
    total_watch = models.PositiveBigIntegerField(default=0)
    publish_social = models.BooleanField(default=False)
    trailer_link = EmbedVideoField(blank=True, null=True)
    seasons = models.IntegerField(default=1)
    premier_dt = models.DateField()
    showrunner = models.ForeignKey(to=Showrunner, on_delete=models.PROTECT)
    genre = models.ManyToManyField(to=Genre)

    def __str__(self):
        return f"{self.title} | ID:{self.pk}"


class ShowsItem(models.Model):
    title = models.CharField(max_length=255)
    season = models.PositiveIntegerField()
    series = models.PositiveIntegerField()
    premier_dt = models.DateField()
    video = models.ForeignKey(to=Video, on_delete=models.PROTECT, related_name='origin_shows_video')
    shows_id = models.ForeignKey(to=Shows, on_delete=models.PROTECT, related_name='parent_shows_item')
    total_watch = models.PositiveBigIntegerField(default=0)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='w', verbose_name='Статус')

    def __str__(self):
        return f"Shows: {self.shows_id} | ID: {self.pk} | {self.title} | season: {self.season} | series {self.series}"

    class Meta:
        ordering = ['season', 'series']
