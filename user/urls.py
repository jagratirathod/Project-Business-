from django.urls import path
from . import views

urlpatterns=[
    path('',views.userhome),
    path('addproduct/',views.addproduct),
    path('viewproductuser/',views.viewproductuser),
    path('cancel/',views.cancel),
    path('success/',views.success),
    path('payment/',views.payment),
    path('bidproduct/',views.bidproduct),
    path('bidproductview/',views.bidproductview),
    path('bidhistory/',views.bidhistory),
    path('mybid/',views.mybid),
    path('cpuser/',views.cpuser),
    path('fetchSubCategoryAJAX/',views.fetchSubCategoryAJAX)
   ]