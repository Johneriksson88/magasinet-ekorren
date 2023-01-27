from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .models import StorageUnit, Customer, Order
from .forms import CustomerForm, OrderForm, ContactForm, SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse_lazy
from datetime import datetime
import csv
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMessage
from django.conf import settings


def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            messages.success(
                request,
                'Thank you for contacting us! We will get back to you shortly.')
            return redirect('index')

    else:
        form = ContactForm()
    return render(request, 'index.html', {'form': form})


@login_required(login_url='login')
def user_panel(request):

    # If customer has no fullname the user has not yet filled their customer
    # information (this field cannot be left blank, hence if it's empty
    # the form has not been filled)
    # i.e. the customer is not created, then show the customer form for them
    # to fill it

    customer = Customer.objects.get(user=request.user)
    if customer.fullname.__len__() < 1:
        return redirect('customer_form')

    orders = request.user.customer.order_set.all()

    context = {'orders': orders, 'customer': customer}
    return render(request, 'user_panel.html', context)


def edit_user_info(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your information has been updated.')
            print('Updated information')
            return redirect('user_panel')
        else:
            print('Form invalid')

    else:
        form = CustomerForm(instance=customer)
    context = {'form': form}
    return render(request, 'edit_user_info.html', context)


def user_login(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('user_panel')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('user_panel')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'user_login.html')


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')


def customer_form(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your information was successfully added!")
            return redirect('user_panel')
    context = {'form': form}
    return render(request, 'customer_form.html', context)


@login_required(login_url='login')
def order_form(request):
    units = StorageUnit.objects.all().values_list('name', 'size', 'price')
    customer = Customer.objects.get(user=request.user)

    # Variables for sending confirmation email
    name = customer.fullname
    email = customer.email
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.instance.customer = customer
            new_order = form.save()
            order_id = new_order.pk
            messages.success(
                request,
                "Order successfully submitted! You will get an email confirmation shortly.")
            return redirect("user_panel")

    context = {'form': form, 'units': units}
    return render(request, 'order_form.html', context)


def register_form(request):

    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            user = form.save()
            Customer.objects.create(
                user=user
            )
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                'Account successfully created for ' +
                username)
            return redirect('user_panel')

    context = {'form': form}
    return render(request, 'register_form.html', context)


def delete_order(request, pk):
    order = Order.objects.get(pk=pk)
    customer = request.user.customer
    order_id = order.id
    if request.method == 'POST':
        order.delete()
        messages.success(request, f"Order #{order_id} successfully deleted.")
        return redirect('user_panel')
    context = {'order': order}
    return render(request, 'delete_order.html', context)


def delete_account(request, pk):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        logout(request)
        messages.info(request, 'Your account has been successfully deleted.')
        return redirect('index')
    context = {'user': user}
    return render(request, 'delete_account.html', context)


# Export customer database to a csv file

@staff_member_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow([
        'Namn',
        'Adress',
        'Postnummer',
        'Stad',
        'Email',
        'Telefon',
        'Personnr/orgnr'
    ])
    for customer in Customer.objects.all().values_list(
        'fullname',
        'address',
        'zipcode', 'city',
        'email',
        'phone',
        'person_or_org_nr'
    ):
        writer.writerow(customer)

    response['Content-Disposition'] = 'attatchment; filename="customers.csv"'
    return response


def not_registered(request):
    return render(request, 'not_registered.html')
