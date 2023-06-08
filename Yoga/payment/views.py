from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from program.models import program,Category,order
from client.models import Appoinment,User,doctor,department
# Create your views here.
from datetime import datetime
import razorpay,datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth import get_user, logout
client =  razorpay.Client(auth = ("rzp_live_extnBMvpztuUgO","hiAhbFBivYZNOn1oV2D7gvWz"))
# client =  razorpay.Client(auth = ("rzp_test_qoUoBWhmPOM55N","BWs0lFVYJGVCeY2zr5KzwD4U"))

# @login_required
@requires_csrf_token
@csrf_exempt
def create_order(request):
	context = {}
	user = request.user
	userid=user.id
	if 'userids' in request.session:
		print("USERID FROM SESSION ")
		userids=request.session['userids']
		user=User.objects.get(id=userids)
		userid=user.id
	if userid == None:
		flag = 1
		return redirect('userlogin2',flag=flag)
	else:
		if request.method =='POST':
			catId = request.POST.get("category")
			cat = Category.objects.get(id = catId)
			category_name = cat.category
			amount = cat.price
			name = user.get_full_name()
			phone = user.phone
			email = user.email
			order_amount = int(amount)*100
			notes = {'Shipping address': user.address}
			order_currency ="INR"

			order_receipt = datetime.date.today().strftime('%D')
			start_date = datetime.date.today().strftime('%Y-%m-%d')
			start_time = datetime.datetime.now()
			start_time=start_time.time().strftime("%H:%M")
			# CREAING ORDER
			response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='1'))
			order_id = response['id']
			order_status = response['status']
			if order_status=='created':

			# Server data for user convinience
				context['product_id'] = order_id
				context['price'] = order_amount
				context['name'] = name
				context['phone'] = phone
				context['email'] = email
				context['userid'] = userid
				# data that'll be send to the razorpay for
				context['order_id'] = order_id
				context['product_price'] = amount
				context['catId'] = catId
				context['category_name'] = category_name
				context['start_date'] = start_date
				context['start_time'] = start_time
				context['user'] = user
			return render(request,'payment/confirm-page.html', context)
		return render(request,'payment/confirm-page.html', {'user':user})
@requires_csrf_token
@csrf_exempt
def payment_status(request):

	response = request.POST
	date = request.POST.get('date')
	time = request.POST.get('time')
	categoryid = request.POST.get('categoryid')
	amount = int(request.POST.get('price'))
	user = request.user
	userids = request.POST.get('userid')
	userid=User.objects.get(id=userids)
	params_dict = {
	'razorpay_payment_id' : response['razorpay_payment_id'],
	'razorpay_order_id' : response['razorpay_order_id'],
	'razorpay_signature' : response['razorpay_signature']
	}
	try:
		status = client.utility.verify_payment_signature(params_dict)
		order_id =response['razorpay_order_id']
		payment_id = response['razorpay_payment_id']
		signature = response['razorpay_signature']
		categoryid = Category.objects.get(id = categoryid)
		order.objects.create(subscribe=True,order_id=order_id,payment_id=payment_id,categoryid=categoryid,signature=signature,userid=userid,amount=amount,date=date,time=time)
	except:
		return render(request, 'payment/order_summary.html', {'status': 'Payment Faliure!!!'})
	else:
		userid.status = "Subscriber"
		userid.save()
		inform='You have successfully bought the Package'
		request.session['extra']=inform
		request.session['userids']=userids
		return redirect('Categories',catid=categoryid.id)


@login_required
def create_appoinment(request):
	context = {}
	print("hello")
	if request.method =='POST':
		appoinId = request.POST.get("appoinment")
		print(appoinId)
		appoinment = Appoinment.objects.get(id = appoinId)
		appoin_date = appoinment.appoinmentdate
		print(appoin_date)
		doctor_name = appoinment.doctor
		print(doctor_name)
		depart_name = appoinment.department
		print(depart_name)
		name = appoinment.name
		print(name)
		email = appoinment.email
		phone = appoinment.phone
		amount = 100
		order_amount = amount*100
		notes = appoinment.address
		order_currency ="INR"
		order_receipt = "24/12/2020"
		start_date = datetime.date.today().strftime('%Y-%m-%d')
		# CREAING ORDER
		response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='1'))
		order_id = response['id']
		order_status = response['status']

		if order_status=='created':

		# Server data for user convinience
			context['product_id'] = order_id
			context['price'] = order_amount
			context['name'] = name
			context['phone'] = phone
			context['email'] = email
			# data that'll be send to the razorpay for
			context['order_id'] = order_id
			context['product_price'] = amount
			context['appoinId'] = appoinId
			context['appoin_date'] = appoin_date
			context['doctor_name'] = doctor_name
			context['depart_name'] = depart_name
			context['start_date'] = start_date
			
	
	return render(request,'home/confirm-appoinment.html', context)

@csrf_exempt
def appoinment_status(request):
        
	user = request.user
	userids = request.POST.get('userid')
	if userids != None:
		user=User.objects.get(id=userids)
	response = request.POST
	appointmentId = request.POST.get('appointmentId')
	departments    = request.POST.get('department') 
	De = department.objects.get(department=departments)
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
	
	
	params_dict = {
	'razorpay_payment_id' : response['razorpay_payment_id'],
	'razorpay_order_id' : response['razorpay_order_id'],
	'razorpay_signature' : response['razorpay_signature']
	}
	try:
		status = client.utility.verify_payment_signature(params_dict)
		order_id =response['razorpay_order_id']
		payment_id = response['razorpay_payment_id']
		signature = response['razorpay_signature']
		print(comment)
		if comment == None:
			comment = "None"
			a = Appoinment.objects.create(signature=signature,order_id=order_id,payment_id=payment_id,department=De,doctor=Do,name=name,phone=phone,email=email,address=address,state=state,city=city,postcode=postcode,comment=comment,appoinmentdate=appoinmentdate,status="pending")
			appointmentId = a.id
			doctor_name = a.doctor
			department_name = a.department
			date = a.appoinmentdate
		else:
			a = Appoinment.objects.create(signature=signature,order_id=order_id,payment_id=payment_id,department=De,doctor=Do,name=name,phone=phone,email=email,address=address,state=state,city=city,postcode=postcode,comment=comment,appoinmentdate=appoinmentdate,status="pending")
			appointmentId = a.id
			doctor_name = a.doctor
			department_name = a.department
			date = a.appoinmentdate
	except:
		return render(request, 'payment/order_summary.html', {'status': 'Payment Faliure!!!'})
	else:
		extra = {'popup':True,'heading':'Appoinment Made !!','msg':'Your appointment with doctor '+str(doctor_name.doctor.upper())+' is made successfully.     Appointment date: '+str(date)}
		request.session['userids']=userids
		return render(request,'home/appoinment.html', {'user':user,'extra':extra})
