from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import ChatRoom, Message, DirectMessage
from .forms import ChatRoomForm, MessageForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('room_list')
    else:
        form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('room_list')
    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

@login_required
def room_list(request):
    rooms = ChatRoom.objects.all()
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.created_by = request.user
            room.save()
            return redirect('room', room_name=room.name)
    else:
        form = ChatRoomForm()
    return render(request, 'chat/room_list.html', {
        'rooms': rooms, 'users': users, 'form': form
    })

@login_required
def room(request, room_name):
    chat_room = get_object_or_404(ChatRoom, name=room_name)
    messages = chat_room.messages.all()
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(room=chat_room, sender=request.user, content=content)
        return redirect('room', room_name=room_name)
    return render(request, 'chat/room.html', {
        'room': chat_room, 'messages': messages
    })

@login_required
def direct_chat(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = DirectMessage.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    )
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            DirectMessage.objects.create(
                sender=request.user, receiver=other_user, content=content
            )
        return redirect('direct_chat', username=username)
    return render(request, 'chat/direct_chat.html', {
        'other_user': other_user, 'messages': messages
    })