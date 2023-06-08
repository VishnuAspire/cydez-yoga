from django.shortcuts import render,redirect
from .models  import program,Category,Level,banner,order
from client.models import User
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView 
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FormParser,MultiPartParser,FileUploadParser,JSONParser
from . serializers import programSerializer,programSerializer1,slideSerializer,catgorySerializer,orderSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from datetime import datetime, timedelta
import datetime
from bs4 import BeautifulSoup
from django.core.files import File
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.contrib.auth import get_user, logout

# import vimeo

# client = vimeo.VimeoClient(token='bbf357639018210e0bf85709325491a4',key='22a0418a14545a3d347950a78d789d24d59289c9',secret='E9Te1x4j2B8F/Q4Vbgj1Gw8M8P2iOdzdXP1ntECTOfkhhQYbrNGS0CrUw8vAu3gGAqDDKCockybX/pbyYc21FVNeJ53c7qLLj8C+YKYJgfRoP+cTjNBLlxTlzN7Jjb2H')
# Create your views here.
def addProgram(request):
    c=Category.objects.all()
    if request.method=='POST':
        title=request.POST.get('title')
        day=request.POST.get('day')
        video_duration=request.POST.get('video_duration')
        categorys=request.POST.get('category')
        cat=Category.objects.get(category=categorys)
        introduction=request.POST.get('content')
        cleantext = BeautifulSoup(introduction, "lxml").text
        videourl=request.POST.get('videourl')
        image=request.FILES['image']
        f=FileSystemStorage()
        fn=f.save(image.name,image)
        program.objects.create(title=title,day=day,video_duration=video_duration,category=cat,introduction=cleantext,video_url=videourl,image=fn)
        # extra = {'popup':True,'heading':'Success','msg':'Succesfully Added'}
        # return render(request, "program.html",{'extra':extra})
        return redirect('list_program')
    return render(request,'program.html',{'c':c})

def listProgram(request):
    showprogram=program.objects.all().order_by('-id')
    # page=request.GET.get('page')
    # paginator=Paginator(showprogram,per_page=5)
    # try:
    #     showprogram=paginator.page(page)
    # except PageNotAnInteger:
    #     showprogram=paginator.page(1)
    # except EmptyPage:
    #     showprogram=paginator.page(paginator.num_pages)
    
    
    return render(request,'listprograms.html',{'showprogram':showprogram,})



def editProgram(request,userid):
    r = program.objects.filter(id=userid).values()
    c=Category.objects.all()
    v = program.objects.filter(id=userid)
    if request.method=='POST':
        update_values = {}
        
        title=request.POST.get('title')
        if title:
            update_values['title'] = title

        day=request.POST.get('day')
        if day:
            update_values['day'] = day

        video_duration=request.POST.get('video_duration')
        if video_duration:
            update_values['video_duration'] = video_duration

        categorys=request.POST.get('category')
        if categorys:
            cat=Category.objects.get(id=categorys)
            update_values['category'] = cat

        introduction=request.POST.get('content')
        cleantext = BeautifulSoup(introduction, "lxml").text
        if introduction:
            update_values['introduction'] = cleantext

        videourl=request.POST.get('videourl')
        if videourl:
            update_values['video_url'] = videourl
        img = request.FILES.get('image')
        if img :
            image=request.FILES['image']
            f=FileSystemStorage()
            fn=f.save(image.name,image)
            update_values['image'] = fn
        else:
            k =r[0]['image']
            update_values['image'] = k
        r.update(**update_values)

        # levels=Level.objects.get(level=level)
        return redirect('list_program')
    return render(request,"editprogram.html",{'i':v,'c':c})


def deleteProgram(request):
    if 'delete' in request.GET and request.method == 'POST':
        programid = request.POST.get('programid')
        pgm=program.objects.filter(id=programid)
        pgm.delete()
    return redirect('list_program')

