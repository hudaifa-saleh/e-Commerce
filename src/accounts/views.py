from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from ecommerce.forms import LoginForm, RegisterForm
from django.utils.http import is_safe_url
User = get_user_model()


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {"form": form}
    print("User Loged_in")
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            print("Error...")
    return render(request, "accounts/login.html", context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        newUser = User.objects.create_user(username, email, password)
        print(newUser)
    return render(request, "accounts/register.html", context)
