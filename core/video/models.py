from django.db import models
from django.urls import reverse

STATUS_CHOICES = [
    ("n", "New"),
    ("p", "Process"),
    ("c", "Compleat"),
    ("d", "Delete"),
]

TYPE = [
    ("m", "фильм"),
    ("s", "сериал"),
]


class Video(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=TYPE, default='m')
    video = models.FileField(upload_to='video/origin/%Y/%m/%d')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n', verbose_name='Статус')

    def __str__(self):
        return f'{self.title} оригинальное видео'


class VideoForStreem(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE, default='s')
    origin_video = models.ForeignKey(to=Video, on_delete=models.PROTECT)
    resolution = models.CharField(max_length=4)
    duration_in_seconds = models.IntegerField()
    video = models.FileField(upload_to=str, null=True, blank=True)

    def __str__(self):
        return f"STREEM | video_id: {self.pk} | origin object: {self.origin_video} | video path: {self.video}"
