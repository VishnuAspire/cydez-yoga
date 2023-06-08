from django.shortcuts import render,redirect
from rest_framework.response import Response 
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from datetime import datetime, timedelta
import datetime
from django.db.models import Sum,Count
from rest_framework.decorators import api_view,permission_classes
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import auth
from rest_framework import status
import re
import random
from django.shortcuts import get_object_or_404
### models and  serializers ###
from .models import User,Appoinment,doctor,department
from .serializers import userserializer,appoinmentserializer
from program.models import program,Category,Level,banner,order
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import urllib.parse
### convert to pdf ###
from django.http import HttpResponse
from django.views.generic import View
from Yoga.utils import render_to_pdf 
from django.template.loader import get_template
### for token ###
from rest_framework.authtoken.views  import ObtainAuthToken
from  rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

import razorpay

### token based login ##
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            #'email': user.email,
            'username':user.username
        })


### customer ####


def contact(request):
    user=request.user
    if 'userids' in request.session:
        userids=request.session['userids']
        user=User.objects.get(id=userids)
    return render(request,'contact.html',{'user':user})
# @login_required
@api_view(['POST'])
def addcustomer(request):
    if request.method=='POST':
        email=request.data.get('email')
        username=request.data.get('username')
        password=request.data.get('password')
        address=request.data.get('address')
        postcode=request.data.get('postcode')
        city=request.data.get('city')
        phone=request.data.get('phone')
        dob=request.data.get('dob')
        role = request.data.get('role')
        status = request.data.get('status')
        k=User.objects.create_user(email=email,status=status,role=role,username=username,DOB=dob,password=password,address=address,postcode=postcode,city=city,phone=phone)
        ad=User.objects.filter(email=k)
        serializer=userserializer(ad,many=True)
        return Response(serializer.data)

def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

# @login_required 
@api_view(['POST'])
def checkUser(request):
    number = request.data.get('phone')
    if (isValid(number)):  
        user_data=User.objects.filter(phone=number).values()
        updateUserPassword={}
        otp=random.randint(1000,9999)
        otp=123
        message='Your OTP is '+str(otp)
        try:
            user_phone = user_data[0]['phone']
        except:
            user_phone = ''
        if user_phone:
            password=str(otp)
            password = make_password(password)
            updateUserPassword["password"]=password
            updateUserPassword["otp"]=otp
            user_data.update(**updateUserPassword )
            resp =  sendSMS('2KHSSIdPIwA-vfTHvbr0MjVZ5NaqoYXCxETpTR2vMa', number,'TXTLCL', message)
            print (resp)
            return Response({'status':"Existing User"},status=status.HTTP_200_OK)
        else:
            password=str(otp)
            print ("Registering  User")
            registerUsingPhone(number,password,otp)
            resp =  sendSMS('2KHSSIdPIwA-vfTHvbr0MjVZ5NaqoYXCxETpTR2vMa',number,'TXTLCL', message)
            return Response({'status':"Registered New User"},status=status.HTTP_200_OK)
        return Response(otp)    
    else : 
        return Response("In Valid Number")


@api_view(['POST'])
def userResetPasword(request):
    number = request.data.get('phone')
    password = request.data.get('password')
    PhoneOtp = request.data.get('otp')
    user_data=User.objects.filter(phone=number).values()
    updateUserPassword={}
 
    try:
        user_otp = str(user_data[0]['otp'])
    except:
        user_otp = 0
    if (isValid(number) and (user_otp == PhoneOtp)):  
        user_data=User.objects.filter(phone=number).values()
        updateUserPassword={}
        try:
            user_phone = user_data[0]['phone']
        except:
            user_phone = ''
        if user_phone:
            password = make_password(password)
            updateUserPassword["password"]=password
            user_data.update(**updateUserPassword )
        else:
            return Response("Not a registered user")
        return Response("Password changed successfully")    
    else : 
        return Response("In Valid Number")

def registerUsingPhone(phone,password,otp):
        registered_mobile=User.objects.create_user_phone(phone=phone,password=password,otp=otp)
        return registered_mobile

def isValid(s): 
    Pattern = re.compile("^[7-9][0-9]{9}$") 
    return Pattern.match(s) 


# @login_required
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def logoutview(request):
    logout(request)
    return Response({'status':"successfully logout"},status=status.HTTP_200_OK)

def logoutadmin(request):
	auth.logout(request)
	return redirect('login_admin')

#@login_required
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def showall_customer(request):
    User.objects.all()
    ad=User.objects.all()
    serializer=userserializer(ad,many=True)
    return Response(serializer.data)

