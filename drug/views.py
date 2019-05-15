from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError
from django.db.models import Sum, Q, Count
from datetime import date, timedelta
import datetime

from .models import Drug_resource, Staff_resource, Order, Ordered_drug, Ordered_staff, Days_of_emchilgee, Doctor_review, Costumer_review, Drug, Drug_order, Drug_order_status, Drug_important, Emchilgee, Onosh, History, Worker, Costumer
from .forms import OrderForm, Ordered_drugForm, Ordered_staffForm, Drug_create_form, Drug_important_form, Emchilgee_form, OnoshForm, HistoryForm
import pprint

# Create your views here.
@login_required
def staff_order(request, id):
    ordered_staff = get_object_or_404(Ordered_staff, id=id)
    pprint.pprint(ordered_staff.qty)
    staff_resource = get_object_or_404(Staff_resource, staff=ordered_staff.staff)
    pprint.pprint(staff_resource.qty)
    return redirect('drug:drug_order')

@login_required
def staff_distribute(request, id):
    ordered_staff = get_object_or_404(Ordered_staff, id=id)
    pprint.pprint(ordered_staff.qty)
    staff_resource = get_object_or_404(Staff_resource, staff=ordered_staff.staff)
    pprint.pprint(staff_resource.qty)
    return redirect('drug:drug_order')

@login_required
def drug_order(request, template_name='drug/drug_order.html'):
    context = {}
    order = Order.objects.all()
    ordered_drug = Ordered_drug.objects.all()
    ordered_staff = Ordered_staff.objects.all()
    drug_resource = Drug_resource.objects.all()
    staff_resource = Staff_resource.objects.all()

    Ordered_drugFormset = modelformset_factory(Ordered_drug, form=Ordered_drugForm)
    Ordered_staffFormset = modelformset_factory(Ordered_staff, form=Ordered_staffForm)

    form = OrderForm(request.POST or None, initial={'worker': request.user.worker})
    formset1 = Ordered_drugFormset(request.POST or None, queryset = Ordered_drug.objects.none(), prefix='ordered_drug')
    formset2 = Ordered_staffFormset(request.POST or None, queryset = Ordered_staff.objects.none(), prefix='ordered_staff')

    if request.method == "POST":
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.save()

                    if formset1.is_valid():
                        for ordered_drug in formset1:
                            data = ordered_drug.save(commit=False)
                            if data.drug != None and data.qty != None:
                                data.order = order
                                data.save()

                    if formset2.is_valid():
                        for ordered_staff in formset2:
                            pprint.pprint(ordered_staff)
                            data = ordered_staff.save(commit=False)
                            pprint.pprint(data.staff)
                            pprint.pprint(data.qty)
                            if data.staff != None and data.qty != None:
                                data.order = order
                                data.save()

            except IntegrityError:
                print("Error Encountered")

            return redirect('drug:drug_order')

    context['staff_resource'] = staff_resource
    context['drug_resource'] = drug_resource
    context['order'] = order
    context['formset2'] = formset2
    context['formset1'] = formset1
    context['form'] = form
    return render(request, template_name, context)