def addCategory(request):
    if request.method=='POST':
        category=request.POST.get('category')
        numberofdays=request.POST.get('numberofdays')
        price=request.POST.get('price')
        validity=request.POST.get('validity')
        description=request.POST.get('content')
        # metakeywords=request.POST.get('metakeywords')
        # paid=request.POST.get('paid')
        # if paid==None:
        #     p=False
        # else:
        #     p=True
        # image=request.FILES['image']
        # f=FileSystemStorage()
        # fn=f.save(image.name,image)

        image=request.FILES['image']
        images = Image.open(image)
        width, height  = images.size
        if width > 350 and height > 360:
            images = images.convert('RGB')
            images = images.resize((285,200),Image.ANTIALIAS)
            output = BytesIO()
            images.save(output, format='JPEG', quality=90)
            output.seek(0)
            new_pic= InMemoryUploadedFile(output, 'ImageField',image.name,'image/jpeg',sys.getsizeof(output), None)
            c=FileSystemStorage()
            fn=c.save(image.name,new_pic)
        else:
            images = images.convert('RGB')
            images = images.resize((285,200),Image.ANTIALIAS)
            output = BytesIO()
            images.save(output, format='JPEG', quality=90)
            output.seek(0)
            new_pic= InMemoryUploadedFile(output, 'ImageField',image.name,'image/jpeg',sys.getsizeof(output), None)
            c=FileSystemStorage()
            fn=c.save(image.name,new_pic)
        
        Category.objects.create(SubscriptionValidity=validity,category=category,numberofclass=numberofdays,price=price,description=description,image=fn)
        return redirect('list_category')
    return render(request,'addcategory.html')

def listCategory(request):
    showcategory=Category.objects.all()
    page=request.GET.get('page')
    paginator=Paginator(showcategory,per_page=5)
    try:
       showcategory=paginator.page(page)
    except PageNotAnInteger:
        showcategory=paginator.page(1)
    except EmptyPage:
        showcategory=paginator.page(paginator.num_pages)
    return render(request,'listcategory.html',{'showcategory':showcategory,})


def addLevel(request):
    if request.method=='POST':
        level=request.POST.get('level')
        Level.objects.create(level=level)
        return redirect('list_level')
    return render(request,'addlevel.html')


def listLevel(request):
    showlevel=Level.objects.all()
    page=request.GET.get('page')
    paginator=Paginator(showlevel,per_page=5)
    try:
       showlevel=paginator.page(page)
    except PageNotAnInteger:
        showlevel=paginator.page(1)
    except EmptyPage:
        showlevel=paginator.page(paginator.num_pages)
    return render(request,'listlevel.html',{'showlevel':showlevel,})


def editLevel(request,userid):
    r = Level.objects.filter(id=userid).values()
    if request.method=='POST':
        level=request.POST.get('level')
        r.update(level=level)
        return redirect('list_level')
    return render(request,"editlevel.html",{'r':r})


def editCategory(request,userid):
    r = Category.objects.filter(id=userid).values()
    v = Category.objects.filter(id=userid)
    print(v)
    if request.method=='POST':
        update_values = {}
        categorys=request.POST.get('category')
        if categorys:
            update_values['category'] = categorys
        numberofclass=request.POST.get('numberofdays')
        print(numberofclass,"no fo cls")
        if numberofclass:
            update_values['numberofclass'] = numberofclass
        price=request.POST.get('price')
        if price:
            update_values['price']=price
        validity=request.POST.get('validity')
        if validity:
            update_values['SubscriptionValidity']=validity
        description=request.POST.get('content')
        if description:
            update_values['description']=description
        metakeywords=request.POST.get('metakeywords')
        if metakeywords:
            update_values['metakeywords']=metakeywords
        paid=request.POST.get('paid')

        if paid==None:
            p=False
            update_values['paid']=p
        else:
            p=True
            update_values['paid']=p
        # img = request.FILES.get('image')
        # if img :
        #     image=request.FILES['image']
        #     f=FileSystemStorage()
        #     fn=f.save(image.name,image)
        #     update_values['image'] = fn
        image=request.FILES.get('image')
        if image :
            images = Image.open(image)
            width, height  = images.size
            if width > 350 and height > 360:
                images = images.convert('RGB')
                images = images.resize((285,200),Image.ANTIALIAS)
                output = BytesIO()
                images.save(output, format='JPEG', quality=90)
                output.seek(0)
                new_pic= InMemoryUploadedFile(output, 'ImageField',image.name,'image/jpeg',sys.getsizeof(output), None)
                c=FileSystemStorage()
                fn=c.save(image.name,new_pic)
                update_values['image'] = fn
            else:
                images = images.convert('RGB')
                images = images.resize((285,200),Image.ANTIALIAS)
                output = BytesIO()
                images.save(output, format='JPEG', quality=90)
                output.seek(0)
                new_pic= InMemoryUploadedFile(output, 'ImageField',image.name,'image/jpeg',sys.getsizeof(output), None)
                c=FileSystemStorage()
                fn=c.save(image.name,new_pic)
                update_values['image'] = fn
        
        else:
            k =r[0]['image']
            update_values['image'] = k
        r.update(**update_values)
        return redirect('list_category')
    return render(request,"editcategory.html",{'i':v,'r':r})

