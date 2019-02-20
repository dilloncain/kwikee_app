from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from kwikeeapp.forms import UserForm, BusinessForm, UserFormForEdit, ItemForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User         # User model from django
from kwikeeapp.models import Item, Order, Driver

from django.db.models import Sum, Count, Case, When

# Redirect import funtions render and redirect
# Create your views here.

def home(request):
    return redirect(business_home)

def obtain_auth_token(request):
    return redirect(business_home)

@login_required(login_url='/business/sign-in/')   # Login required to access business homepage
def business_home(request):
    return redirect(business_order)      # DO NOT FORGET COMMAS ='(

@login_required(login_url='/business/sign-in/')
def business_account(request):
    user_form = UserFormForEdit(instance = request.user)
    business_form = BusinessForm(instance = request.user.business)

    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance = request.user)
        business_form = BusinessForm(request.POST, request.FILES, instance = request.user.business)

        if user_form.is_valid() and business_form.is_valid():
            user_form.save()
            business_form.save()

    return render(request, 'business/account.html', {
        "user_form": user_form,
        "business_form": business_form
    })      # DO NOT FORGET COMMAS ='(

@login_required(login_url='/business/sign-in/')   # Login required to access business item
def business_item(request):
    items = Item.objects.filter(business = request.user.business).order_by("-id")       #
    return render(request, 'business/item.html', {"items": items})      # Pass to frontend

@login_required(login_url='/business/sign-in/')   # Login required to access business item
def business_add_item(request):
    form = ItemForm()

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES) # upload image for item

        if form.is_valid():
            item = form.save(commit=False) # Create item object but don't save in database yet... in memory
            item.business = request.user.business # returns to user
            item.save()                         # save to database
            return redirect(business_item)  # returns to business if all correct

    return render(request, 'business/add_item.html', {
        "form": form        # pass into this variable
    })      # DO NOT FORGET COMMAS ='(

@login_required(login_url='/business/sign-in/')   # Login required to access business item
def business_edit_item(request, item_id):
    form = ItemForm(instance = Item.objects.get(id = item_id))      # Get items from database

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance = Item.objects.get(id = item_id)) # upload image for item

        if form.is_valid():
            form.save()                        # save to database
            return redirect(business_item)  # returns to business if all correct

    return render(request, 'business/edit_item.html', {
        "form": form        # pass into this variable
    })      # DO NOT FORGET COMMAS ='(


@login_required(login_url='/business/sign-in/')   # Login required to access business order
def business_order(request):
    if request.method == "POST":
        order = Order.objects.get(id = request.POST["id"], business = request.user.business)

        if order.status == Order.PROCESSING:
            order.status = Order.READY
            order.save()

    orders = Order.objects.filter(business = request.user.business).order_by("-id")     # Get all orders from database with condition business = user
    return render(request, 'business/order.html', {"orders": orders})      # Pass to front end # DO NOT FORGET COMMAS ='(

@login_required(login_url='/business/sign-in/')   # Login required to access business report
def business_report(request):
    # Calculate revenue and number of order by current week
    from datetime import datetime, timedelta

    revenue = []
    orders = []

    # Calculate weekdays
    today = datetime.now()
    current_weekdays = [today + timedelta(days = i) for i in range(0 - today.weekday(), 7 - today.weekday())]   # Return current_weekdays

    for day in current_weekdays:
        delivered_orders = Order.objects.filter(
            business = request.user.business,
            status = Order.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )
        revenue.append(sum(order.total for order in delivered_orders))
        orders.append(delivered_orders.count())


    # Top 3 Items
    top3_items = Item.objects.filter(business = request.user.business)\
                        .annotate(total_order = Sum('orderdetails__quantity'))\
                        .order_by("-total_order")[:3]


    item = {
        "labels": [item.name for item in top3_items],
        "data": [item.total_order or 0 for item in top3_items]
    }

    # Top 3 DRIVERS
    top3_drivers = Driver.objects.annotate(
        total_order = Count(
            Case (
                When(order__business = request.user.business, then = 1)     #
            )
        )
    ).order_by("-total_order")[:3]

    driver = {
        "labels": [driver.user.get_full_name() for driver in top3_drivers],
        "data": [driver.total_order for driver in top3_drivers]
    }

    return render(request, 'business/report.html', {
        "revenue": revenue,
        "orders": orders,
        "item": item,
        "driver": driver
    })      # DO NOT FORGET COMMAS ='(

def business_sign_up(request):
    user_form = UserForm()
    business_form = BusinessForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)        # data from user form
        business_form = BusinessForm(request.POST, request.FILES)   # Allow logo upload with request.FILES and data from business form

        if user_form.is_valid() and business_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)   # Transform to python type clean (business owner)
            new_business = business_form.save(commit = False)           # Create new business object in memory
            new_business.user = new_user                                  # Assign new user to business
            new_business.save()                                           # Saves

            login(request, authenticate(
                username = user_form.cleaned_data["username"],          # Forgot comma (fixed)
                password = user_form.cleaned_data["password"]
            ))

            return redirect(business_home)

    return render(request, 'business/sign_up.html', {
        "user_form": user_form,
        "business_form": business_form
    })
