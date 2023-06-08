from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.contrib.auth.hashers import make_password





class UserManager(BaseUserManager):
       
    def _create_user(self, phone, password, **other_fields):
        """
        Create and save a user with the given email and password. And any other fields, if specified.
        """
        if not phone:
            raise ValueError('Valid Mobile number must be given')
       # email = self.normalize_email(email)
        
        user = self.model(phone=phone, **other_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def _create_user_phone(self, phone, password,otp, **other_fields):
        """
        Create and save a user with the given email and password. And any other fields, if specified.
        """
        if not phone:
            raise ValueError('Phone number is mandatory')
        
        user = self.model(phone=phone,password=password,otp=otp, **other_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, phone, password=None, **other_fields):
        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **other_fields)
    
    def create_user_phone(self, phone, password,otp, **other_fields):
        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_superuser', False)
        return self._create_user_phone(phone, password,otp,**other_fields)

    def create_superuser(self, phone, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **other_fields)


class User(AbstractUser):
    STATUS = (
        ('Registered', 'Registered'),
        ('Subscriber', 'Subscriber')
    )
    
    username       = models.CharField(max_length=100,null=True,blank=True)
    first_name     = models.CharField(max_length=100,null=True,blank=True)
    last_name      = models.CharField(max_length=100,null=True,blank=True)
    email          = models.EmailField(max_length=255,null=True,blank=True)
    phone          = models.IntegerField(unique=True)
    address        = models.TextField(max_length=100,null=True,blank=True)
    city           = models.CharField(max_length=255,null=True,blank=True)
    postcode       = models.IntegerField(null=True,default=None)
    role           = models.CharField(max_length=30,null=True,blank=True)
    DOB            = models.DateField(null=True)
    status         = models.CharField(default="Registered",max_length=50,null=True, choices=STATUS)
    image          = models.ImageField(upload_to='customer', blank=True, null=True,default='default.png')
    otp            = models.IntegerField(null=True,default=None)

    USERNAME_FIELD  = 'phone'
    REQUIRED_FIELDS = ['address','email','city','postcode','role','DOB','image']
    objects=UserManager()

    def get_username(self):
        return self.email


class department(models.Model):
    department = models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return str(self.department)

class doctor(models.Model):
    department     = models.ForeignKey(department,on_delete=models.CASCADE,null=True,blank=True)
    doctor         = models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return str(self.id)


class Appoinment(models.Model):
    STATUS = (
        ('Accepted', 'Accepted'),
        ('Cancelled', 'Cancelled'),
        ('pending','pending')
    )

    customer_id    = models.OneToOneField('User', on_delete = models.CASCADE, null=True)
    department     = models.ForeignKey(department,on_delete=models.CASCADE,null=True,blank=True)
    doctor         = models.ForeignKey(doctor,on_delete=models.CASCADE,null=True,blank=True)
    name           = models.CharField(max_length=40,null=True)
    phone          = models.IntegerField(null=True)
    email          = models.EmailField(max_length=50, null=True,blank=True)
    address        = models.TextField(max_length=100,null=True,blank=True)
    state          = models.CharField(max_length=40,null=True) 
    city           = models.CharField(max_length=40,null=True)
    postcode       = models.IntegerField(null=True,default=None)
    comment        = models.TextField(max_length=500,null=True,blank=True)
    appoinmentdate = models.DateField(null=True)
    status         = models.CharField(max_length=50,null=True, choices=STATUS)
    order_id       = models.CharField(max_length=90,null=True,blank=True)
    payment_id     = models.CharField(max_length=90,null=True,blank=True)
    signature      = models.CharField(max_length=90,null=True,blank=True)
    amount         = models.IntegerField(default='100',null=True,blank=True) 
    def __str__(self):
        return self.name
