from django.db import models
from client.models import User
from django.http import HttpResponse
from django.template import Template,Context
# Create your models here.

class Category(models.Model):
    category=models.CharField(max_length=90,null=True) 
    numberofclass=models.IntegerField(default='0',null=True)
    validity = models.IntegerField(default='30',null=True)
    paid=models.BooleanField(default=False,null=True,blank=True)
    price=models.IntegerField(default='0',null=True)
    description=models.TextField(max_length=500,null=True)
    metakeywords=models.CharField(max_length=100,null=True)
    image=models.ImageField(upload_to='products',blank=True,null=True)
    SubscriptionValidity = models.IntegerField(blank=True,null=True)
    def __str__(self):
       return  self.category

    def get_description(self):
        if self.description:
            t =  Template(self.description)
            context = Context(dict(name='World'))
            return t.render(context)
        else:
            return " "

class Level(models.Model):
    level=models.CharField(max_length=90,null=True)
    
    
    def __str__(self):
       return  self.level

class program(models.Model):
    title=models.CharField(max_length=90,null=True)
    day=models.IntegerField(default='0',null=True)
    video_duration=models.IntegerField(default='0',null=True)
    numberofclass=models.IntegerField(default='0',null=True)
    style=models.CharField(max_length=90,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    level=models.ForeignKey(Level,on_delete=models.SET_NULL,null=True,blank=True)
    introduction=models.TextField(max_length=500,null=True)
    video_url=models.CharField(max_length=90,null=True)
    image=models.ImageField(upload_to='products',blank=True,null=True)
    
    class Meta:
        ordering = ['day']

    def __str__(self):
       return  self.title



class banner(models.Model):
    title=models.CharField(max_length=90,null=True)
    subtitle=models.CharField(max_length=90,null=True)
    description=models.TextField(max_length=100,null=True)
    def __str__(self):
       return  self.title

class order(models.Model):
    STATUS = (
        ('Paid', 'Paid'),
        ('NotPaid', 'NotPaid')
    )
    userid     = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    categoryid = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    amount     = models.IntegerField(default='0',null=True,blank=True)
    status     = models.CharField(max_length=90,null=True,choices=STATUS)
    order_date = models.DateField(auto_now_add=True)
    order_time = models.TimeField(auto_now_add=True,null=True,blank=True)
    time       = models.TimeField(null=True)
    date       = models.DateField(null=True)
    order_id   = models.CharField(max_length=90,null=True,blank=True)
    payment_id = models.CharField(max_length=90,null=True,blank=True)
    signature  = models.CharField(max_length=90,null=True,blank=True)
    subscribe  = models.BooleanField(default=False)
    def __str__(self):
        
        if self.userid:
            return self.userid.get_full_name()
        else:
            return "Not registered user"