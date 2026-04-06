from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied

from .models import Order, OrderItem
from products.models import Cart, Product


@login_required
@permission_required('products.checkout', raise_exception=True)
def place_order(request):
    cart = request.session.get('cart', {})

    if not cart:
        # Cart is empty in session
        return redirect('cart_view')

    # Create order
    order = Order.objects.create(customer=request.user)

    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=int(product_id))  # get Product object from DB
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],  # use 'item', not 'product'
            price=item['price']         # use 'item', not 'product'
        )

    # Clear session cart
    request.session.pop('cart', None)

    return redirect('order_detail', order_id=order.id)




@login_required
def order_list(request):
    # customers can see their orders
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.user != order.customer and request.user.role != 'vendor':
        raise PermissionDenied


    if request.user.role == 'vendor':
        items = order.items.filter(product__category__vendor=request.user)
    else:
        items = order.items.all()

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items
    })
