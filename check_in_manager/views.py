from datetime import timedelta, date

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .render import Render
from .models import *
from datetime import datetime
from django.utils.dateparse import parse_date


def index(request):
    alerts = get_alerts(request)
    if request.user.is_superuser:
        orders = reversed(Order.objects.all())
    else:
        orders = reversed(Order.objects.filter(creator_name_id=request.user.id))

    ctx = {
        'orders': orders,
        'inclusions': Inclusions.objects.all(),
        'notes': Notes.objects.all(),
        'users': User.objects.all(),
        'villas': StorageRoom.objects.exclude(pk=1),
        'alerts': alerts[0],
        'alerts_count': alerts[1],
        'call_alerts': alerts[2]
    }
    if request.method == 'POST':
        if request.POST.get('from_date') and request.POST.get('to_date'):
            orders = Order.objects.filter(
                check_in_date__range=(request.POST.get('from_date'), request.POST.get('to_date')))
            ctx['orders'] = orders
    return render(request, 'check_in_manager/index.html', ctx)


def accept_decline_order_list(request):
    alerts = get_alerts(request)
    today = datetime.today()
    if request.user.is_superuser:
        orders = Order.objects.filter(check_out_date__gte=today)
    else:
        orders = Order.objects.filter(creator_name_id=request.user.id, check_out_date__gte=today)
    villas = StorageRoom.objects.all()
    mx = orders.order_by("-id")[0]
    mn = orders.order_by("id")[0]
    ctx = {
        'orders': orders,
        'villas': villas,
        'alerts': alerts[0],
        'alerts_count': alerts[1],
        'call_alerts': alerts[2],
        'max' : mx,
        'min' : mn
    }

    if request.method == 'POST':
        number = 0
        for i in range(1, Order.objects.last().id + 1):
            if request.POST.get('DeclineReason' + str(i)) is not None or request.POST.get(
                    'OrderVilla' + str(i)) is not None:
                number = i
                break
        if number != 0:
            if request.POST.get('DeclineReason' + str(number)) is not None:
                order = Order.objects.get(pk=number)
                order.decline_reason = request.POST.get(
                    'DeclineReason' + str(number))
                order.declined_by_client = True
                order.accepted = False
                order.save()
            if request.POST.get('OrderVilla' + str(number)) is not None:
                order = Order.objects.get(pk=number)
                order.chosen_villa = StorageRoom.objects.get(
                    storage_name=request.POST.get('OrderVilla' + str(number)))
                order.accepted_by_client = True
                order.accepted = False
                order.balance = request.POST.get('Balance')
                order.price = request.POST.get('Price')
                order.save()
    return render(request, 'check_in_manager/order_list.html', ctx)


def order_detail(request, pk):
    alerts = get_alerts(request)
    order = Order.objects.get(pk=pk)
    order_calls = Calls.objects.filter(order=order)
    should_be_alerted = Order.objects.filter(pk=pk, alerted=False, check_in_date=date.today() + timedelta(days=1),
                                             creator_name_id=request.user.id).first()

    ctx = {
        'order': order,
        'inclusions': Inclusions.objects.all(),
        'notes': Notes.objects.all(),
        'alerts': alerts[0],
        'alerts_count': alerts[1],
        'call_alerts': alerts[2],
        'should_be_alerted': should_be_alerted,
        'order_calls': order_calls
    }
    if request.method == 'POST':
        if request.POST.get("add_call") is not None:
            return HttpResponseRedirect("/check_in_manager/add_new_call/{}".format(pk))
        if request.POST.get("alert_done") is not None and should_be_alerted:
            should_be_alerted.alerted = True
            should_be_alerted.save()
            return HttpResponseRedirect("/check_in_manager/order_list/order/{}".format(pk))
    return render(request, 'check_in_manager/order_detail.html', ctx)


