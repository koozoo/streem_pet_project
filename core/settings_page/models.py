from django.db import models


STATUS_CHOICES = [
    ("d", "Draft"),
    ("p", "Published"),
    ("w", "Withdrawn"),
]

BLOCK_TYPE = [
    ("b", "banner"),
    ("m", "media_block"),
]


class PageBlock(models.Model):
    title = models.CharField(max_length=150)
    type = models.CharField(max_length=1, choices=BLOCK_TYPE, default='m')
    priority = models.PositiveIntegerField(default=1)
    data_filter = models.JSONField()
    block_title = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')


class SettingsPage(models.Model):
    title = models.CharField(max_length=150)
    blocks = models.ManyToManyField(to=PageBlock)
    meta = models.JSONField()
    ads = models.JSONField()
    keyword = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
