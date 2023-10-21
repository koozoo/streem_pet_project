from django.db import models
from django.urls import reverse
from embed_video.fields import EmbedVideoField
from video import models as video_models

# Create your models here.
STATUS_CHOICES = [
    ("d", "Draft"),
    ("p", "Published"),
    ("w", "Withdrawn"),
]


class Shows(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    subject = models.TextField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='movie_images/%Y/%m/%d', null=True, blank=True)
    actors = models.TextField(blank=True, null=True)
    category_id = models.ForeignKey(to=video_models.Categories, on_delete=models.PROTECT)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Статус')
    total_watch = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    publish_social = models.BooleanField(default=False)
    trailer_link = EmbedVideoField()