#@login_required    
@api_view(['PUT'])
# @permission_classes([IsAuthenticated])
def update_customer(request,userid):
    k=User.objects.filter(id=userid).values()
    if request.method=='PUT':
        email=request.data.get('email')
        updatevalues={}
        if email:
            updatevalues["email"]=email
        username=request.data.get('username')
        if username:
            updatevalues["username"]=username
        address=request.data.get('address')
        if address:
            updatevalues["address"]=address
        postcode=request.data.get('postcode')
        if postcode:
            updatevalues["postcode"]=postcode
        city=request.data.get('city')
        if city:
            updatevalues["city"]=city
        phone=request.data.get('phone')
        status=request.data.get('status')
        if status:
            updatevalues["status"]=status
        role=request.data.get('role')
        if role:
            updatevalues["role"]=role
        if phone:
            updatevalues["phone"]=phone
        k.update(**updatevalues )
        ad=User.objects.filter(id=userid)
        serializer=userserializer(ad,many=True)
        return Response(serializer.data)
    return Response('please fill the form correctly')

#@login_required    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def delete_customer(request,userid):
    u=User.objects.get(id=userid)
    name=u.email
    u.delete()
    return Response("User:"+name+"is deleted")

#@login_required    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def retrive_customer(request,userid):
    ad=User.objects.filter(id=userid)
    serializer=userserializer(ad,many=True)
    return Response(serializer.data)

# @login_required
@api_view(['POST'])
def createAppoinment(request):
    if request.method=='POST':
        departments    = request.data.get('department') 
        De             = department.objects.get(id=departments)
        doctors        = request.data.get('doctor')
        Do             = doctor.objects.get(id=doctors)
        customer_id    = request.data.get('customer_id')
        d              = User.objects.get(id=customer_id)
        name           = request.data.get('name')
        phone          = request.data.get('phone')
        email          = request.data.get('email')
        address        = request.data.get('address')
        state          = request.data.get('state')
        city           = request.data.get('city')
        postcode       = request.data.get('postcode')
        comment        = request.data.get('comment')
        appoinmentdate = request.data.get('appoinmentdate')
        Appoinment.objects.create(department=De,doctor=Do,customer_id=d,name=name,phone=phone,email=email,address=address,state=state,city=city,postcode=postcode,comment=comment,appoinmentdate=appoinmentdate)
        E=Appoinment.objects.all()
        serializer=appoinmentserializer(E,many=True)
        return Response(serializer.data)

# @login_required
@api_view()
def showallAppoinment(request):
    v = Appoinment.objects.all()
    serializer = appoinmentserializer(v,many=True)
    return Response(serializer.data)

#@login_required
@api_view(['GET'])
def deleteAppoinment(request,userid):
    u = Appoinment.objects.get(id=userid)
    # name= u.username
    u.delete()
    return Response("deleted")

# @login_required
@api_view(['PUT'])
def updateAppoinment(request,appoinmentid):
    K = Appoinment.objects.filter(id=appoinmentid).values()
    if request.method=='PUT':
        departments    = request.data.get('department') 
        De             = department.objects.get(id=departments)
        doctors        = request.data.get('doctor')
        Do             = doctor.objects.get(id=doctors)
        customer_id    = request.data.get('customer_id')
        d              = User.objects.get(id=customer_id)
        name           = request.data.get('name')
        phone          = request.data.get('phone')
        email          = request.data.get('email')
        address        = request.data.get('address')
        state          = request.data.get('state')
        city           = request.data.get('city')
        postcode       = request.data.get('postcode')
        comment        = request.data.get('comment')
        appoinmentdate = request.data.get('appoinmentdate')
        K.update(department=De,doctor=Do,customer_id=d,name=name,phone=phone,email=email,address=address,state=state,city=city,postcode=postcode,comment=comment,appoinmentdate=appoinmentdate)
        E=Appoinment.objects.all()
        serializer=appoinmentserializer(E,many=True)
        return Response(serializer.data)
    return Response("Please fill the form correctly")


def adminlogin(request):
    if request.method == 'POST':
        phone    = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(request,phone=phone,password=password)
        if user:
            login(request,user)
            return redirect('dashboard')
        else:
            extra = {'popup':True,'heading':'Login Failed','msg':'Invalid credentials'}
            return render(request, "loginu.html",{'extra':extra})
    return render(request, "loginu.html")