def create_new_order(request):
    sources = Source.objects.all()
    occasions = SpecOccasion.objects.all()
    alerts = get_alerts(request)
    if request.method == 'POST':
        source = Source.objects.filter(source_name=request.POST.get('Source'))
        if source.count():
            source = source[0]
        else:
            source = None
        spec_ocas = SpecOccasion.objects.filter(spec_occasion_name=request.POST.get('SpecOccasion'))
        if spec_ocas.count():
            spec_ocas = spec_ocas[0]
        else:
            spec_ocas = None
        if request.POST.get('EarlyCheckIn') is not None:
            early_check = True
        else:
            early_check = False

        if request.POST.get('LateCheckOut') is not None:
            late_check = True
        else:
            late_check = False

        gn = request.POST['GuestName']
        gcn = request.POST['GuestCellNumber']
        cid = parse_date(request.POST['CheckInDate'])

        for st in Order.objects.all():
            if st.guest_name == gn and st.guest_cell_number == gcn and st.check_in_date == cid:
                ctx = {'sources': sources,
                       'occasions': occasions,
                       'alerts': alerts[0],
                       'alerts_count': alerts[1],
                       'call_alerts': alerts[2],
                       'success': 0}
                return render(request, 'check_in_manager/create_new_order.html', ctx)

        new_order = Order.objects.create(
            creator_name=request.user,
            guest_name=request.POST['GuestName'],
            guest_cell_number=request.POST['GuestCellNumber'],
            guest_email=request.POST['GuestEmail'],
            guest_watsapp=request.POST['GuestWhatsApp'],
            check_in_date=request.POST['CheckInDate'],
            check_out_date=request.POST['CheckOutDate'],
            early_check_in_required=early_check,
            late_check_out_required=late_check,
            number_of_adults=request.POST['NumberOfAdults'],
            number_of_kids_below_5=request.POST['NumberOfKids'],
            source=source,
            spec_occasion=spec_ocas,
            waiting_for_manager=True,
            accepted=False,
            accepted_by_client=False,
            offer=None,
            comment=request.POST['Comment']
        )

        Notes.objects.create(
            note=request.POST['Notes'],
            order=new_order,
        )

        Inclusions.objects.create(
            inclusion=request.POST['Inclusions'],
            order=new_order,
        )
        return HttpResponseRedirect("/check_in_manager/create_new_order/")
    ctx = {'sources': sources,
           'occasions': occasions,
           'alerts': alerts[0],
           'alerts_count': alerts[1],
           'call_alerts': alerts[2],
           'success': 1}
    return render(request, 'check_in_manager/create_new_order.html', ctx)


def send_variants(request, order_id, count):
    villas = StorageRoom.objects.exclude(pk=1)
    order = Order.objects.get(pk=order_id)
    rng = range(1, count + 1)
    alerts = get_alerts(request)
    ctx = {'villas': villas,
           'alerts': alerts[0],
           'alerts_count': alerts[1],
           'call_alerts': alerts[2],
           'range': rng
           }
    if request.method == 'POST':
        villa1name = request.POST.get('Villa1Name')
        villa2name = request.POST.get('Villa2Name')
        villa3name = request.POST.get('Villa3Name')
        villa4name = request.POST.get('Villa4Name')
        if villa2name:
            villa2 = StorageRoom.objects.get(
                storage_name=request.POST.get('Villa2Name'))
        else:
            villa2 = None

        if villa3name:
            villa3 = StorageRoom.objects.get(
                storage_name=request.POST.get('Villa3Name'))
        else:
            villa3 = None

        if villa4name:
            villa4 = StorageRoom.objects.get(
                storage_name=request.POST.get('Villa4Name'))
        else:
            villa4 = None

        new_offer = Offer.objects.create(
            villa1=StorageRoom.objects.get(
                storage_name=request.POST.get('Villa1Name')),
            price_per_night1=request.POST.get('Villa1Price'),
            tax1=request.POST.get('Villa1Tax'),
            villa2=villa2,
            price_per_night2=request.POST.get('Villa2Price'),
            tax2=request.POST.get('Villa2Tax'),
            villa3=villa3,
            price_per_night3=request.POST.get('Villa3Price'),
            tax3=request.POST.get('Villa3Tax'),
            villa4=villa4,
            price_per_night4=request.POST.get('Villa4Price'),
            tax4=request.POST.get('Villa4Tax'),
        )
        order.offer = new_offer
        order.waiting_for_manager = False
        order.accepted = True
        order.save()

    return render(request, 'check_in_manager/send_variants.html', ctx)


def order_pdf(request, order_id):
    order = Order.objects.get(pk=order_id)
    alerts = get_alerts(request)
    ctx = {
        'order': order,
        'alerts': alerts[0],
        'alerts_count': alerts[1]
    }
    return Render.render('check_in_manager/order_pdf.html', ctx)


def offer_pdf(request, order_id):
    alerts = get_alerts(request)
    order = Order.objects.get(pk=order_id)
    offer = Offer.objects.get(pk=order_id)
    ctx = {
        'order': order,
        'offer': offer,
        'alerts': alerts[0],
        'alerts_count': alerts[1]
    }
    return Render.render('check_in_manager/offer_pdf.html', ctx)


def accept_pdf(request, order_id):
    alerts = get_alerts(request)
    order = Order.objects.get(pk=order_id)
    ctx = {
        'order': order,
        'alerts': alerts[0],
        'alerts_count': alerts[1]
    }
    return Render.render('check_in_manager/accept_pdf.html', ctx)


