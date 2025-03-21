"""
URL configuration for hotel_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # paths from the system app
    path('booking/', include('Booking.urls')),
    path('hotel/', include('Hotel.urls')),
    path('user/', include('User.urls')),
    
    # add URL maps to redirect the base URL to our app
    path('', RedirectView.as_view(url='/user/login', permanent=True)), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Use static() to add url mapping to serve static files during development (only)