from django.contrib import admin, messages
from django.utils.translation import ngettext
from actor.models import Actors


@admin.register(Actors)
class ActorsAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ["name"]
    prepopulated_fields = {"slug": ("name",)}
