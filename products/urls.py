from django.conf.urls.static import static
from django.urls import path

from config import settings
from . import category_views, product_views

urlpatterns = [
    path('vendor/dashboard/', category_views.vendor_dashboard, name='vendor_dashboard'),
    path('customer/dashboard/', category_views.customer_dashboard, name='customer_dashboard'),

    path('create_category/', category_views.create_category, name='create_category'),
    path('category_detail/<int:category_id>/', category_views.category_detail, name='category_detail'),
    path('category_list/', category_views.category_list, name='category_list'),
    path('update_category/<int:category_id>/', category_views.update_category, name='update_category'),
    path('delete_category/<int:category_id>/', category_views.delete_category, name='delete_category'),

    path('create_product/<int:category_id>/', product_views.create_product, name='create_product'),
    path('update_product/<int:product_id>/', product_views.update_product, name='update_product'),
    path('delete_product/<int:product_id>/', product_views.delete_product, name='delete_product'),
    path('product_list/', product_views.product_list, name='product_list'),
    path('product_detail/<int:product_id>/', product_views.product_detail, name='product_detail'),

    path('cart/', product_views.cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', product_views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', product_views.remove_from_cart, name='remove_from_cart'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