def deleteLevel(request,userid):
    delete1= Level.objects.get(id=userid)
    delete1.delete()
    return redirect('list_level')


def deleteCategory(request):
    if 'delete' in request.GET and request.method == 'POST':
        categoryid = request.POST.get('categoryid')
        category=Category.objects.filter(id=categoryid)
        category.delete()
    return redirect('list_category')


def listSlides(request):
    showslides=banner.objects.all()
    page=request.GET.get('page')
    paginator=Paginator(showslides,per_page=5)
    try:
       showslides=paginator.page(page)
    except PageNotAnInteger:
        showslides=paginator.page(1)
    except EmptyPage:
        showslides=paginator.page(paginator.num_pages)
    return render(request,'listbanner.html',{'showslides':showslides,})


def addSlides(request):
    if request.method=='POST':
        title=request.POST.get('title')
        subtitle=request.POST.get('subtitle')
        description=request.POST.get('content')
        
        banner.objects.create(title=title,subtitle=subtitle,description=description)
        return redirect('list_slides')
    return render(request,'addslides.html')


def editSlides(request,userid):
    r = banner.objects.filter(id=userid).values()
    if request.method=='POST':
        title=request.POST.get('title')
        subtitle=request.POST.get('subtitle')
        description=request.POST.get('content')
        r.update(title=title,subtitle=subtitle,description=description)
        return redirect('list_slides')
    return render(request,"editslides.html",{'r':r})


def deleteSlides(request,userid):
    delete2= banner.objects.get(id=userid)
    delete2.delete()
    return redirect('list_slides')

def searchProgram(request):
    results = request.POST.get('search')
    print(results)

    showprogram = program.objects.filter(title__contains=results)
    page=request.GET.get('page')
    paginator=Paginator(showprogram,per_page=5)
    try:
        showprogram=paginator.page(page)
    except PageNotAnInteger:
        showprogram=paginator.page(1)
    except EmptyPage:
        showprogram=paginator.page(paginator.num_pages)
    return render(request,'listprograms.html',{'showprogram':showprogram,})
       
def searchCategory(request):
        results = request.POST.get('search')
        print(results)
        showcategory = Category.objects.filter(category__contains=results)
        page=request.GET.get('page')
        paginator=Paginator(showcategory,per_page=5)
        try:
            showcategory=paginator.page(page)
        except PageNotAnInteger:
            showcategory=paginator.page(1)
        except EmptyPage:
            showcategory=paginator.page(paginator.num_pages)
        return render(request,'listcategory.html',{'showcategory':showcategory,})
       
def searchLevel(request):
   
        results = request.POST.get('search')
        print(results)
        showlevel = Level.objects.filter(level__contains=results)
        page=request.GET.get('page')
        paginator=Paginator(showlevel,per_page=5)
        try:
            showlevel=paginator.page(page)
        except PageNotAnInteger:
            showlevel=paginator.page(1)
        except EmptyPage:
            showlevel=paginator.page(paginator.num_pages)
        return render(request,'listlevel.html',{'showlevel':showlevel,})
       
