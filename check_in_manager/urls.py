from django.urls import path
from .views import *

urlpatterns = [
    path('orders_table/', index, name='orders_table'),
    path('accept_decline_order_list', accept_decline_order_list),
    path('create_new_order/', create_new_order),
    path('order_list/order/<int:pk>', order_detail),
    path('send_variants/<int:order_id>+<int:count>', send_variants),
    path('order_pdf/<int:order_id>', order_pdf),
    path('offer_pdf/<int:order_id>', offer_pdf),
    path('accept_pdf/<int:order_id>', accept_pdf),
    path('add_new_sources/', add_new_source),
    path('add_new_occasions/', add_new_occasion),
    path('add_new_call/<int:pk>', add_call_notes),
    path('order_list/order/<int:order_id>/edit/', edit_order),
]
