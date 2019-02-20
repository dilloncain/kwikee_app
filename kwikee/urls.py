"""kwikee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, reverse
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib import auth
from django.contrib.auth import views as auth_views

from kwikeeapp import views, apis

#from django.contrib.auth import login_required
#from django.contrib.auth.views import logout
#from django.contrib.auth.views import login

##from django.contrib.auth.views import LogoutView()


from django.conf.urls.static import static
from django.conf import settings

# Django auth library provides built in views for login/logout functions
# Takes care of all authentication.

##
#url(r'^login/$', views.LoginView.as_view(template_name=template_name), name='login'),
#path('login', auth_views.LoginView.as_view(template_name='accounts/login.html'))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('api-token-auth/', views.obtain_auth_token),


    # Business Area
    path('business/sign-in/', auth_views.LoginView.as_view(template_name='business/sign_in.html'), name = 'business-sign-in'),
    path('business/sign-out', auth_views.LogoutView.as_view(), name ='business-sign-out'),      # name and template_name are different! xD

    path('business/sign-up', views.business_sign_up, name='business-sign-up'),
    path('business/', views.business_home, name = 'business-home'),
    path('business/account/', views.business_account, name='business-account'),
    path('business/item/', views.business_item, name='business-item'),
    path('business/item/add/', views.business_add_item, name='business-add-item'),              # Make sure all forms have the correct name, such as ItemForm
    path('business/item/edit/<item_id>/',    # Pass parameter with pattern item_id
    views.business_edit_item, name = 'business-edit-item'),

#    path('business/item/add/', views.business_add_item, name='business-add-item'),
#    path('business/item/edit/(?P<item_id>\d+)/$', views.business_edit_item, name = 'business-edit-item'),
    path('business/order/', views.business_order, name='business-order'),
#    path('business/customer/(?P<business_id>\d+)/$', views.business_customer, name='business-cutomer'),
    path('business/report/', views.business_report, name='business-report'),


# Django auth library provides built in views for login/logout functions
# Takes care of all authentication.

## (Old style)
#url(r'^login/$', views.LoginView.as_view(template_name=template_name), name='login'),

    # Sign In/ Sign Up/ Sign Out
    path('api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign in/ sign up)
    # /revoke-token (sign out)
    path('api/business/order/notification/<last_request_time>/', apis.business_order_notification),


    # django >2.0 -- path('<int:album_id>/', views.detail, name='detail'),

    # APIs for CUSTOMERS
    path('api/customer/businesses/', apis.customer_get_businesses),
    path('api/customer/items/<business_id>/', apis.customer_get_items),
    path('api/customer/order/add/', apis.customer_add_order),
    path('api/customer/order/latest/', apis.customer_get_latest_order),
    path('api/customer/driver/location/', apis.customer_driver_location),



    # APIs for DRIVERS
    path('api/driver/orders/ready/', apis.driver_get_ready_orders),
    path('api/driver/order/pick/', apis.driver_pick_orders),
    path('api/driver/order/latest/', apis.driver_get_latest_orders),
    path('api/driver/order/complete/', apis.driver_complete_orders),
    path('api/driver/revenue/', apis.driver_get_revenue),
    path('api/driver/location/update/', apis.driver_update_location),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

















#





















#
