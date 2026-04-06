from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from .forms import CategoryForm
from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required("products.view_category", raise_exception=True)
def vendor_dashboard(request):
    if request.user.role != 'vendor':
        return HttpResponseForbidden()

    categories = request.user.categories.all()  # all categories of this vendor
    return render(request, 'products/vendor_dashboard.html', {'categories': categories})


@login_required
@permission_required("products.view_category", raise_exception=True)
def customer_dashboard(request):
    return render(request, 'products/customer_dashboard.html')


@login_required
@permission_required('products.view_category', raise_exception=True)
def category_list(request):
    if request.user.role == 'vendor':
        categories = Category.objects.filter(vendor=request.user)
    else:
        categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})


@login_required
@permission_required('products.view_category', raise_exception=True)
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    return render(request, 'products/category_detail.html', {
        'category': category,
        'products': products
    })


@login_required
@permission_required('products.add_category', raise_exception=True)
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.vendor = request.user
            category.save()
            return redirect('category_detail', category_id=category.id)
    else:
        form = CategoryForm()
    return render(request, 'products/create_category.html', {'form': form})


@login_required
@permission_required('products.change_category', raise_exception=True)
def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, vendor=request.user)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.vendor = request.user
            category.save()
            return redirect('category_detail', category_id=category.id)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products/update_category.html', {'form': form, 'category': category})


@login_required
@permission_required('products.delete_category', raise_exception=True)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, vendor=request.user)
    category.delete()
    return redirect('category_list')
