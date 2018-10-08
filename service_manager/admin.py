from django.contrib import admin
from .models import *


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('villa', 'start_day', 'end_day', 'notes', 'allow_stacking')



