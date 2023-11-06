from django.contrib import admin, messages
from django.utils.translation import ngettext

from categories.models import Categories


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    ordering = ["title"]
    actions = ["make_published"]
    prepopulated_fields = {"slug": ("title",)}

    @admin.action(description="Отметить категорию на публикацию")
    def make_published(self, request, queryset):
        updated = queryset.update(status="p")

        self.message_user(
            request,
            ngettext(
                "%d Файлов/л  успешно опубликованы",
                "%d stories were successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )
