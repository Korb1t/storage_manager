from django.db import models
from datetime import datetime
from django.contrib.auth.models import *
from storage_manager.models import *


class Booking(models.Model):
    villa = models.ForeignKey(StorageRoom, null=True, blank=True, on_delete=models.CASCADE)
    start_day = models.DateField()
    end_day = models.DateField(u'Day of moving', help_text=u'Day of moving')
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)
    allow_stacking = models.BooleanField(default=False)

    class Meta:
        db_table = 'Booking'
