from django.urls import path
from .views import place_order, order_list, order_detail

urlpatterns = [
    path('place/', place_order, name='place_order'),
    path('', order_list, name='order_list'),
    path('<int:order_id>/', order_detail, name='order_detail'),
]
