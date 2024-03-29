from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView

from .models import Khach
from .forms import KhachForm, LoginForm, RegisterForm
from .signals import user_logged_in

from ryanstudio.mixins import NextUrlMixin, RequestFormAttachMixin

class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'taikhoan/login.html'
    default_next = '/' 

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "taikhoan/register.html"
    success_url = "/login/"

class GuestRegisterView(NextUrlMixin, RequestFormAttachMixin, CreateView):
    form_class = KhachForm
    default_next = "/register"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.get_next_url():
                return self.get_next_url()
            return redirect('/')
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.get_next_url()

    def form_valid(self, form):
        email       = form.cleaned_data.get("email")
        khach       = Khach.objects.create(email=email)
        self.request.session['id_khach'] = khach.id
        return redirect(self.get_next_url())

    def form_invalid(self, form):
        return redirect(self.default_next)