from django.contrib import admin, messages
from django.utils.translation import ngettext

from video.models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'pk',  'video', 'status']
