from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apis.views.auth import RegisterApiView, LoginAPIView
from apis.views.category import CategoryListCreateAPIView, CategoryDetailAPIView
from apis.views.product import ProductListCreateAPIView, ProductDetailAPIView
from apis.views.cart import CartView, AddToCartAPIView, RemoveFromCartAPIView, CheckoutAPIView

urlpatterns = [
    path("auth/register/", RegisterApiView.as_view()),
    path("auth/login/", LoginAPIView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),

    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),

    path('cart/', CartView.as_view(), name='cart-view'),
    path('cart/add/<int:product_id>/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:product_id>/', RemoveFromCartAPIView.as_view(), name='remove-from-cart'),
    path('cart/checkout/', CheckoutAPIView.as_view(), name='checkout'),
]
