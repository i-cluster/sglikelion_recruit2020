from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Application
from .forms import ApplicationForm, SignupForm, SigninForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password 

# Create your views here.

def main(request):
    art = Application.objects.filter(author=request.user)
    if art:
        return render(request, 'main.html', {'art':art})
    else:
        return render(request, 'main.html')

def new(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            art = form.save(commit=False)
            art.date = timezone.now()
            art.author = request.user
            art.final = False
            art.save()
            return redirect('show')
    else:
        form = ApplicationForm()
        return render(request, 'new.html',{'art':form})

def show(request):
    art = get_object_or_404(Application, author=request.user)
    return render(request, 'show.html', {'art':art})

def edit(request):
    art = get_object_or_404(Application, author=request.user)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=art)
        if form.is_valid():
            art = form.save(commit=False)
            art.date = timezone.now()
            art.save()
            return redirect('show')
    else:
        form = ApplicationForm(instance=art)
        return render(request, 'edit.html',{'art':form})

def submit(request):
    art = get_object_or_404(Application, author=request.user)
    art.final = True
    art.save()
    return render(request, 'show.html', {'art':art})

def delete(request):
    art = get_object_or_404(Application, author=request.user)
    art.delete()
    return render(request, 'main.html')

def signup(request):#역시 GET/POST 방식을 사용하여 구현한다.
    if request.method == "GET":
        return render(request, 'signup.html', {'f':SignupForm()} )
        
    elif request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password_check']:
                new_user = User.objects.create_user(form.cleaned_data['username'],form.cleaned_data['email'],form.cleaned_data['password'])
                new_user.last_name = form.cleaned_data['last_name']
                new_user.first_name = form.cleaned_data['first_name']
                new_user.save()
                auth.login(request, new_user)
                return HttpResponseRedirect(reverse('main'))
            else:
                return render(request, 'signup.html',{'f':form, 'error':'비밀번호와 비밀번호 확인이 다릅니다.'})#password와 password_check가 다를 것을 대비하여 error를 지정해준다.
        return render(request, 'signup.html',{'f':form})

def signin(request):#로그인 기능
    if request.method == "GET":
        return render(request, 'signin.html', {'f':SigninForm()} )

    elif request.method == "POST":
        form = SigninForm(request.POST)
        id = request.POST.get('username')
        pw = request.POST.get('password')
        u = authenticate(username=id, password=pw)
        if u: #u에 특정 값이 있다면
            login(request, user=u) #u 객체로 로그인해라
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'signin.html',{'f':form, 'error':'아이디나 비밀번호가 일치하지 않습니다.'})

from django.contrib.auth import logout #logout을 처리하기 위해 선언

def signout(request): #logout 기능
    logout(request) #logout을 수행한다.
    return HttpResponseRedirect(reverse('signin'))