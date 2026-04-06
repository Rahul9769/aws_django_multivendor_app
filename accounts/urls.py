from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vendor_signup/', views.vendor_signup, name='vendor_signup'),
    path('customer_signup/', views.customer_signup, name='customer_signup'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
]
