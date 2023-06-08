from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from client import views
from program import views
from payment import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', include('client.urls')),
    path('program/',include('program.urls')),
    path('payment/',include('payment.urls')),
    # path('^', include('django.contrib.auth.urls')),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