@login_required
def drug_detail(request, template_name='drug/drug_detail.html'):
    data = {}
    drug_detail = Drug.objects.all()
    form = Drug_create_form(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('drug:drug_detail')

    data['drug_detail'] = drug_detail
    data['form'] = form
    return render(request, template_name, data)

@login_required
def emchilgee_create(request, template_name='drug/emchilgee_create.html'):
    context = {}
    emchilgee = Emchilgee.objects.all()
    drug_important = Drug_important.objects.all()

    Drug_important_formset = modelformset_factory(Drug_important, form=Drug_important_form)

    form = Emchilgee_form(request.POST or None)
    formset2 = Drug_important_formset(request.POST or None, queryset = Drug_important.objects.none(), prefix='drug_important')

    if request.method == "POST":
        if form.is_valid():
            try:
                with transaction.atomic():
                    emchilgee = form.save(commit=False)
                    emchilgee.save()

                    if formset2.is_valid():
                        for drug_important in formset2:
                            data1 = drug_important.save(commit=False)
                            data1.emchilgee = emchilgee
                            data1.save()

            except IntegrityError:
                print("Error Encountered")

            return redirect('drug:emchilgee_create')

    context['emchilgee'] = emchilgee
    context['formset2'] = formset2
    context['form'] = form
    return render(request, template_name, context)

@login_required
def onosh_create(request, template_name='drug/onosh_create.html'):
    context = {}
    OnoshFormset = modelformset_factory(Onosh, form=OnoshForm)

    formset1 = OnoshFormset(request.POST or None, queryset = Onosh.objects.none(), prefix='onosh')

    if request.method == "POST":
        if formset1.is_valid():
            try:
                with transaction.atomic():
                    for onosh in formset1:
                        data = onosh.save(commit=False)
                        data.save()

            except IntegrityError:
                print("Error Encountered")

            return redirect('drug:onosh_list')

    context['formset1'] = formset1
    return render(request, template_name, context)

@login_required
def onosh_list(request, template_name='drug/onosh_list.html'):

    onosh = Onosh.objects.all()

    data = {}
    data['onosh'] = onosh

    return render(request, template_name, data)

@login_required
def history_create(request, template_name='drug/history_create.html'):
    context = {}
    HistoryFormset = modelformset_factory(History, form=HistoryForm)

    formset1 = HistoryFormset(request.POST or None, queryset = History.objects.none(), prefix='history')

    if request.method == "POST":
        if formset1.is_valid():
            try:
                with transaction.atomic():
                    for history in formset1:
                        data = history.save(commit=False)
                        data.save()

            except IntegrityError:
                print("Error Encountered")

            return redirect('drug:history_list')

    context['formset1'] = formset1
    return render(request, template_name, context)

@login_required
def history_list(request, template_name='drug/history_list.html'):

    history = History.objects.all()

    data = {}
    data['history'] = history

    return render(request, template_name, data)

@login_required
def review_details(request, id):
    data = {}
    days = []
    result = {}
    temp_result = []
    button = True
    today = date.today()
    emchilgee = get_object_or_404(Emchilgee, id=id)
    costumer = Costumer.objects.filter(user=emchilgee.costumer)
    count_day = emchilgee.count_days()

    day_of_emchilgee = Days_of_emchilgee.objects.filter(emchilgee = emchilgee)

    if request.method == "POST":
        emchilgee_id = request.POST.get('emchilgee')
        emchilgee = get_object_or_404(Emchilgee, id=emchilgee_id)

        day_of_emchilgee = Days_of_emchilgee()
        day_of_emchilgee.emchilgee = emchilgee
        day_of_emchilgee.day = today
        day_of_emchilgee.is_done = True
        day_of_emchilgee.save()

    template_name='drug/review_details.html'
    for done in emchilgee.days_of_emchilgee_set.all():
        if done.day == today:
            button = False
            break

    for x in range(count_day):
        days.append(emchilgee.start_date + timedelta(days=x))
        temp = emchilgee.start_date + timedelta(days=x)
        if emchilgee.days_of_emchilgee_set.all():
            for done in emchilgee.days_of_emchilgee_set.all():
                pprint.pprint("****")
                pprint.pprint(temp)
                pprint.pprint('-----------')
                pprint.pprint(done.day)
                pprint.pprint('****')
                if done.day == temp:
                    result[x] = "✔"
                    temp_result.append("✔")
                    break
                else:
                    if temp < today:
                        result[x] = "✘"
                        temp_result.append("✘")
                    elif temp == today:
                        result[x] = "?"
                        temp_result.append("?")
                    else:
                        result[x] = "*"
                        temp_result.append("*")
        else:
            if temp < today:
                result[x] = "✘"
                temp_result.append("✘")
            elif temp == today:
                result[x] = "?"
                temp_result.append("?")
            else:
                result[x] = "*"
                temp_result.append("*")

    pprint.pprint(result)

    data['button'] = button
    data['result'] = result
    data['today'] = today
    data['days'] = days
    data['costumer'] = costumer
    data['emchilgee'] = emchilgee

    return render(request, template_name, data)

@login_required
def emchilgee_details(request, id):
    data = {}
    emchilgee = get_object_or_404(Emchilgee, id=id)
    costumer = Costumer.objects.filter(user=emchilgee.costumer)

    template_name='drug/emchilgee_details.html'
    data['costumer'] = costumer
    data['emchilgee'] = emchilgee

    return render(request, template_name, data)

@login_required
def emchilgee_list(request, template_name='drug/emchilgee_list.html'):
    data = {}
    temp = []
    today = date.today()
    emchilgee = Emchilgee.objects.filter(worker = request.user.worker)
    drug_important = Drug_important.objects.all()
    for item in emchilgee:
        if item.end_date > today:
            temp.append(item)

    emchilgee = temp
    data['drug_important'] = drug_important
    data['emchilgee'] = emchilgee

    return render(request, template_name, data)

@login_required
def emchilgee_list_done(request, template_name='drug/emchilgee_list_done.html'):
    data = {}
    temp = []
    today = date.today()
    emchilgee = Emchilgee.objects.filter(worker = request.user.worker)
    drug_important = Drug_important.objects.all()
    for item in emchilgee:
        if item.end_date < today:
            temp.append(item)

    emchilgee = temp
    data['drug_important'] = drug_important
    data['emchilgee'] = emchilgee

    return render(request, template_name, data)

@login_required
def all_emchilgee_list(request, template_name='drug/all_emchilgee_list.html'):
    data = {}
    temp = []
    today = date.today()
    doctor_review = Doctor_review.objects.all()
    emchilgee = Emchilgee.objects.all()
    for item in emchilgee:
        if item.end_date < today:
            temp.append(item)

    emchilgee = temp
    data['doctor_review'] = doctor_review
    data['emchilgee'] = emchilgee

    return render(request, template_name, data)

@login_required
def costumer_emchilgee_list(request, template_name='drug/costumer_emchilgee_list.html'):
    data = {}
    temp = []
    today = date.today()
    costumer_review = Costumer_review.objects.all()
    emchilgee = Emchilgee.objects.filter(costumer=request.user.costumer)
    for item in emchilgee:
        if item.end_date < today:
            temp.append(item)

    emchilgee = temp
    data['costumer_review'] = costumer_review
    data['emchilgee'] = emchilgee

    return render(request, template_name, data)

@login_required
def add_recived_date(request, id):
    drug_order = get_object_or_404(Drug_order,id=id)
    drug_order.recived_date = date.today()
    drug_order.save()
    return redirect('drug:drug_order')

@login_required
def reviews(request, template_name='drug/reviews.html'):
    data = {}
    temp = []
    days = []
    today = date.today()
    doctor_review = Doctor_review.objects.all()
    costumer_review = Costumer_review.objects.all()
    emchilgee = Emchilgee.objects.filter(worker = request.user.worker)

    data['costumer_review'] = costumer_review
    data['doctor_review'] = doctor_review
    data['emchilgee'] = emchilgee

    return render(request, template_name, data)

@login_required
def make_review_1(request, emchilgee_id):
    if request.user.is_worker:
        rsp = Doctor_review.objects.filter(emchilgee = emchilgee_id)
        if not rsp:
            doctor_review = Doctor_review()

            doctor_review.emchilgee = emchilgee_id
            doctor_review.doctor = request.user.worker
            doctor_review.review = 1
            doctor_review.save()
            return redirect('drug:all_emchilgee_list')
        else:
            doctor_review = get_object_or_404(Doctor_review, emchilgee = emchilgee_id)

            doctor_review.doctor = request.user.worker
            doctor_review.review = 1
            doctor_review.save()
            return redirect('drug:all_emchilgee_list')
    else:
        rsp = Costumer_review.objects.filter(emchilgee = emchilgee_id)
        if not rsp:
            costumer_review = Costumer_review()

            costumer_review.emchilgee = emchilgee_id
            costumer_review.costumer = request.user.costumer
            costumer_review.review = 1
            costumer_review.save()
            return redirect('drug:costumer_emchilgee_list')
        else:
            costumer_review = get_object_or_404(Costumer_review, emchilgee = emchilgee_id)

            costumer_review.costumer = request.user.costumer
            costumer_review.review = 1
            costumer_review.save()
            return redirect('drug:costumer_emchilgee_list')

@login_required
def make_review_2(request, emchilgee_id):
    if request.user.is_worker:
        rsp = Doctor_review.objects.filter(emchilgee = emchilgee_id)
        if not rsp:
            doctor_review = Doctor_review()

            doctor_review.emchilgee = emchilgee_id
            doctor_review.doctor = request.user.worker
            doctor_review.review = 2
            doctor_review.save()
            return redirect('drug:all_emchilgee_list')
        else:
            doctor_review = get_object_or_404(Doctor_review, emchilgee = emchilgee_id)

            doctor_review.doctor = request.user.worker
            doctor_review.review = 2
            doctor_review.save()
            return redirect('drug:all_emchilgee_list')
    else:
        rsp = Costumer_review.objects.filter(emchilgee = emchilgee_id)
        if not rsp:
            costumer_review = Costumer_review()

            costumer_review.emchilgee = emchilgee_id
            costumer_review.costumer = request.user.costumer
            costumer_review.review = 2
            costumer_review.save()
            return redirect('drug:costumer_emchilgee_list')
        else:
            costumer_review = get_object_or_404(Costumer_review, emchilgee = emchilgee_id)

            costumer_review.costumer = request.user.costumer
            costumer_review.review = 2
            costumer_review.save()
            return redirect('drug:costumer_emchilgee_list')

@login_required
def make_review_3(request, emchilgee_id):
    if request.user.is_worker:
        rsp = Doctor_review.objects.filter(emchilgee = emchilgee_id)
        if not rsp:
            doctor_review = Doctor_review()

            doctor_review.emchilgee = emchilgee_id
            doctor_review.doctor = request.user.worker
            doctor_review.review = 3
            doctor_review.save()
            return redirect('drug:all_emchilgee_list')
        else:
            doctor_review = get_object_or_404(Doctor_review, emchilgee = emchilgee_id)

            doctor_review.doctor = request.user.worker
            doctor_review.review = 3
            doctor_review.save()
            return redirect('drug:all_emchilgee_list')
    else:
        rsp = Costumer_review.objects.filter(emchilgee = emchilgee_id)
        if not rsp:
            costumer_review = Costumer_review()

            costumer_review.emchilgee = emchilgee_id
            costumer_review.costumer = request.user.costumer
            costumer_review.review = 3
            costumer_review.save()
            return redirect('drug:costumer_emchilgee_list')
        else:
            costumer_review = get_object_or_404(Costumer_review, emchilgee = emchilgee_id)

            costumer_review.costumer = request.user.costumer
            costumer_review.review = 3
            costumer_review.save()
            return redirect('drug:costumer_emchilgee_list')

@login_required
def make_review_4(request, emchilgee_id):
    if request.user.is_worker:
        rsp = Doctor_review.objects.filter(emchilgee = emchilgee_id)
        if not rsp:
            doctor_review = Doctor_review()

            doctor_review.emchilgee = emchilgee_id
            doctor_review.doctor = request.user.worker
            doctor_review.review = 4
            doctor_review.save()
            return redirect('drug:all_emchilgee_list')
        else:
            doctor_review = get_object_or_404(Doctor_review, emchilgee = emchilgee_id)

            doctor_review.doctor = request.user.worker
            doctor_review.review = 4
            doctor_review.save()
            return redirect('drug:all_emchilgee_list')
    else:
        rsp = Costumer_review.objects.filter(emchilgee = emchilgee_id)
        if not rsp:
            costumer_review = Costumer_review()

            costumer_review.emchilgee = emchilgee_id
            costumer_review.costumer = request.user.costumer
            costumer_review.review = 4
            costumer_review.save()
            return redirect('drug:costumer_emchilgee_list')
        else:
            costumer_review = get_object_or_404(Costumer_review, emchilgee = emchilgee_id)

            costumer_review.costumer = request.user.costumer
            costumer_review.review = 4
            costumer_review.save()
            return redirect('drug:costumer_emchilgee_list')

@login_required
def make_review_5(request, emchilgee_id):
    if request.user.is_worker:
        rsp = Doctor_review.objects.filter(emchilgee = emchilgee_id)
        if not rsp:
            doctor_review = Doctor_review()

            doctor_review.emchilgee = emchilgee_id
            doctor_review.doctor = request.user.worker
            doctor_review.review = 5
            doctor_review.save()
            return redirect('drug:all_emchilgee_list')
        else:
            doctor_review = get_object_or_404(Doctor_review, emchilgee = emchilgee_id)

            doctor_review.doctor = request.user.worker
            doctor_review.review = 5
            doctor_review.save()
            return redirect('drug:all_emchilgee_list')
    else:
        rsp = Costumer_review.objects.filter(emchilgee = emchilgee_id)
        if not rsp:
            costumer_review = Costumer_review()

            costumer_review.emchilgee = emchilgee_id
            costumer_review.costumer = request.user.costumer
            costumer_review.review = 5
            costumer_review.save()
            return redirect('drug:costumer_emchilgee_list')
        else:
            costumer_review = get_object_or_404(Costumer_review, emchilgee = emchilgee_id)

            costumer_review.costumer = request.user.costumer
            costumer_review.review = 5
            costumer_review.save()
            return redirect('drug:costumer_emchilgee_list')
