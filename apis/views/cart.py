from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from products.models import Cart, CartItem, Product
from apis.serializers.cart import CartSerializer


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self):
        cart, created = Cart.objects.get_or_create(customer=self.request.user)
        return cart

    def get(self, request):
        cart = self.get_cart()
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        if request.user.role != 'customer':
            return Response({"detail": "Only customers can add products"}, status=status.HTTP_403_FORBIDDEN)

        product = Product.objects.get(id=product_id)
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        if request.user.role != 'customer':
            return Response({"detail": "Only customers can remove products"}, status=status.HTTP_403_FORBIDDEN)

        cart = Cart.objects.get(customer=request.user)
        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
        except CartItem.DoesNotExist:
            return Response({"detail": "Item not in cart"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'customer':
            return Response({"detail": "Only customers can checkout"}, status=status.HTTP_403_FORBIDDEN)

        cart = Cart.objects.get(customer=request.user)
        cart.items.all().delete()  # clear all items
        return Response({"detail": "Order placed successfully"}, status=status.HTTP_200_OK)
