"""storage_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views import *
from service_manager.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('add_item_form', add_item_form, name="add_item_form"),
    path('add_storage_form', add_storage_form, name="add_storage_form"),
    path('transport_item/item_id=<int:item_id>',
         transport_item, name="transport_item"),
    path('storage/<int:storage_id>', storage_details, name="storage_details"),
    path('storage_list', storage_list, name="storage_list"),
    path('login', login, name="login"),
    path('logout/', logout, name='logout'),
    path('report', report, name="report"),
    path('search', search, name="search"),
    path('report_search', report_search, name='report_search'),
    path('search_storages', search_storages, name="search_storages"),
    path('check_in_manager/', include('check_in_manager.urls')),
    path('financial_storage_list', financial_storage_list,
         name="financial_storage_list"),
    path('financial_villa_info/<int:storage_id>',
         financial_villa_info, name="financial_villa_info"),
    path('add_service_stor/<int:storage_id>',
         add_service_for_storage, name='add_service_for_storage'),
    path('add_service', add_service, name='add_service'),
    path('book_villa/<int:villa_id>', book_villa_form, name="book_villa_form"),
    path('generate_prev_month_report/<int:villa_id>',
         GenerateVillaReport.as_view()),
    path('storage/pdf_report/<int:villa_id>/<int:month>/<int:year>',
         VillaReportPdf.as_view()),
    path('storage/<int:storage_id>/<int:service_id>', EditService.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, documet_root=settings.STATIC_ROOT)
