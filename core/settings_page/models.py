from django.db import models

from categories.models import Categories
from genre.models import Genre
from showrunner.models import Showrunner

STATUS_CHOICES = [
    ("d", "Draft"),
    ("p", "Published"),
    ("w", "Withdrawn"),
]

BLOCK_TYPE = [
    ("b", "banner"),
    ("m", "media_block")
]

COMPONENT_NAME = [
    ("banner-2", "banner-style-2"),
    ("banner-1", "banner-style-1"),
    ("banner-3", "banner-style-3"),
    ("carousel-1", "carousel-style-1"),
    ("carousel-2", "carousel-style-2"),
    ("carousel-3", "carousel-style-3"),
]


class PageBlock(models.Model):
    view_title = models.CharField(max_length=150)
    type = models.CharField(max_length=1, choices=BLOCK_TYPE, default='m')
    priority = models.PositiveIntegerField(default=1)
    block_title = models.CharField(max_length=100)
    component_name = models.CharField(max_length=100, choices=COMPONENT_NAME, default='m')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')


class PageBlockParams(models.Model):
    block_id = models.ForeignKey(to=PageBlock, on_delete=models.PROTECT)
    category_id = models.ManyToManyField(to=Categories, blank=True, null=True, verbose_name='Категории')
    showrunner_id = models.ForeignKey(to=Showrunner, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Шоураннер')
    most_views = models.BooleanField(default=False, verbose_name='Больше просмотров')
    genres = models.ManyToManyField(to=Genre, blank=True, null=True, verbose_name='Жанры')
    recently_updated = models.BooleanField(default=False, verbose_name='Недавно обновленные')
    new = models.BooleanField(default=False, verbose_name='Новинки')
    is_published = models.BooleanField(default=True)
    last_mount = models.BooleanField(default=False, verbose_name='Просмотры за последний месяц')
    last_day = models.BooleanField(default=False, verbose_name='Смотрят сейчас')
    last_week = models.BooleanField(default=False, verbose_name='Просмотры за последнюю неделю')


class SettingsPage(models.Model):
    title = models.CharField(max_length=150)
    blocks = models.ManyToManyField(to=PageBlock)
    meta = models.JSONField()
    ads = models.JSONField()
    keyword = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
