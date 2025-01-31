from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm,LogInForm,ProfileForm,MessageForm
from django.db.models import Q
from .models import Profile,Message
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
def rooms(request):


  context = {}
  context = {
        "users": User.objects.all()
    }
  print("Room view called. Users:", context["users"])
  print(context["users"])
  return render(request, "messaging/rooms.html", [])


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
  User = get_user_model()
  users = User.objects.all()
  user_profiles = []
  for user in users:
        try:
            profile = Profile.objects.get(user=user)
            user_profiles.append({
                'username': user.username,
                'password': user.password,
                'id': user.id,
                'profile': {
                    'bio': profile.bio,
                    'location': profile.location,
                    'phone_number': profile.phone_number,
                    'profile_pic_url': profile.profile_picture.url if profile.profile_picture else None,
                }
            })
        except Profile.DoesNotExist:
            user_profiles.append({
                'username': user.username,
                'password': user.password,
                'profile': 'No profile available'
            })

  template = loader.get_template("messaging/dashboard.html")
  context = {
        'users': user_profiles
    }
  return HttpResponse(template.render(context, request))

@login_required
def profile(request):
    try:
        # Attempt to get the user's profile
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # If no profile exists, create a new one for the form
        profile = None

    if request.method == 'POST':
        # If the profile exists, pass it to the form instance for updating
        form = ProfileForm(request.POST, request.FILES,instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Ensure the profile is linked to the current user
            profile.save()
            return redirect('/rooms/dashboard')
        else:
            print(form.errors)
    else:
        # Initialize the form with the user's profile if it exists
        form = ProfileForm(instance=profile)

    return render(request, 'messaging/profile.html', {'form': form})
def room(request, user_id):
    user = get_object_or_404(User, id=user_id)
    current_user = request.user
    print('user ' + str(user) + ' curr user ' + str(current_user) + 'msgs ' + str(Message.objects.all()))
    messages = Message.objects.filter(
        Q(sender=current_user, receiver=user) |
        Q(sender=user, receiver=current_user)
    ).order_by('timestamp')
    #find all messages where the sender is either the other user or you and the receiver is either the other user or you
    print('Messages:', messages)
    return render(request, 'messaging/room.html', {'user': user,'messages':messages})

@login_required
def message(request,user_id):
  msgs = Message.objects.all()
  print(msgs)
  user = get_object_or_404(User, id=user_id)
  form = MessageForm(request.POST)
  if form.is_valid():
    message = form.save(commit=False)
    print(f'req_user: {request.user}, user: {user}')
    message.sender = request.user
    message.receiver = user
    print(f'Message saved: sender={message.sender}, receiver={message.receiver}, content={message.content}')
    message.save()
    return redirect('room', user_id=user_id)
  else:
    print(form.errors)

def updateMsg(request,msg_id):
  msg = get_object_or_404(Message, id=msg_id)
  print(msg)
  if request.method == 'POST':
    form = MessageForm(request.POST,instance=msg)
    if form.is_valid():
      updated_message = form.save(commit=False)
      if msg.receiver:
        updated_message.receiver = msg.receiver
      updated_message.save()
      return redirect('/rooms/dashboard')
  else:
    form = MessageForm(instance=msg)
  return render(request, 'messaging/edit_message.html', {'form': form, 'message': msg})

def deleteMsg(request,msg_id):
  msg = get_object_or_404(Message, id=msg_id)
  msg.delete()
  return redirect('room', user_id=msg.receiver.id)

