from django.contrib import admin
from .models import program,Category,Level,banner,order
# Register your models here.
admin.site.register(program)
admin.site.register(Category)
admin.site.register(Level)
admin.site.register(banner)
admin.site.register(order)