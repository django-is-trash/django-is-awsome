from django.contrib import admin

from moneybook.models import Moneybook


@admin.register(Moneybook)
class BlogAdmin(admin.ModelAdmin):
    ...