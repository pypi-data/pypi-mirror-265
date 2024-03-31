from django.contrib import admin

from .models import Clock


@admin.register(Clock)
class ClockAdmin(admin.ModelAdmin):
    pass
