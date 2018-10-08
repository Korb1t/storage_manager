from django.contrib.auth.models import AbstractUser
from django.db import models
from storage_manager.models import StorageRoom


class User(AbstractUser):

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'Users'


class Source(models.Model):
    source_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.source_name

    class Meta:
        db_table = 'Source'


class SpecOccasion(models.Model):
    spec_occasion_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.spec_occasion_name


class Offer(models.Model):
    villa1 = models.ForeignKey(
        StorageRoom, on_delete=models.CASCADE, related_name='villa1')
    price_per_night1 = models.IntegerField()
    tax1 = models.IntegerField()
    villa2 = models.ForeignKey(
        StorageRoom, on_delete=models.CASCADE, related_name='villa2', blank=True, null=True)
    price_per_night2 = models.IntegerField(blank=True, null=True)
    tax2 = models.IntegerField(blank=True, null=True)
    villa3 = models.ForeignKey(
        StorageRoom, on_delete=models.CASCADE, related_name='villa3', blank=True, null=True)
    price_per_night3 = models.IntegerField(blank=True, null=True)
    tax3 = models.IntegerField(blank=True, null=True)
    villa4 = models.ForeignKey(
        StorageRoom, on_delete=models.CASCADE, related_name='villa4', blank=True, null=True)
    price_per_night4 = models.IntegerField(blank=True, null=True)
    tax4 = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Offer'


class Order(models.Model):
    creator_name = models.ForeignKey(User, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=255)
    guest_cell_number = models.CharField(max_length=255)
    guest_email = models.CharField(max_length=255)
    guest_watsapp = models.CharField(max_length=255)
    check_in_date = models.DateField(auto_now_add=False)
    check_out_date = models.DateField(auto_now_add=False)
    early_check_in_required = models.BooleanField(default=False, blank=True)
    late_check_out_required = models.BooleanField(default=False, blank=True)
    number_of_adults = models.PositiveIntegerField(default=0)
    number_of_kids_below_5 = models.PositiveIntegerField(default=0)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, blank=True, null=True)
    spec_occasion = models.ForeignKey(SpecOccasion, on_delete=models.CASCADE, blank=True, null=True)
    waiting_for_manager = models.BooleanField(default=True, blank=False)
    accepted = models.BooleanField(default=False, blank=False)
    accepted_by_client = models.BooleanField(default=False, blank=False)
    declined_by_client = models.BooleanField(default=False, blank=False)
    offer = models.ForeignKey(Offer, null=True, on_delete=models.CASCADE)
    decline_reason = models.CharField(max_length=255, default=None, null=True)
    chosen_villa = models.ForeignKey(StorageRoom, on_delete=models.CASCADE, related_name='chosen_villa', default=None, null=True)
    balance = models.PositiveIntegerField(null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    alerted = models.BooleanField(default=False)
    comment = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'Order'


class Notes(models.Model):
    note = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.note

    class Meta:
        db_table = 'Notes'


class Inclusions(models.Model):
    inclusion = models.CharField(max_length=255)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.inclusion

    class Meta:
        db_table = 'Inclusions'


class Calls(models.Model):
    date_of_call = models.DateTimeField(auto_now_add=True)
    message = models.TextField(default=None, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.date_of_call

    class Meta:
        db_table = 'Calls'
