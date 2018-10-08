from django.contrib import admin
from .models import *



@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name', 'item_quantity', 'item_price', 'item_total_price', 'item_adding_date', 'storage')


@admin.register(StorageRoom)
class StorageRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'storage_name',)

@admin.register(Service)
class StorageRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'storage', 'price', 'type')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'item', 'quantity', 'storage_from', 'storage_to', 'person')
#
# @admin.register
# class BookingAdmin(Booking):
#     list_display = ('day', 'start_time', 'end_time', 'notes')




