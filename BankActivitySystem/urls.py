"""BankActivitySystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('activity-sign-up/', include('ActivitySignUp.urls')),
    path('address/', include('Address.urls')),
    path('admin-third/', include('AdminThird.urls')),
    path('admin-second/', include('AdminSecond.urls')),
    path('admin-first/', include('AdminFirst.urls')),
    path('admin-zero/', include('AdminZero.urls')),
    path('login/', include('Login.urls')),
    path('customer/', include('Customer.urls')),
    path('notice/', include('Notice.urls')),
    path('merchandise/', include('Merchandise.urls')),
    path('request-action/', include('RequestAction.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