@login_required
def deshboard(request):
    appoinments      = Appoinment.objects.all().order_by('-id')
    count   =   Appoinment.objects.filter(status="pending").count()
    total_appoinment = appoinments.count()
    registeruser     = User.objects.filter(status='Registered',is_superuser=False)
    users = registeruser.count()
    s = User.objects.filter(status='Subscriber',is_superuser=False)
    subscribers = s.count()
    orders           = order.objects.all().order_by('-id')

    page=request.GET.get('page')
    paginator=Paginator(orders,per_page=5)
    try:
        orders=paginator.page(page)
    except PageNotAnInteger:
        orders=paginator.page(1)
    except EmptyPage:
        orders=paginator.page(paginator.num_pages)

    
    paginator=Paginator(appoinments,per_page=20)
    try:
        appoinments=paginator.page(page)
    except PageNotAnInteger:
        appoinments=paginator.page(1)
    except EmptyPage:
        appoinments=paginator.page(paginator.num_pages)

    return render(request,'index.html',{'count':count,'appoinments':appoinments,'total_appoinment':total_appoinment,'users':users,'paginator':paginator,'subscribers':subscribers,'orders':orders})
    

@login_required 
def ShowDetails(request,id):
    appoinments = Appoinment.objects.get(id=id)
    return render(request,'show_details.html',{'appoinments':appoinments})

@login_required 
def GeneratePDF(request,id):
        appoinments = Appoinment.objects.get(id=id)
        template = get_template('show_details.html')
        context = {
            'appoinments':appoinments
        }
        html = template.render(context)
        pdf = render_to_pdf('show_details.html',context)
        if pdf:
            response = HttpResponse(pdf,content_type='application/pdf')
            filename= "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download= request.GET.get("download")
            if download:
                response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            return response    
        return HttpResponse("Not found")


@login_required
def accept(request):

    if 'action' in request.GET:
        appoinment_id = request.GET.get('id')
        appoinments = Appoinment.objects.get(id=appoinment_id)

        if request.GET.get('action') =='1':
            appoinments.status = 'Accepted'
            appoinments.save()
            return redirect("dashboard")

        elif request.GET.get('action') == '0':
            appoinments.status = 'Cancelled'
            appoinments.save()
            return redirect("dashboard")
        return redirect("dashboard")


def Account(request):
	return render(request,'account.html')


### front-end ###

def home(request,error=None):
    user=request.user
    if 'phone' in request.session:
        del request.session['phone']
    Categories = Category.objects.all().order_by('-id')
    k = program.objects.all()
    user_cat = []
    if 'userids' in request.session:
        userids=request.session['userids']
        user=User.objects.get(id=userids)
        for i in user.order_set.all():
            SubscriptionValidity=i.categoryid.SubscriptionValidity
            hours = SubscriptionValidity * 24   
            hours=hours-24         
            order_date=i.date
            order_time = i.time
            Starttime = datetime.datetime.combine(datetime.datetime.today(),order_time)   
            time_after = Starttime + datetime.timedelta(minutes=30)
            time_after = time_after.time()
            orderdate_ordertime = datetime.datetime.combine(order_date,time_after)
            newdate_newtime = orderdate_ordertime + timedelta(hours=hours)
            current_date_current_time = datetime.datetime.now()
            if current_date_current_time <= newdate_newtime:
                user_cat += [i.categoryid]
            else:
                i.subscribe=False
                i.save()
    if request.user.is_authenticated:
        user = request.user
        for i in user.order_set.all():
            SubscriptionValidity=i.categoryid.SubscriptionValidity
            hours = SubscriptionValidity * 24   
            hours=hours-24         
            order_date=i.date
            order_time = i.time
            Starttime = datetime.datetime.combine(datetime.datetime.today(),order_time)   
            time_after = Starttime + datetime.timedelta(minutes=30)
            time_after = time_after.time()
            orderdate_ordertime = datetime.datetime.combine(order_date,time_after)
            newdate_newtime = orderdate_ordertime + timedelta(hours=hours)
            current_date_current_time = datetime.datetime.now()
            if current_date_current_time <= newdate_newtime:
                user_cat += [i.categoryid]
            else:
                i.subscribe=False
                i.save()
    popup = False
    if error == 1:
        popup = True
    return render(request,"home/index.html",{'user':user,'Categories':Categories,'k':k,'user_cat':user_cat,'buyPopup':popup})   

def about(request):
    user=request.user
    if 'userids' in request.session:
        userids=request.session['userids']
        user=User.objects.get(id=userids)
    return render(request,"home/about.html",{'user':user})

def specialoffers(request):
    return render(request,"home/offer.html")

def pricedetails(request):
    data = Category.objects.all()
    user=request.user
    if 'userids' in request.session:
        userids=request.session['userids']
        user=User.objects.get(id=userids)
    return render(request,"home/pricedetails.html",{'user':user,'data':data})

