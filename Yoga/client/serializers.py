from rest_framework import serializers
from .models import User,doctor,department,Appoinment

class userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id',
        'email',
        'username',
        'password',
        'address',
        'postcode',
        'role',
        'city',
        'phone',
        'DOB',
        'status'
        ]

class appoinmentserializer(serializers.ModelSerializer):
    class Meta:
        model = Appoinment
        fields = '__all__'