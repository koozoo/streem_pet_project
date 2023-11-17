from django.contrib import admin, messages
from django.utils.translation import ngettext

from tags.models import Tags


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    ordering = ["title"]
    actions = ["make_published"]
    prepopulated_fields = {"slug": ("title",)}

    @admin.action(description="Отметить теги на публикацию")
    def make_published(self, request, queryset):
        updated = queryset.update(status="p")

        self.message_user(
            request,
            ngettext(
                "%d Тег/ов успешно опубликован/ы",
                "%d stories were successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

