from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from apis.serializers.product import ProductSerializer
from products.models import Product
from apis.permissions import IsVendorOrReadOnly, IsOwnerVendor

class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()  # category ownership validated in serializer

class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerVendor]  # vendor can only modify their own products