def get_alerts(request):

    if request.user.is_superuser:
        arrive_soon = Order.objects.filter(alerted=False, check_in_date=date.today() + timedelta(days=1))

    else:
        arrive_soon = Order.objects.filter(alerted=False, check_in_date=date.today() + timedelta(days=1),
                                           creator_name_id=request.user.id)
    call_alerts = get_call_alerts(request)
    return arrive_soon, arrive_soon.count() + len(call_alerts), call_alerts


def get_call_alerts(request):
    call_alerts = []
    if request.user.is_superuser:
        active_orders = Order.objects.filter(check_in_date__lt=datetime.today())

    else:
        active_orders = Order.objects.filter(check_in_date__lt=datetime.today(),
                                             creator_name_id=request.user.id)
    for order in active_orders:
        if not Calls.objects.filter(order=order, date_of_call__gte=datetime.today() - timedelta(days=10)):
            call_alerts.append(order)
    return call_alerts


def add_new_source(request):
    success = 0
    alerts = get_alerts(request)
    if request.method == 'POST':
        Source.objects.create(
            source_name=request.POST['source_name']
        )
        return HttpResponseRedirect("/check_in_manager/add_new_sources/")
    ctx = {
        'success': success,
        'alerts': alerts[0],
        'alerts_count': alerts[1]
    }
    return render(request, 'check_in_manager/add_new_source.html/', ctx)


def add_new_occasion(request):
    alerts = get_alerts(request)
    success = 0
    if request.method == 'POST':
        SpecOccasion.objects.create(
            spec_occasion_name=request.POST['occasion_name']
        )
        return HttpResponseRedirect("/check_in_manager/add_new_occasions/")
    ctx = {
        'success': success,
        'alerts': alerts[0],
        'alerts_count': alerts[1]
    }
    return render(request, 'check_in_manager/add_new_spec_occasion.html/', ctx)


def add_call_notes(request, pk):
    alerts = get_alerts(request)
    if request.method == "POST":
        notes = request.POST.get("notes")
        order = Order.objects.get(pk=pk)
        Calls.objects.create(message=notes, order=order)
        return HttpResponseRedirect("/check_in_manager/order_list/order/{}".format(pk))
    ctx = {'alerts': alerts[0],
           'alerts_count': alerts[1]}

    return render(request, 'check_in_manager/add_new_call.html/', ctx)


def edit_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_inclusion = Inclusions.objects.get(order=Order.objects.get(pk=order_id))
    order_note = Notes.objects.get(order=Order.objects.get(pk=order_id))
    order_check_in_date = order.check_in_date.strftime('%Y-%m-%d')
    order_check_out_date = order.check_out_date.strftime('%Y-%m-%d')
    sources = Source.objects.all()
    spec_occasions = SpecOccasion.objects.all()
    ctx = {
        'order': order,
        'order_inclusion': order_inclusion,
        'order_note': order_note,
        'order_check_in_date': order_check_in_date,
        'order_check_out_date': order_check_out_date,
        'sources': sources,
        'spec_occasions': spec_occasions
    }
    if request.method == 'POST':
        order.guest_name = request.POST['order_guest_name']
        order.guest_cell_number = request.POST['order_guest_cell_number']
        order.guest_email = request.POST['order_guest_email']
        order.guest_watsapp = request.POST['order_guest_watsapp']
        order.check_in_date = request.POST['order_check_in_date']
        order.check_out_date = request.POST['order_check_out_date']
        order.number_of_adults = request.POST['order_number_of_adults']
        order.number_of_kids_below_5 = request.POST['order_number_of_kids_below_5']
        order.source.source_name = request.POST['order_source_name']
        order.spec_occasion.spec_occasion_name = request.POST['order_special_occasion']
        order_inclusion.inclusion = request.POST['order_inclusion']
        order_note.note = request.POST['order_note']
        order.price = request.POST['order_price']
        order.balance = request.POST['order_balance']
        order.comment = request.POST['order_comment']
        if request.POST.get('order_early_check_in_required') is not None:
            order.early_check_in_required = True
        else:
            order.early_check_in_required = False

        if request.POST.get('order_late_check_out_required') is not None:
            order.late_check_out_required = True
        else:
            order.late_check_out_required = False
        order.save()
        order_inclusion.save()
        order_note.save()
        return HttpResponseRedirect("/check_in_manager/order_list/order/{}/edit/".format(order_id))
    return render(request, 'check_in_manager/edit.html', ctx)
