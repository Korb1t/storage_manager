from django import forms

from .models import *


class BookVilla(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ('start_day', 'end_day', 'notes')