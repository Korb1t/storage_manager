from datetime import date, timedelta
from django.shortcuts import render
from .models import *
from .forms import *
from storage_manager.models import *
from django.views import View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .render import Render


def book_villa_form(request, villa_id):
    success = 0
    form = BookVilla
    villa = StorageRoom.objects.get(pk=villa_id)
    villa_planing = Booking.objects.get(villa=villa)
    ctx = {'villa_planing': villa_planing, 'form': form}
    if request.method == 'POST':
        Booking.objects.create(villa=villa,
                               start_date=datetime.datetime.strptime(request.POST['arrival_date'],
                                                                     '%Y-%m-%d').timestamp(),
                               end_date=datetime.datetime.strptime(request.POST['arrival_date'], '%Y-%m-%d').date(),
                               notes=request.POST['notes'])
    return render(request, 'book_villa_form.html', ctx)


class GenerateVillaReport(View):

    def get(self, request, villa_id):
        storage = StorageRoom.objects.get(pk=villa_id)
        ctx = {'storage' : storage}
        return render(request, "generate_villa_prev_month_report.html", ctx)

    def post(self, request, villa_id):
        self.villa = StorageRoom.objects.get(pk=villa_id)
        today = date.today()
        this_month = today.replace(day=1)
        prev_month = (this_month - timedelta(days=1)).replace(day=1)
        total_income = request.POST['total_income']
        month_nights = int((this_month - timedelta(days=1)).strftime("%d"))
        month_number = int((this_month - timedelta(days=1)).strftime("%m"))
        month_name = (this_month - timedelta(days=1)).strftime("%B")
        year = int((this_month - timedelta(days=1)).strftime("%Y"))
        ocupied_nights = request.POST['occupied_nights']
        ocupancy = float("{0:.2f}".format((float(ocupied_nights) / float(month_nights)) * 100))
        avarange_monthly_price = float("{0:.2f}".format(float(total_income) / float(ocupied_nights)))
        total_expenses = self.get_expenses(prev_month, this_month)

        profit = float(total_income) - total_expenses
        try:
            report = VillaReports.objects.get(villa=self.villa, month=month_number, year=year)
        except VillaReports.DoesNotExist:
            report = None
        if report:
            report.villa = self.villa
            report.income = total_income
            report.expenses = total_expenses
            report.occupancy = ocupancy
            report.profit = profit
            report.average_price = avarange_monthly_price
            report.month = month_number
            report.month_name = month_name
            report.year = year
            report.save()

        else:
            VillaReports.objects.create(villa=self.villa,
                                        income=total_income,
                                        expenses=total_expenses,
                                        occupancy=ocupancy,
                                        profit=profit,
                                        average_price=avarange_monthly_price,
                                        month=month_number,
                                        month_name=month_name,
                                        year=year)
        if 'SubmitAndNew' in request.POST:
            return HttpResponseRedirect('/storage/{}'.format(villa_id))
        if 'SubmitAndPDF' in request.POST:
            return HttpResponseRedirect('/storage/pdf_report/{}/{}/{}'.format(villa_id, month_number, year))

    def get_expenses(self, date_from, date_to):
        services = Service.objects.filter(storage=self.villa, date__range=[date_from, date_to])
        extences = 0
        for service in services:
            extences += service.price
        return extences


class VillaReportPdf(View):
    def get(self, request, villa_id, month, year):
        villa = StorageRoom.objects.get(pk=villa_id)
        report = VillaReports.objects.get(villa=villa, month=month, year=year)
        params = {'today': timezone.now(),
                  'report': report,
                  'request': request}
        return Render.render('villa_report_pdf_template.html', params)


class EditService(View):

    def get(self, request, storage_id, service_id):
        service = Service.objects.get(pk=service_id)
        storage = StorageRoom.objects.get(pk=storage_id)
        services = ServiceType.objects.all()

        ctx = {'storage': storage,
               'services': services,
               }
        return render(request, "add_service_for_storage.html", ctx)

    def post(self, request, storage_id, service_id):
        service = Service.objects.get(pk=service_id)
        service.price = float(request.POST['ServicePrice'])
        service.type = ServiceType.objects.get(name=str(request.POST['ServiceSelect']))
        service.save()
        return HttpResponseRedirect("/storage/{}".format(storage_id))

# class VillaServiceExctence:
#     def __init__(self, villa, service_type):
#         self.service_name = service_type.name
#         self.price = sum(i.price for i in Service.objects.filter(storage=villa, type=service_type))
