from .tools import villa_services_names, preaty_services_names, ServiceDetail
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib import auth
from .models import *
from django.contrib.auth import logout as django_logout


def index(request):
    return render(request, 'index.html')


def add_item_form(request):
    success = 0

    if request.method == 'POST':
        success = 1
        new_item_name = request.POST['item_name']
        new_item_quantity = request.POST['item_quantity']
        new_item_price = request.POST['item_price']
        new_item_total_price = int(new_item_quantity) * int(new_item_price)
        try:
            old_item = Item.objects.get(storage=StorageRoom.objects.get(pk=1), item_name=new_item_name,
                                        item_price=new_item_price)
        except Item.DoesNotExist:
            old_item = None
        if old_item:
            old_item.item_quantity += int(new_item_quantity)
            old_item.item_total_price = int(old_item.item_quantity) * int(old_item.item_price)
            old_item.save()
        else:
            item = Item.objects.create(item_name=new_item_name,
                                       item_quantity=new_item_quantity,
                                       item_price=new_item_price,
                                       item_total_price=new_item_total_price,
                                       storage=StorageRoom.objects.get(pk=1))
            StorageRoom.objects.get(pk=1).storage_items.add(item)
    ctx = {'success': success}
    if 'SubmitAndNew' in request.POST:
        return render(request, 'add_item_form.html', ctx)
    elif 'SubmitToIndex' in request.POST:
        return redirect(index)
    else:
        return render(request, 'add_item_form.html', ctx)


def storage_details(request, storage_id):
    storage = StorageRoom.objects.get(pk=storage_id)
    items = Item.objects.filter(storage=storage)
    services = Service.objects.filter(storage=storage)
    services.order_by("-date")
    reports = VillaReports.objects.filter(villa=storage)
    success = 0
    if request.method == "POST":
        if request.POST.get('delete_items'):
            quantity_to_delete = request.POST['item_quantity']
            success = 1
            item_to_delete = Item.objects.get(pk=int(request.POST['item_id']))
            if int(quantity_to_delete) >= int(item_to_delete.item_quantity):
                item_to_delete.delete()
                quantity_to_delete = str(max(int(quantity_to_delete), int(item_to_delete.item_quantity)))
            else:
                item_to_delete.item_quantity = str(int(item_to_delete.item_quantity) - int(quantity_to_delete))

            Report.objects.create(item=item_to_delete,
                                  storage_from=StorageRoom.objects.get(
                                      storage_name=item_to_delete.storage.storage_name),
                                  storage_to="DELETED",
                                  person=request.user.username,
                                  quantity=quantity_to_delete)
        else:
            service_to_add = request.POST['ServiceSelect']
            service_price = request.POST['service_price']
            Service.objects.create(type=service_to_add,
                                   storage=storage,
                                   price=service_price)

    """service_details_list = []
    for index, service_name in enumerate(villa_services_names):
        service_details_list.append(ServiceDetail(service_name, preaty_services_names[index], storage))
    """
    ctx = {'storage': storage,
           'items': items,
           'success': success,
           'services': services,
           'reports': reversed(reports)
           # 'service_details_list': service_details_list
           }

    return render(request, 'storage_details.html', ctx)


def add_storage_form(request):
    success = 0
    storages = StorageRoom.objects.all()
    ctx = {}
    ctx.update({'storages': storages})
    if request.method == 'POST':
        success = 1
        new_storage_name = request.POST['storage_name']
        storage_link = request.POST['storage_link']

        StorageRoom.objects.create(storage_name=new_storage_name, link=storage_link)
    ctx.update({'success': success})
    if 'SubmitAndNew' in request.POST:
        return render(request, 'add_storage_form.html', ctx)
    elif 'SubmitToIndex' in request.POST:
        return redirect(index)
    else:
        return render(request, 'add_storage_form.html', ctx)


def transport_item(request, item_id):
    item_to_transport = Item.objects.get(pk=item_id)
    success = 0
    """for stor in StorageRoom.objects.all():
        if item_to_transport.storage == stor:
            storage_from = stor"""
    storage_from = item_to_transport.storage
    if request.method == 'POST':
        success = 1
        quantity_to_transport = request.POST['item_quantity']
        storage_to = StorageRoom.objects.get(storage_name=request.POST['storage_to_name'])
        Report.objects.create(item=item_to_transport.item_name,
                              storage_from=StorageRoom.objects.get(storage_name=storage_from.storage_name),
                              storage_to=storage_to.storage_name,
                              person=str(request.POST['person_name']),
                              quantity=quantity_to_transport)
        item_price = item_to_transport.item_price
        try:
            old_item = Item.objects.get(item_name=item_to_transport, storage=storage_to)
        except Item.DoesNotExist:
            old_item = None
        if old_item is not None:
            old_item.item_quantity += int(quantity_to_transport)
            old_item.item_total_price += int(old_item.item_quantity) * int(old_item.item_price)
            old_item.save()
        else:
            item = Item.objects.create(item_name=item_to_transport.item_name,
                                       item_quantity=quantity_to_transport,
                                       item_price=item_price,
                                       item_total_price=int(item_price) * int(quantity_to_transport),
                                       storage=storage_to)
            storage_to.storage_items.add(item)
            storage_to.save()
        if int(quantity_to_transport) == int(item_to_transport.item_quantity):
            Item.objects.get(pk=item_to_transport.id).delete()
        else:
            item_to_transport.item_quantity -= int(quantity_to_transport)
            item_to_transport.item_total_price -= int(quantity_to_transport) * int(item_price)
            item_to_transport.save()

    storages = StorageRoom.objects.all()
    ctx = {'storage_from': storage_from,
           'storages': storages,
           'item_to_transport': item_to_transport,
           'success': success}
    return render(request, 'transport_item.html', ctx)


