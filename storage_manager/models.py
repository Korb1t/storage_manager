from django.db import models
from datetime import datetime


class StorageRoom(models.Model):
    storage_name = models.CharField(max_length=255, blank=True, null=True)
    storage_items = models.ManyToManyField('Item', blank=True)
    order_villa_price = models.PositiveIntegerField(null=True, blank=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'StorageRoom'

    def __str__(self):
        return self.storage_name


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    item_quantity = models.IntegerField(default=0)
    item_price = models.FloatField(default=0)
    item_total_price = models.FloatField(default=0)
    item_adding_date = models.DateTimeField(default=datetime.now, blank=True)
    storage = models.ForeignKey(StorageRoom, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Items'

    def __str__(self):
        return self.item_name

    def __float__(self):
        return self.item_quantity, self.item_price, self.item_total_price


class Report(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    storage_from = models.ForeignKey(StorageRoom, related_name='storage_from', null=True, blank=True, on_delete=models.CASCADE)
    storage_to = models.CharField(max_length=255, blank=True, null=True)
    person = models.CharField(max_length=255, blank=True, null=True)
    item = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'Report'

    def __str__(self):
        return self.person


class ServiceType(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)

    class Meta:
        db_table = 'Service type'

    def __str__(self):
        return self.name


class Service(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    storage = models.ForeignKey(StorageRoom, related_name='storage', null=True, blank=True, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    type = models.ForeignKey(ServiceType, related_name='type', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Service'

    def __str__(self):
        template = 'Type: {}.type for villa: {}.storage.storage_name'
        return template.format(self)


class VillaReports(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    villa = models.ForeignKey(StorageRoom, related_name='villa', null=True, blank=True, on_delete=models.CASCADE)
    income = models.FloatField(default=0)
    expenses = models.FloatField(default=0)
    occupancy = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    average_price = models.FloatField(default=0)
    month_nights = 0
    month_name = models.TextField(default='May', max_length=20)
    month = models.IntegerField(default=0)
    year = models.IntegerField(default=0)

    class Meta:
        db_table = 'VillaReport'

    def __str__(self):
        return self.villa.storage_name

    def __float__(self):
        return self.income, self.expenses, self.occupancy




