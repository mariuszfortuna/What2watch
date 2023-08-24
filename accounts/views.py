from psycopg2 import IntegrityError
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, UpdateView
from accounts.forms import RegisterForm, UserUpdateView
from django.contrib import messages
from what_to_watch.context_processors import user_is_moderator


# Create your views here.


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  # Autentycation
        if user is not None:
            login(request, user)  # Autoryzation
            redirect_url = request.GET.get('next', 'home')
            return redirect(redirect_url)
        else:
            messages.error(request, 'Invalid username or password')  # Add error message
            return render(request, 'login.html')



class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('home')


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Add a user to an existing "Users" group
            users_group = Group.objects.get(name='Users')
            user.groups.add(users_group)

            return redirect('login')
        return render(request, 'register.html', {'form': form})


# List of registered users
class UserListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'user_list.html'

    # checks if the user belongs to the Moderators group returns Tru or False
    def test_func(self):
        return user_is_moderator(self.request.user)


# Edit a user, add a user to a group.
class UpdateUserView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_update.html'
    form_class = UserUpdateView

    def test_func(self):
        return user_is_moderator(self.request.user)

    def get_success_url(self):
        return reverse('update_user', kwargs={'pk': self.object.pk})