def searchSlide(request):
   
        results = request.POST.get('search')
        print(results)
        showslides = banner.objects.filter(title__contains=results)
        page=request.GET.get('page')
        paginator=Paginator(showslides,per_page=5)
        try:
            showslides=paginator.page(page)
        except PageNotAnInteger:
            showslides=paginator.page(1)
        except EmptyPage:
            showslides=paginator.page(paginator.num_pages)
        return render(request,'listbanner.html',{'showslides':showslides,})
       
#apiviews
@api_view(['GET'])
def listofprograms(request):
    k=program.objects.all()
    serializer= programSerializer(k,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def listoforder(request):
    k=order.objects.all()
    serializer=orderSerializer(k,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def listofslides(request):
    k=banner.objects.all()
    serializer= slideSerializer(k,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def retrieveprogram(request,pid):
    k=program.objects.filter(id=pid)
    serializer= programSerializer(k,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def retrivecategory(request,catid):
    k=program.objects.filter(category__id=catid)
    serializer= programSerializer(k,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def listofcategory(request):
    k=Category.objects.all()
    serializer=catgorySerializer(k,many=True)
    return Response(serializer.data)

# @login_required
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def createorder(request,userid):

    n=User.objects.filter(id=userid).values()
    print(n)
    user_status=n[0]['status']
    print(user_status)
    if user_status=='Subscriber':
    
        if request.method=='POST':
            amount=request.data.get('amount')
            status=request.data.get('status')
            date=request.data.get('date')
            time=request.data.get('time')
            userid=request.data.get('userid')
            user=User.objects.get(id=userid)
            categorid=request.data.get('categorid')
            cat=Category.objects.get(id=categorid)
            order.objects.create(amount=amount,status=status,date=date,time=time,userid=user,categorid=cat,subscribe=True)
            k=order.objects.all()
            serializer=orderSerializer(k,many=True)
            return Response(serializer.data)
    else:
        
        return Response({'please subscribe'})
@api_view(['GET'])
def programs(request,userid):
    userdata=User.objects.filter(id=userid).values()
    print(userdata)
    user_status=userdata[0]['status']
    if user_status=='Subscriber':
        k=program.objects.all().values()
        print(k)
        user_video=k[0]['video_url']
        print(user_video)
        # user_video={'video_url':None}
        # print(user_video)
        serializer= programSerializer(k,many=True)
        return Response(serializer.data)
    else:
       
        s=program.objects.all()
        
        serializer=programSerializer1(s,many=True)
        return Response(serializer.data)

@api_view(['POST'])
def takeprogram(request):
    if request.method=='POST':
        userid=request.POST.get('userid')
        print(userid)
        user_data=order.objects.filter(id=userid).values()
        
        
        print(user_data)
        user_status=user_data[0]['status']
        
        print(user_status)
        user_category=user_data[0]['categorid_id']
        print(user_category)
        if user_status=='Paid':
            ordered=program.objects.filter(category__id=user_category).values()
            print(ordered)
            serializer= programSerializer(ordered,many=True)

            return Response(serializer.data)
        else:
            return Response({'please subscribe'})
           
           

### fornt-end ###

def Categories(request,catid):
    user = request.user
    ids=user.id
    k=program.objects.filter(category__id = catid)
    cat = Category.objects.get(id = catid)
    bought = False
    total_pgm = k.count()
    if request.user.is_authenticated :
        if order.objects.filter(userid = user,categoryid = cat).exists():
            j=order.objects.filter(userid = user,categoryid = cat).order_by('-id')
            subscribe=j[0].subscribe
            if subscribe == False:
                bought = False
            else:
                bought = True
    if 'userids' in request.session:
        userids=request.session['userids']
        user=User.objects.get(id=userids)
        ids=user.id
        k=program.objects.filter(category__id = catid)
        cat = Category.objects.get(id = catid)
        bought = False
        total_pgm = k.count()
        if user.is_authenticated :
            if order.objects.filter(userid = user,categoryid = cat).exists():
                j=order.objects.filter(userid = user,categoryid = cat).order_by('-id')
                subscribe=j[0].subscribe
                if subscribe == False:
                    bought = False
                else:
                    bought = True
    if 'inform' in request.session:
        extra=request.session['inform']
        userProgramStartdate=request.session['date']
        userProgramStarttimebefore=request.session['time_before']
        userProgramStarttimeafter=request.session['time_after']
        del request.session['inform']
        del request.session['date']
        del request.session['time_before']
        del request.session['time_after']
        response=  render(request,"home/program.html",{'ids':ids,'user':user,'k':k,'total_pgm':total_pgm,'cat':cat,'is_bought':bought,'extra':extra,'date':userProgramStartdate,'time':userProgramStarttimebefore,'time1':userProgramStarttimeafter})
        return response
    if 'extra' in request.session:
        inform=request.session['extra']
        del request.session['extra']
        response= render(request,"home/program.html",{'ids':ids,'user':user,'k':k,'total_pgm':total_pgm,'cat':cat,'is_bought':bought,'inform':inform})
        return response
    response= render(request,"home/program.html",{'ids':ids,'user':user,'k':k,'total_pgm':total_pgm,'cat':cat,'is_bought':bought})
    return response
def listallprograms(request,error=None):
    print("LIST ALL PROGRAMS WORKING ")
    user=request.user
    if 'phone' in request.session:
        del request.session['phone']
    Categories = Category.objects.all().order_by('-id')
    k = program.objects.all()
    user_cat = []
    user = get_user(request)
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
    if request.user.is_authenticated :
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
    return render(request,"newprogram.html",{'user':user,'Categories':Categories,'k':k,'user_cat':user_cat,'buyPopup':popup})
# @login_required
def eachProgram(request,pid):
    print("EACH PROGRAM FUNCTION PROGRAM PLAY FUNCTION WORKS")
    k= program.objects.filter(id=pid).values()
    data = program.objects.get(id=pid)
    X = datetime.datetime.now()
    current_date=X.date()
    today = X.day
    current_time = X.time()
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
        order_details = order.objects.filter(userid=user,categoryid = data.category,subscribe=True).first()
        if order_details:
            userProgramStartdate = order_details.date
            user_day = userProgramStartdate.day
            userProgramStarttime = order_details.time
            validity_date = data.category.SubscriptionValidity
            programEnddate = userProgramStartdate + datetime.timedelta(days = validity_date) 
            pgm_end = programEnddate.day
            Starttime = datetime.datetime.combine(datetime.datetime.today(),userProgramStarttime)       
            time_before = Starttime - datetime.timedelta(minutes=60)
            time_before = time_before.time()
            k1=time_before.strftime("%I:%M %p")
            time_after = Starttime + datetime.timedelta(minutes=60)
            time_after = time_after.time()
            k2=time_after.strftime("%I:%M %p")        
            if ( current_date >= userProgramStartdate and current_date <= programEnddate and current_time >=time_before and current_time<=time_after ):
                day_get =  (current_date-userProgramStartdate).days
                video_day = data.day
                view = False
                if (day_get+1) == video_day:
                    view = True
                    return render(request,"home/eachprogram.html",{'user':user,'data':data,'view':view})
                else:
                    extra='Failed'
                    request.session['inform']=extra
                    request.session['date']=str(userProgramStartdate + datetime.timedelta(days = (video_day-1)))
                    request.session['time_before']=str(k1)
                    request.session['time_after']=str(k2)
                    return redirect(Categories,catid=data.category.id)
            else:
                extra='Failed'
                request.session['inform']=extra
                request.session['date']=str(userProgramStartdate)
                request.session['time_before']=str(k1)
                request.session['time_after']=str(k2)
                return redirect(Categories,catid=data.category.id)
        else:
            return redirect('home2',error=1)
        return render(request,"home/eachprogram.html",{'user':user,'data':data})
    