def userRegister(request):
    if request.method=='POST':
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        email      = request.POST.get('email')
        address    = request.POST.get('address')
        postcode   = request.POST.get('postcode')
        city       = request.POST.get('city')
        phone      = request.POST.get('phone')
        password   = request.POST.get('password')
        u = 0
        try:
            u = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,address=address,postcode=postcode,city=city,phone=phone)
        except Exception as e:
            error = True
        else:
            error = False

        if u:
            login(request,u)

        if error:
            Categories = Category.objects.all()
            k = program.objects.all()
            request.session['phone']="Phone number is already used.Please use a different one."
            return render(request,"home/index.html",{'Categories':Categories,'k':k,'errorPopup':error})   
        else:
            return redirect("home")


def userLogin(request,flag=None):
    if flag:
        error = "Please login"

    if request.method=='POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(request,phone=phone,password=password)
        if user:
            login(request,user)
            return redirect('home')
        else: 
            error = "Invalid Phone number/password"   
        
    return render(request,'home/index.html',{'error':error})

def logoutuser(request):
    if 'userids' in request.session:
        del request.session['userids']
    auth.logout(request)
    return redirect('home')


def ResetPasword(request):
    if request.method =='POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        if password == confirmpassword:
            if User.objects.filter(phone=phone).exists():
                data = User.objects.get(phone=phone)
                data.set_password(password)
                data.save()
        return redirect('home')




def addDepartment(request):
    department_values = department.objects.all()
    if request.method =='POST':
        addDepartment = request.POST.get('department')
        department.objects.create(department=addDepartment)
    page=request.GET.get('page')
    paginator=Paginator(department_values,per_page=2)
    try:
       department_values=paginator.page(page)
    except PageNotAnInteger:
        department_values=paginator.page(1)
    except EmptyPage:
        department_values=paginator.page(paginator.num_pages)
        return redirect('addDepartment')
    return render(request,'addDepartment.html',{"department_values":department_values,'paginator':paginator})

def searchDepartment(request):
    results = request.POST.get('search')
    department_values = department.objects.filter(department__contains=results)
    page=request.GET.get('page')
    paginator=Paginator(department_values,per_page=5)
    try:
        department_values=paginator.page(page)
    except PageNotAnInteger:
        department_values=paginator.page(1)
    except EmptyPage:
        department_values=paginator.page(paginator.num_pages)
    return render(request,'addDepartment.html',{'department_values':department_values,'paginator':paginator})


def updateDepartment(request,departmentid):
    department_values = department.objects.filter(id=departmentid).values()
    if request.method =='POST':
        addDepartment = request.POST.get('department')
        department_values.update(department=addDepartment)
        return redirect('addDepartment')
    return render(request,'updateDepartment.html',{"department_values":department_values})


def deleteDepartment(request,departmentid):
    deleteDepartment= department.objects.get(id=departmentid)
    deleteDepartment.delete()
    return redirect('addDepartment')

def addDoctor(request):
    department_values = department.objects.all()
    doctor_values = doctor.objects.all()
    if request.method =='POST':
        addDoctor = request.POST.get('doctor')
        departmentSelected  = request.POST.get('departments') 
        De        = department.objects.get(department=departmentSelected)
        doctor.objects.create(doctor=addDoctor,department=De)
    page=request.GET.get('page')
    paginator=Paginator(doctor_values,per_page=2)
    try:
       doctor_values=paginator.page(page)
    except PageNotAnInteger:
        doctor_values=paginator.page(1)
    except EmptyPage:
        doctor_values=paginator.page(paginator.num_pages)
        return redirect('addDoctor')
    return render(request,'addDoctor.html',{"department_values":department_values,'doctor_values':doctor_values,'paginator':paginator})

def searchDoctor(request):
    results = request.POST.get('search')
    doctor_values = doctor.objects.filter(doctor__contains=results)
    page=request.GET.get('page')
    paginator=Paginator(doctor_values,per_page=5)
    try:
        doctor_values=paginator.page(page)
    except PageNotAnInteger:
        doctor_values=paginator.page(1)
    except EmptyPage:
        doctor_values=paginator.page(paginator.num_pages)
    return render(request,'addDoctor.html',{'doctor_values':doctor_values,'paginator':paginator})

def deleteDoctor(request,doctorid):
    deleteDoctor = doctor.objects.get(id=doctorid)
    deleteDoctor.delete()
    return redirect('addDoctor')

