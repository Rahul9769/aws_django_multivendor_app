from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from products.models import Category
from apis.serializers.category import CategorySerializer
from apis.permissions import IsVendorOrReadOnly, IsOwnerVendor

class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.select_related('vendor')
    serializer_class = CategorySerializer
    permission_classes = [IsVendorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.select_related('vendor')
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerVendor]
