from django.contrib import admin
from .models import User,department,doctor,Appoinment

admin.site.register(User)
admin.site.register(department)
admin.site.register(doctor)
admin.site.register(Appoinment)

