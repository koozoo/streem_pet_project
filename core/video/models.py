from django.db import models
from django.urls import reverse

STATUS_CHOICES = [
    ("n", "New"),
    ("p", "Process"),
    ("c", "Compleat"),
    ("d", "Delete"),
]

RESOLUTION = [
    ("HD", "720p"),
    ("FHD", "1080p"),
    ("SD", "480p"),
    ("4k", "2160p"),
]

TYPE = [
    ("m", "фильм"),
    ("s", "сериал"),
]


class Video(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=TYPE, default='m')
    video = models.FileField(upload_to='video/origin/%Y/%m/%d')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='w', verbose_name='Статус')

    def __str__(self):
        return f'{self.title} оригинальное видео'


class VideoForStreem(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    origin_video = models.ForeignKey(to=Video, on_delete=models.PROTECT)
    resolution = models.CharField(max_length=3)
    duration_in_seconds = models.IntegerField()
    video = models.FileField(upload_to='video/streem/%Y/%m/%d')
