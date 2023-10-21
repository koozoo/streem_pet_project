from django.contrib import admin, messages
from django.utils.translation import ngettext
from movie.models import Movie, ActorMovie


# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'category_id']
    search_fields = ['title']
    ordering = ["title"]
    actions = ["make_published"]
    prepopulated_fields = {"slug": ("title",)}

    @admin.action(description="Отметить фильм на публикацию")
    def make_published(self, request, queryset):
        updated = queryset.update(status="p")

        self.message_user(
            request,
            ngettext(
                "%d фильмов успешно опубликованы",
                "%d stories were successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


class ActorMovieAdmin(admin.ModelAdmin):
    list_display = ['movie_id', 'actor_id']
    ordering = ["movie_id"]


admin.site.register(Movie, MovieAdmin)
admin.site.register(ActorMovie, ActorMovieAdmin)
