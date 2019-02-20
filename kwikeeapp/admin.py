from django.contrib import admin

# Register your models here.
from kwikeeapp.models import Business, Customer, Driver, Item, Order, OrderDetails

admin.site.register(Business)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderDetails)

# Customize login process
# We need to know which user is which with every new sign-up
