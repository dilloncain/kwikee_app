import json

from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from oauth2_provider.models import AccessToken

from kwikeeapp.models import Business, Item, Order, OrderDetails, Driver
from kwikeeapp.serializers import BusinessSerializer, \
    ItemSerializer, \
    OrderSerializer

import stripe
from kwikee.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


############
# CUSTOMERS
############

def customer_get_businesses(request):
    businesses = BusinessSerializer(
        Business.objects.all().order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"businesses": businesses})

def customer_get_items(request, business_id):
    items = ItemSerializer(
        Item.objects.filter(business_id = business_id).order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"items": items})


@csrf_exempt
def customer_add_order(request):
    """
        params:
            access_token
            businesses_id
            address
            order_details (json format), example:
                [{"item_id": 1, "quantity": 2},{"item_id": 2, "quantity": 3}]
            stripe_token

        return:
            {"status": "success"}
    """

    if request.method == "POST":
        # Get access_token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        # Get profile
        customer = access_token.user.customer

        # Get Stripe token
        stripe_token = request.POST["stripe_token"]

        # Check whether customer has any order that is not delivered/rendered
        if Order.objects.filter(customer = customer).exclude(status = Order.DELIVERED):
            return JsonResponse({"status": "fail", "error": "Your last order must be completed."})

        # Check Address/Location
        if not request.POST["address"]:
            return JsonResponse({"status": "failed", "error": "Address is required."})

        # Get Order Details
        order_details = json.loads(request.POST["order_details"])

        order_total = 0
        for item in order_details:
            order_total += Item.objects.get(id = item["item_id"]).price * item["quantity"]

        if len(order_details) > 0:

            # Step 1 - Create a charge: this will charge a customer's card
            charge = stripe.Charge.create(
                amount = order_total * 100, # Amount in cents
                currency = "usd",
                source = stripe_token,
                description = "Kwikee Order"
            )

            if charge.status != "failed":
                # Step 2 - Create an Order
                order = Order.objects.create(
                customer = customer,
                business_id = request.POST["business_id"],
                total = order_total,
                status = Order.PROCESSING,
                address = request.POST["address"]
                )

                # Step 3 - Create Order Details
                for item in order_details:
                    OrderDetails.objects.create(
                        order = order,
                        item_id = item["item_id"],
                        quantity = item["quantity"],
                        sub_total = Item.objects.get(id = item["item_id"]).price * item["quantity"]
                    )

                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "failed", "error": "Failed to connect to Stripe."})





def customer_get_latest_order(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer
    order = OrderSerializer(Order.objects.filter(customer = customer).last()).data  # last order of the customer in the database

    return JsonResponse({"order": order})   # return in Json format

def customer_driver_location(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer

    # Get driver's location related to this customer's current order.
    current_order = Order.objects.filter(customer = customer, status = Order.ONTHEWAY).last()       # Satisfy this condition
    location = current_order.driver.location                                                        # location of driver

    return JsonResponse({"location": location})     # Returns location with update





############
# BUSINESS
############

def business_order_notification(request, last_request_time):
    notification = Order.objects.filter(business = request.user.business,
        created_at__gt = last_request_time).count()     # Python syntax for > is __gt

    #select count(*) from Orders
    #where business = request.user.business AND created_at > last_request_time

    return JsonResponse({"notification": notification}) # Passes the time of the order created and then passes total back

############
# DRIVERS  (General API for driver using mobile app)
############

def driver_get_ready_orders(request):           # transforms python data into Json data
    orders = OrderSerializer(
        Order.objects.filter(status = Order.READY, driver = None).order_by("-id"),
        many = True
    ).data

    return JsonResponse({"orders": orders})

@csrf_exempt    # allows driver to post request, to pick up an order
# POST
# params: access_token, order_id
def driver_pick_orders(request):
    if request.method == "POST":
        # Get AccessToken
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        # Get DRIVER
        driver = access_token.user.driver

        # Check if driver can only pick up one order at the same time
        if Order.objects.filter(driver = driver).exclude(status = Order.ONTHEWAY):
            return JsonResponse({"status": "failed", "error": "You can only pick one order at the same time."})

        try:
            order = Order.objects.get(
                id = request.POST["order_id"],
                driver = None,
                status = Order.READY
            )
            order.driver = driver
            order.status = Order.ONTHEWAY
            order.picked_at = timezone.now()
            order.save()

            return JsonResponse({"status": "success"})

        except Order.DoesNotExist:
            return JsonResponse({"status": "failed", "error": "This order has been picked up by another."})


    return JsonResponse({})

# GET params: access_token
def driver_get_latest_orders(request):
    # Get AccessToken
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver
    order = OrderSerializer(           # Python database into Json format
        Order.objects.filter(driver = driver).order_by("picked_at").last()          # All orders in database and pick last only then
    ).data

    return JsonResponse({"order": order})


# POST params: access_token, order_id
@csrf_exempt
def driver_complete_orders(request):
        # Get AccessToken
    access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver

    order = Order.objects.get(id = request.POST["order_id"], driver = driver)       # Get order in database
    order.status = Order.DELIVERED
    order.save()

    return JsonResponse({"status": "success"})

# GET params: access_token
def driver_get_revenue(request):
    # Get AccessToken
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver

    from datetime import timedelta

    revenue = {}
    today = timezone.now()
    current_weekdays = [today + timedelta(days = i) for i in range(0 - today.weekday(), 7 - today.weekday())]   # Return current_weekdays

    for day in current_weekdays:
        orders = Order.objects.filter(
            driver = driver,
            status = Order.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )

        revenue[day.strftime("%a")] = sum(order.total for order in orders)

    return JsonResponse({"revenue": revenue})

# POST - params: access_token, "lat,lng"
@csrf_exempt
def driver_update_location(request):
    if request.method == "POST":
    # Get AccessToken
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        driver = access_token.user.driver

        # Set location string => database
        driver.location = request.POST["location"]
        driver.save()

        return JsonResponse({"status": "success"})
