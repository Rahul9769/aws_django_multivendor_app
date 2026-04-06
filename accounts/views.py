from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import VendorSignUpForm, CustomerSignUpForm, CustomAuthenticationForm


def home(request):
    return render(request, 'accounts/home.html')


def vendor_signup(request):
    if request.method == "POST":
        form = VendorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = VendorSignUpForm()
    return render(request, "accounts/vendor_signup.html", {'form': form})


def customer_signup(request):
    if request.method == "POST":
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomerSignUpForm()
    return render(request, 'accounts/customer_signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login_view')
