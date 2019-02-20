from django import forms

from django.contrib.auth.models import User
from kwikeeapp.models import Business, Item

class UserForm(forms.ModelForm):
    email = forms.CharField(max_length = 100, required = True)      # validates data length
    password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email")

class UserFormForEdit(forms.ModelForm):
    email = forms.CharField(max_length = 100, required = True)      # validates data length

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ("name", "phone", "address", "logo")

class ItemForm(forms.ModelForm):                    # Make sure all declared classes are named correctly in each file
    class Meta:
        model = Item
        exclude = ("business",)
