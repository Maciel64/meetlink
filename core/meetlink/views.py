from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.views import View
from django.views.generic import TemplateView

from .forms import LoginForm

from .exceptions import LoginDataIsInvalidException, UserEmailOrPasswordIsInvalidException
from .models import Role, User
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

# Create your views here.

@login_required
def totem(request) :
    user: User = request.user

    if user.role in (Role.MANAGER, Role.INTERPRETER) :
      return redirect('dashboard')

    return render(request, 'totem.html', { 'user': user })

@login_required
def dashboard(request) :
  user = request.user

  return render(request, 'dashboard.html', { 'user': user })

class LoginView(View) :
    def get(self, request):
        return render(request, 'login.html', { "hide_sidebar": True })

    def post(self, request) :
        try :
            data = LoginForm(request.POST)
            
            if not data.is_valid :
                raise LoginDataIsInvalidException()

            user = User.objects.get(email=data.cleaned_data["email"])
            
            if not check_password(data.cleaned_data["password"], user.password) :
                raise UserEmailOrPasswordIsInvalidException()
            
            login(request, user)

            return redirect('index')

        except User.DoesNotExist :
            return render(request, 'login.html', { "hide_sidebar": True, "error": 'Usuário não encontrado' })

        except Exception as e:
            return render(request, 'login.html', { "hide_sidebar": True, "error": 'Email ou senha não inválidos' })

  
def logout_view(request) :
  user = request.user

  if not user :
    return redirect('index')
  
  logout(request)

  return redirect('index')