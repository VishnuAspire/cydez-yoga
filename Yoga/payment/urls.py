from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings

urlpatterns = [
    path('createorder',views.create_order,name="createorder"),
    path('order_status',views.payment_status,name="order_status"),
    path('create_appoinment',views.create_appoinment,name="create_appoinment"),
    path('appoinment_status',views.appoinment_status,name="appoinment_status")
]