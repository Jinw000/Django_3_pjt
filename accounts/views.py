from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.GET.get("next") or "products:products"
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def home(request):
    return render(request, 'accounts/home.html')

@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("home")

@require_POST
def signout(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect("home")