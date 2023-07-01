
from django.contrib import admin
from django.urls import path,include
from . import views
from django .conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path('',views.home),
    path('about/',views.about),
    path('contact/',views.contact),
    path('service/',views.service),
    path('register/',views.register),
    path('verifyuser/',views.verifyuser),
    path('viewsubcategory/',views.viewsubcategory),
    path('viewproductfilter/',views.viewproductfilter),
    path('forgetpassword/',views.forgetpassword),
    path('login/',views.login),
    path('myadmin/',include('myadmin.urls')),
    path('user/',include('user.urls'))
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
