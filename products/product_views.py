from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category, Product
from .forms import ProductForm
from orders.models import Order, OrderItem



@login_required
@permission_required("products.view_product", raise_exception=True)
def product_list(request):
    search_query = request.GET.get('q', '')
    products = Product.objects.all()
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products/product_list.html', {'products': page_obj, 'search_query': search_query})


@login_required
@permission_required("products.view_product", raise_exception=True)
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
@permission_required("products.add_product", raise_exception=True)
def create_product(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if category.vendor != request.user:
        return HttpResponseForbidden("Not allowed")
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.category = category
            product.save()
            return redirect('category_detail', category_id=category.id)
    else:
        form = ProductForm()
    return render(request, 'products/create_product.html', {'form': form, "category": category})


@login_required
@permission_required("products.change_product", raise_exception=True)
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.category.vendor != request.user:
        return HttpResponseForbidden("Not allowed")
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('category_detail', category_id=product.category.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/update_product.html', {'form': form, 'product': product})


@login_required
@permission_required("products.delete_product", raise_exception=True)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.category.vendor != request.user:
        return HttpResponseForbidden("Not allowed")
    category_id = product.category.id
    product.delete()
    return redirect('category_detail', category_id=category_id)


@login_required
@permission_required("products.add_to_cart", raise_exception=True)
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    if str(product.id) in cart:
        cart[str(product.id)]['quantity'] += 1
    else:
        cart[str(product.id)] = {
            'title': product.title,
            'price': float(product.price),
            'quantity': 1,
            'image_url': product.image.url if product.image else ''
        }
    request.session['cart'] = cart
    messages.success(request, f"{product.title} added to cart")
    return redirect('product_list')


@login_required
@permission_required("products.view_cart", raise_exception=True)
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, item in cart.items():
        subtotal = item['price'] * item['quantity']
        total += subtotal
        cart_items.append({**item, 'id': product_id, 'subtotal': subtotal})
    return render(request, 'products/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
@permission_required("products.delete_cart", raise_exception=True)
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        removed_item = cart.pop(str(product_id))
        messages.success(request, f"{removed_item['title']} removed from cart.")
        request.session['cart'] = cart
    return redirect('cart_view')




@login_required
@permission_required("products.checkout", raise_exception=True)
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart_view')

    # Create order
    order = Order.objects.create(customer=request.user)

    # Create order items
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],
            price=product.price
        )

    # Clear cart
    request.session.pop('cart', None)
    messages.success(request, f"Order #{order.id} placed successfully!")
    return redirect('order_detail', order_id=order.id)
