from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import SignUpForm,LogInForm
from .models import User
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
def rooms(request):
  template = loader.get_template("messaging/rooms.html")
  context = {}
  return HttpResponse(template.render(context, request))

def signUp(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('/rooms/logIn')
  else:
    form = UserCreationForm()

  return render(request,'messaging/signUp.html',{'form':form})

def logIn(request):
  users = User.objects.all()
  for user in users:
    print(f'username: {user.username},password: {user.password}')

  if request.method == 'POST':
    form = AuthenticationForm(request,data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request,user)
      if user is not None:
        login(request,user)
        return redirect('/rooms/dashboard')
  else:
    form = AuthenticationForm()

  return render(request,'messaging/logIn.html',{'form':form})

def logOut(request):
  logout(request)
  return redirect('/rooms/')

def dashboard(request):
  template = loader.get_template("messaging/dashboard.html")
  context = {}
  return HttpResponse(template.render(context, request))