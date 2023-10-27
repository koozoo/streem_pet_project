from django.contrib import admin, messages
from django.utils.translation import ngettext
from showrunner.models import Showrunner


@admin.register(Showrunner)
class ShowrunnerAdmin(admin.ModelAdmin):
    list_display = ['title']

    prepopulated_fields = {"slug": ("title",)}

    @admin.action(description="Отметить шоуранера/ов на публикацию")
    def make_published(self, request, queryset):
        updated = queryset.update(status="p")

        self.message_user(
            request,
            ngettext(
                "%d Шоуранер/ов успешно опубликованы",
                "%d stories were successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )
