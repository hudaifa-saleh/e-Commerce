from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from accounts.forms import GuestForm, LoginForm, RegisterForm
from accounts.models import GuestEmail

# from analytics.models import user_logged_in_receiver
from accounts.signals import user_logged_in

User = get_user_model()

# LoginRequiredMixin
class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = "accounts/home.html"

    def get_object(self):
        return self.request.user


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = "/login/"


class LoginView(FormView):
    form_class = LoginForm
    success_url = "/"
    template_name = "accounts/login.html"
    default_next = "/"

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get("next")
        next_post = request.POST.get("next")
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, email=email, password=password)
        print("User: ", user)
        print("Password: ", password)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.session["guest_email_id"]
            except:
                pass
            if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                return redirect(redirect_path)
            return redirect("/")
        return super(LoginView, self).form_invalid(form)


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {"form": form}
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data["email"]
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session["guest_email_id"] = new_guest_email.id
        if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/regiester/")
    return redirect("/regiester/")


"""
def login_page(request):
    form = LoginForm(request.POST or None)
    context = {"form": form}
    print("User Loged_in")
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            try:
                del request.session["guest_email_id"]
            except:
                pass
            if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
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
"""
