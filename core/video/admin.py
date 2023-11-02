from django.contrib import admin, messages
from django.utils.translation import ngettext

from video.models import Video, VideoForStreem


class VideoForStreemInline(admin.TabularInline):
    model = VideoForStreem
    verbose_name = 'Доступные медиа файлы'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'pk',  'video', 'status']
    inlines = [
        VideoForStreemInline,
    ]
