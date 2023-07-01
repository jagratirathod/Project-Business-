from django.urls import path
from.import views

urlpatterns=[
    path('',views.adminhome),
    path('manageusers/',views.manageusers),
    path('manageuserstatus/',views.manageuserstatus),
    path('addcategory/',views.addcategory),
    path('subcategory/',views.subcategory),
    path('cpmyadmin/',views.cpmyadmin)
]