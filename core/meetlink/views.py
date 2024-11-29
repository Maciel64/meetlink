from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

# Create your views here.

@login_required
def index(request) :
  user = request.user

  return render(request, 'index.html', { 'user': user })

@login_required
def dashboard(request) :
  user = request.user

  return render(request, 'dashboard.html', { 'user': user })

@require_http_methods(['GET', 'POST'])
def login_view(request) :
  if   request.method == 'GET' :
    return render(request, 'login.html', { "hide_sidebar": True })
  
  if request.method == 'POST' :
    user = User.objects.get(email=request.POST.get('email'))

    if not user :
      return render(request, 'login.html', { "hide_sidebar": True, "error": 'Email ou senha não inválidos' })
    
    if not check_password(request.POST.get('password'), user.password) :
      return render(request, 'login.html', { "hide_sidebar": True, "error": 'Email ou senha não inválidos' })
    
    login(request, user)

    return redirect('index')
    
  
def logout_view(request) :
  user = request.user

  if not user :
    return redirect('index')
  
  logout(request)

  return redirect('index')