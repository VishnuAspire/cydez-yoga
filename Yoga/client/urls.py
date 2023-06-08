from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from rest_framework.authtoken.views  import obtain_auth_token




urlpatterns = [
    path('login', views.CustomAuthToken.as_view(),name='login'),
    ### dashboard login ###
    path('adminlogin', views.adminlogin,name='login_admin'),
    path('dashboard',views.deshboard,name="dashboard"),
    path('addDepartment',views.addDepartment,name="addDepartment"),
    path('updateDepartment/<int:departmentid>',views.updateDepartment,name="updateDepartment"),
    path('deleteDepartment<int:departmentid>',views.deleteDepartment,name="deleteDepartment"),
    path('searchDepartment',views.searchDepartment,name='searchDepartment'),
    path('addDoctor',views.addDoctor,name="addDoctor"),
    path('updateDoctor/<int:doctorid>',views.updateDoctor,name="updateDoctor"),
    path('deleteDoctor<int:doctorid>',views.deleteDoctor,name="deleteDoctor"),
    path('searchDoctor',views.searchDoctor,name='searchDoctor'),
    ### customer APIView ###
    path('customer_registeration', views.addcustomer, name='addcustomer'),
    path('showall_customer',views.showall_customer,name='showall_customer'),
    path('update/<int:userid>',views.update_customer,name='update_customer'),
    path('delete/<int:userid>',views.delete_customer,name='delete_customer'),
    path('customer/<int:userid>',views.retrive_customer,name='retrive_customer'),
    path('check-user', views.checkUser, name='checkUser'),
    path('userreset-password', views.userResetPasword, name='checkUser'),
    ### log out apiview ###
    path('logoutview',views.logoutview,name='logoutview'),
    ## dashboard logout
    path('logout',views.logoutadmin,name='logout'),
    ### Appoinment APIViews ###
    path('showallappoinment',views.showallAppoinment,name="showallappoinment"),
    path('deleteappoinment/<int:userid>',views.deleteAppoinment,name='deleteappoinment'),
    path('createAppoinment',views.createAppoinment,name="createAppoinment"),
    path('updateAppoinment/<int:appoinmentid>',views.updateAppoinment,name="updateAppoinment"),
    ### pdf ###
    path('show_details/<int:id>',views.ShowDetails,name="show_details"),
    path('pdf/<int:id>',views.GeneratePDF,name='pdf'),
    path('accept',views.accept,name='accept'),
    path('account',views.Account,name='account'),

    ### front-end ###
    path('',views.home,name="home"),
    path('<int:error>',views.home,name="home2"),
    path('about_us',views.about,name="about_us"),
    path('contact',views.contact,name='contact'),

    path('specialoffers',views.specialoffers,name="specialoffers"),
    path('pricedetails',views.pricedetails,name="pricedetails"),
    path('userRegister',views.userRegister,name='userRegister'),
    path('userLogin',views.userLogin,name="userlogin"),
    path('userLogin/<int:flag>',views.userLogin,name="userlogin2"),
    path('userLogin/1',views.userLogin,name="userlogin3"),
    path('resetpassword', views.ResetPasword, name='reset_password'),
    path('logoutuser',views.logoutuser,name='logoutuser'),
    path('requestAppoinment',views.requestAppoinment,name="appoinment"),
    path('orders',views.orders,name='orders'),
    path('appoinments',views.appoinment_filter,name='appoinments'),
    
    
]

