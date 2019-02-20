from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Business(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business')    # defines one owner and cascade deletes owner and user
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='business_logo/', blank=False)

    def __str__(self):
        return self.name        # Returns name of business instead of id of business object (address works from above)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.get_full_name()    # get_full_name function comes from User model imported from django

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Item(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE) # adds uniqueness to each item if there are duplicates
    name = models.CharField(max_length=500)
    short_description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='item_images/', blank=False)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    PROCESSING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4

    STATUS_CHOICES = (
        (PROCESSING, "Processing"),
        (READY, "Ready"),
        (ONTHEWAY, "On the way"),
        (DELIVERED, "Delivered"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, blank = True, null = True, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    total = models.FloatField()
    status = models.IntegerField(choices = STATUS_CHOICES)
    created_at = models.DateTimeField(default = timezone.now)
    picked_at = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return str(self.id)     # returns to integer

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, related_name='order_details', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sub_total = models.FloatField()

    def __str__(self):
        return str(self.id)