def updateDoctor(request,doctorid):
    department_values = department.objects.all()
    print(department_values)
    for i in department_values:
        print(i.id,"id  is")
    doctor_values = doctor.objects.filter(id=doctorid)
    for i in doctor_values:
        print(i.department.id,"doctor id is")
    if request.method =='POST':
        addDoctor   = request.POST.get('doctor')
        departmentSelected  = request.POST.get('departments') 
        print(departmentSelected,"depart")
        De        = department.objects.get(id=departmentSelected)
        print(De,"de")
        doctor_values.update(doctor=addDoctor,department=De)
        return redirect('addDoctor')
    return render(request,'updateDoctor.html',{"department_values":department_values,'doctor_values':doctor_values})

@csrf_exempt
def requestAppoinment(request):
    department_values = department.objects.all()
    data              = program.objects.all()
    user = request.user
    userid=user.id
    if 'userids' in request.session:
        userids=request.session['userids']
        user=User.objects.get(id=userids)
        userid=user.id
    if userid == None:
        flag = 1
        return redirect('userlogin2',flag=flag)
    else:
        if request.method=='POST':
            departments    = request.POST.get('department') 
            De             = department.objects.get(department=departments)
            doctors        = request.POST.get('doctor')
            Do             = doctor.objects.get(id=doctors) 
            name           = request.POST.get('name')
            phone          = request.POST.get('phone')
            email          = request.POST.get('email')
            address        = request.POST.get('address')
            state          = request.POST.get('state')
            city           = request.POST.get('city')
            postcode       = request.POST.get('postcode')
            comment        = request.POST.get('comment')
            appoinmentdate = request.POST.get('appoinmentdate')
            amount = 100
            order_amount = int(amount)*100
            notes = {'Shipping address':address+',\n'+state+',\n'+city+',\n'+str(postcode)}
            order_currency ="INR"
            order_receipt = str(appoinmentdate)+ Do.doctor
            client =  razorpay.Client(auth = ("rzp_live_extnBMvpztuUgO","hiAhbFBivYZNOn1oV2D7gvWz"))
            # client =  razorpay.Client(auth = ("rzp_test_qoUoBWhmPOM55N","BWs0lFVYJGVCeY2zr5KzwD4U"))    
            # CREAING ORDER
            response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='1'))
            order_id = response['id']
            order_status = response['status']
            if order_status=='created':
            # Server data for user convinience
                context = {}
                context['product_id'] = order_id
                context['price'] = amount
                context['departments'] = departments
                context['doctors'] = doctors
                context['name'] = name
                context['phone'] = phone
                context['email'] = email
                context['address'] = address
                context['city'] = city
                context['state'] = state
                context['postcode'] = postcode
                context['comment'] = comment
                context['appoinmentdate'] = appoinmentdate
                # data that'll be send to the razorpay for
                context['order_id'] = order_id
                context['product_price'] = amount
                context['date'] = appoinmentdate
                context['userid'] = userid
            return render(request,'payment/confirm-appoinment.html', context)
        if 'department' in request.GET:
            print("*****************",department)
            department_values = request.GET.get('department')
            print("@@@@@@@@@@@@@@@@@@@@",department_values)
            department_values = department.objects.get(department=department_values)
            doct  = department_values.doctor_set.all()
            print(doct)
            return render(request,'home/doctor.html',{'doct': doct})
        return render(request,'home/appoinment.html',{'user':user,'department_values':department_values,'data':data})
        


@login_required 
def orders(request): 
    k=User.objects.filter(is_superuser=True).first()
    orders=order.objects.all().exclude(userid=k).order_by('-id')
    if request.method == 'POST':       
        c = request.POST.get('start date')
        d = request.POST.get('end date')
        if c  and d:
           
            orders =order.objects.filter(date__gte= c,date__lte= d)
        
        elif c != '':
            
            orders =order.objects.filter(date__gte= c)
        elif d != '':
            
            orders =order.objects.filter(date__lte= d)  
    return render(request, 'subscription.html', {'orders': orders})

@login_required 
def appoinment_filter(request):
    appoinments= Appoinment.objects.all().order_by('-appoinmentdate')
    if request.method == 'POST':
       
        c = request.POST.get('start date')
        d = request.POST.get('end date')
        if c  and d:
           
            appoinments =Appoinment.objects.filter(appoinmentdate__gte= c,appoinmentdate__lte= d).order_by('-appoinmentdate')
        
        elif c != '':
            
            appoinments = Appoinment.objects.filter(appoinmentdate__gte= c).order_by('-appoinmentdate')
        elif d != '':
            
            appoinments= Appoinment.objects.filter(appoinmentdate__lte= d).order_by('-appoinmentdate')
        
    return render(request, 'index.html', {'appoinments': appoinments})