from django.contrib import admin
from .models import Town
from .models import Village
from .models import Group


@admin.register(Town)
class TownInformation(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = (
        'name',
    )


@admin.register(Village)
class VillageInformation(admin.ModelAdmin):
    list_display = (
        'name',
        'town',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'town',
    )


@admin.register(Group)
class GroupInformation(admin.ModelAdmin):
    list_display = (
        'name',
        'village',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'village',
    )