def storage_list(request):
    storages = StorageRoom.objects.all()
    items = Item.objects.all()
    ctx = {'storages': storages,
           'items': items}

    return render(request, 'storage_list.html', ctx)


def report(request):
    reports = Report.objects.all()

    ctx = {'reports': reports}

    return render(request, 'report.html', ctx)


def delete_item(request, item_id):
    item_to_delete = Item.objects.get(pk=item_id)
    storage_id = Item.objects.get(pk=item_id).storage.id

    if request.method == "POST":
        quantity_to_transport = request.POST['item_quantity']
        storage_from = item_to_delete.storage
        storage_to = "DELETED"
        Report.objects.create(item=item_to_delete.item_name,
                              storage_from=StorageRoom.objects.get(storage_name=storage_from.storage_name),
                              storage_to=storage_to,
                              person=str(request.POST['person_name']),
                              quantity=quantity_to_transport)

        item_to_delete.delete()
        return redirect(storage_details, storage_id=storage_id)
    ctx = {'item_to_delete': item_to_delete}
    return render(request, 'delete_item.html', ctx)


def search(request):
    if request.is_ajax():
        q = request.GET.get('q')
        if q is not None:
            items = Item.objects.filter(
                Q(item_name__contains=q))
            storages = StorageRoom.objects.filter(
                Q(storage_name__contains=q))
            storage_items = Item.objects.all()
            ctx = {

                'items': items,
                'storages': storages,
                'storage_items': storage_items
            }

            return render(request, 'results.html', ctx)


def report_search(request):
    if request.is_ajax():
        q = request.GET.get('q')
        revers = request.GET.get('rev')
        if q is not None:
            items = Report.objects.filter(
                Q(storage_to__contains=q) |
                Q(date__year__contains=q) |
                Q(date__month__contains=q) |
                Q(date__day__contains=q) |
                Q(person__contains=q))
            if int(revers) == 1:
                items = items.order_by("-date")
            ctx = {
                'items': items,
            }

            return render(request, 'report_result.html', ctx)


def login(request):
    """Shows a login form and a registration link."""

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/")

        else:
            return HttpResponse("Invalid login. Please try again.")

    # if not POST then return login form
    return render(request, "login.html", {'next': ''})


def search_storages(request):
    if request.is_ajax():
        q = request.GET.get('q')
        if q is not None:
            storages = StorageRoom.objects.filter(
                Q(storage_name__contains=q))
            ctx = {
                'storages': storages,
            }

            return render(request, 'search_storages.html', ctx)


def financial_storage_list(request):
    storages = StorageRoom.objects.all()
    ctx = {'storages': storages}

    return render(request, 'financial_storage_list.html', ctx)


def financial_villa_info(request, storage_id):
    villa = StorageRoom.objects.get(pk=storage_id)
    service_details_list = []
    for index, service_name in enumerate(villa_services_names):
        service_details_list.append(ServiceDetail(service_name, preaty_services_names[index], villa))
    ctx = {'service_details_list': service_details_list}
    if request.method == "POST":
        if 'Submit' in request.POST:
            service_to_add = request.POST['ServiceSelect']
            service_price = request.POST['service_price']
            Service.objects.create(type=service_to_add,
                                   storage=villa,
                                   price=service_price)
            return HttpResponseRedirect('/financial_villa_info/{}'.format(storage_id))
    return render(request, 'financial_villa_info.html', ctx)


def add_service_for_storage(request, storage_id):
    storage = StorageRoom.objects.get(pk=storage_id)
    services = ServiceType.objects.all()

    ctx = {'storage': storage,
           'services': services,
           }

    if request.method == 'POST':
        service_name = str(request.POST['ServiceSelect'])
        service_to_add = ServiceType.objects.get(name=service_name)
        service_price = float(request.POST['ServicePrice'])
        Service.objects.create(type=service_to_add,
                               storage=storage,
                               price=service_price)

        return HttpResponseRedirect('/storage/{}'.format(storage_id))

    return render(request, 'add_service_for_storage.html', ctx)


def add_service(request):
    if request.method == 'POST':
        exists = ServiceType.objects.filter(name=request.POST['ServiceName'])
        if not exists:
            ServiceType.objects.create(name=request.POST['ServiceName'])
        return redirect(index)

    ctx = {}

    return render(request, 'add_service.html', ctx)


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')
