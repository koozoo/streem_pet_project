from django.contrib import admin, messages
from django.utils.translation import ngettext
from tv_shows import models as shows_models
from video.models import Video


class ShowsItemInline(admin.TabularInline):
    model = shows_models.ShowsItem
    verbose_name = 'ВСЕ СЕРИИ'


class ShowsAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'category_id']
    list_per_page = 10
    search_fields = ['title']
    list_filter = ['status']
    ordering = ["title"]
    actions = ["make_published"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        ShowsItemInline,
    ]

    @admin.action(description="Отметить сериал на публикацию")
    def make_published(self, request, queryset):
        updated = queryset.update(status="p")

        self.message_user(
            request,
            ngettext(
                "%d сериалы успешно опубликованы",
                "%d stories were successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


class ShowsItemAdmin(admin.ModelAdmin):
    list_display = ['shows_id', 'season', 'series', 'title']
    list_per_page = 10
    ordering = ["shows_id"]


admin.site.register(shows_models.Shows, ShowsAdmin)
admin.site.register(shows_models.ShowsItem, ShowsItemAdmin)