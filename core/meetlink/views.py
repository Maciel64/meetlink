from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.views import View
from django.views.generic import TemplateView

from meetlink.adapters.call_adapter import GoogleMeetAdapter

from .forms import LoginForm

from .exceptions.user_exceptions import LoginDataIsInvalidException, UserEmailOrPasswordIsInvalidException
from .models import Role, User
from django.shortcuts import redirect, render

# Create your views here.

@login_required
def index(request) :
    user: User = request.user

    if user.role in (Role.SUPERADMIN, Role.MANAGER, Role.INTERPRETER) :
      return redirect('dashboard')

    return redirect('totem')


@login_required
def totem(request) :
    user: User = request.user

    if user.role in (Role.MANAGER, Role.INTERPRETER) :
      return redirect('dashboard')

    return render(request, 'totem.html', { 'user': user, 'hide_sidebar': True })


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
            return render(request, 'login.html', { "hide_sidebar": True, "error": e.__str__ })

  
def logout_view(request) :
  user = request.user

  if user :
    logout(request)

  return redirect('index')


@login_required
def create_call(request) :
    call_adapter = GoogleMeetAdapter()

    call = call_adapter.create_call()

    return render(request, 'create_call.html', { "call_uri": call.call_uri })