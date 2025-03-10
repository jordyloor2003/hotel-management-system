from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from .models import User
from .forms import CustomUserCreationForm

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model= User
    template_name= "users/list.html"
    context_object_name= "users"

    def test_func(self):
        """"""
        return self.request.user.is_superuser
    
class UserDetailView(LoginRequiredMixin, DetailView):
    model= User
    template_name= "users/detail.html"
    
    def get_object(self):
        """"""
        return self.request.user
    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model= User
    template_name= "users/edit.html"
    fields= "__all__"
    success_url= reverse_lazy('user_detail')
    
    def get_object(self):
        return self.request.user

class UserRegisterView(CreateView):
    form_class= CustomUserCreationForm
    template_name= "users/register.html"
    success_url = reverse_lazy('login')

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        
        if user.is_hotel_owner:
            return redirect('/hotel/dashboard/')  # Redirigir a página de dueños de hoteles
        else:
            return redirect('/booking/')  # Redirigir a clientes