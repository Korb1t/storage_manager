from django import forms
from .models import Order


class CreateOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'guest_name',
            'guest_cell_number',
            'guest_email',
            'guest_watsapp',
            'check_in_date',
            'check_out_date',
            'early_check_in_required',
            'late_check_out_required',
            'number_of_adults',
            'number_of_kids_below_5',
            'source',
            'spec_occasion',
            'comment')