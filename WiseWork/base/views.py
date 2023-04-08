from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib import messages
from .models import Room,Topic,Message
from .forms import RoomForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from joblib import load
import numpy as np

def loginPage(request):

    if request.user.is_authenticated :
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.warning(request, 'User does not exsit')

        user = authenticate(request,username = username, password = password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.warning(request, "UserName or Password doesn't exist")

    return render(request, 'login.html')

def logoutPage(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    if request.user.is_authenticated :
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(str(username) + str(email) + str(password))

        user = User.objects.create_user(username,email,password)
        user.save()
        login(request,user)
        return redirect('home')
    else:
        messages.warning(request,"Can't Register")

    return render(request, "register.html")


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) | Q(name__icontains = q) | Q(description__icontains = q))
    room_count = rooms.count()
    topics = Topic.objects.all()
    room_message = Message.objects.filter(Q(room__topic__name__icontains = q)).order_by('-created')
    print(room_message)

    context = {
        'room' : rooms,
        'topics' : topics,
        'room_count' : room_count,
        'room_message' : room_message
    }


    return render(request, 'home.html',context)

@login_required(login_url='/loginPage')
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context  = {
        'form' : form
    }
    return render(request, 'room_form.html',context)

@login_required(login_url='/loginPage')
def userprofile(request,pk):
    user = User.objects.get(id = pk)
    room = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context={
        'user' : user,
        'room' : room,
        'room_message' : room_message,
        'topics' : topics
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/loginPage')
def room(request,pk):
    room = Room.objects.get(id = pk)

    message_all = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method  == "POST" :
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('message_send'),
        )
        room.participants.add(request.user)
        return redirect(request.META['HTTP_REFERER'])
        # return redirect('room', pk=room.id)

    context = {'room' : room, 'message_all' : message_all, 'participants' : participants}
    return render(request, 'room.html', context)

@login_required(login_url='/loginPage')
def updateRoom(request,pk):
    room = Room.objects.get(id = pk)
    form  = RoomForm()
    
    if request.user != room.host:
        messages.warning(request,"NOT ALLOWED TO UPDATE SOMEONE ELSE ROOM")
        return redirect('home')

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form}
    return render(request, 'room_form.html', context)

@login_required(login_url='/loginPage')
def deleteRoom (request,pk):
    room = Room.objects.get(id = pk)
    context = {'obj' : room }

    if request.user != room.host:
        messages.warning(request,"NOT ALLOWED TO DELETE SOMEONE ELSE ROOM")
        return redirect('home')

    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'delete.html',context)

@login_required(login_url='/loginPage')
def HeartAttack(request):
    lis = []
    if request.method == "POST":
        Age = request.POST.get('Age')
        if Age == None:
            Age = 0
        lis.append(Age)
        Sex = request.POST.get('Sex')
        if Sex == None:
            Sex = 0
        lis.append(Sex)
        Cp = request.POST.get('Cp')
        if Cp == None:
            Cp = 0
        lis.append(Cp)
        trtbps = request.POST.get('trtbps')
        if trtbps == None:
            trtbps = 0
        lis.append(trtbps)
        Chol = request.POST.get('Chol')
        if Chol == None:
            Chol = 0
        lis.append(Chol)
        Fbs = request.POST.get('Fbs')
        if Fbs == None:
            Fbs = 0
        lis.append(Fbs)
        Rest = request.POST.get('Rest')
        if Rest == None:
            Rest = 0
        lis.append(Rest)
        Thala = request.POST.get('Thala')
        if Thala == None:
            Thala = 0
        lis.append(Thala)
        Exec = request.POST.get('Exec')
        if Exec == None:
            Exec = 0
        lis.append(Exec)
        Old = request.POST.get('Old')
        if Old == None:
            Old = 0
        lis.append(Old)
        Slp = request.POST.get('Slp')
        if Slp == None:
            Slp = 0
        lis.append(Slp)
        Caa = request.POST.get('Caa')
        if Caa == None:
            Caa = 0
        lis.append(Caa)
        Thall = request.POST.get('Thall')
        if Thall == None:
            Thall = 0
        lis.append(Thall)
        lis = np.array(lis, dtype=float)
        model = load('finalized_model.sav')
    
        a = [23,0,0,142,200,0,0,144,0,2.8,0,0,2]

        ans = model.predict([lis])
        print(ans)
        context = {
            'result' : ans,
        }
        return render (request,'result/result.html',context)
    return render (request,'models/heart-attack.html')

@login_required(login_url='/loginPage')
def Daibetes(request):
    lis = []
    if request.method == "POST":

        poly = request.POST.get('poly')
        lis.append(poly)
        weight = request.POST.get('weight')
        lis.append(weight)
        pp = request.POST.get('pp')
        lis.append(pp)
        iri = request.POST.get('iri')
        lis.append(iri)
        ph = request.POST.get('ph')
        lis.append(ph)
        Age = request.POST.get('Age')
        lis.append(Age)
        vb = request.POST.get('vb')
        lis.append(vb)
        lis = np.array(lis,dtype=float)
        model = load('finalized2_model.sav')
        answer = model.predict([lis])
        print(answer)
        context = {
            'result' : answer,
        }
        return render (request,'result/daibetes_result.html',context)
    return render (request,'models/daibetes.html')

@login_required(login_url='/loginPage')
def LungCancer(request):
    context = {
        'result' : 'success'
    }
    return render (request,'models/lung-cancer.html',context)

@login_required(login_url='/loginPage')
def KidneyDisease(request):
    context = {
        'result' : 'success'
    }
    return render (request,'models/kidney-disease.html',context)