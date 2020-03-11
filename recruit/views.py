from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Application, Profile, User
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .forms import ApplicationForm, UserForm, ProfileForm, SignupForm, SigninForm
from django.contrib.auth.models import User as authUser
from django.views.generic import (
    DetailView, ListView, CreateView,
    DeleteView, UpdateView, View)
from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from datetime import datetime



# Create your views here.


class NewView(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'new.html'

    def form_valid(self, form):
        self.object = form.save()
        user = self.request.user
        self.object.created_by = user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, '임시 저장되었습니다.')
        return reverse('show')


class ShowView(ListView):
    template_name = 'show.html'
    model = Application

    def get_queryset(self):
        new_queryset = {}
        application = Application.objects.get(created_by=self.request.user)
        new_queryset['art'] = application
        return new_queryset


class EditView(UpdateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'edit.html'

    def get_success_url(self):
        messages.success(self.request, '임시 저장되었습니다.')
        return reverse('show')


class CustomLoginView(LoginView):
    def get_context_data(self, **kwargs):
        new_context = super().get_context_data(**kwargs)
        try:
            new_context['art'] = get_object_or_404(Application, created_by=self.request.user)
        except:
            pass
        return new_context


def submit(request):
    art = get_object_or_404(Application, created_by=request.user)
    art.final = True
    art.save()
    return render(request, 'registration/login.html', {'art':art})


def delete(request):
    art = get_object_or_404(Application, created_by=request.user)
    art.delete()
    return render(request, 'registration/login.html')


class SignupView(ListView):
    model = Profile
    template_name = 'signup.html'

    def post(self, request, *args, **kwargs): 
        user_form = SignupForm(request.POST or None)
        profile_form = ProfileForm(request.POST or None)
        if user_form.is_valid() and profile_form.is_valid():
            user = User.objects.create_user(
                username=request.POST["username"], password=request.POST["password1"])
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile = Profile.objects.create_user(
                major=request.POST["major"], semester=request.POST["semester"], phone=request.POST["phone"], interview_date=request.POST["interview_date"])
            profile.user = user
            profile.save()
            auth.login(request, user, profile)
            messages.success(request, '회원가입 완료. 로그인 해 주세요.')
            return HttpResponseRedirect(reverse('main'))
        else:
            messages.warning(request, '회원가입에 실패했습니다. 다시 작성해주세요')
            return HttpResponseRedirect(reverse('signup'))


class UserUpdate(UpdateView):
    model = Profile
    template_name = 'u_edit.html'
    form_class = ProfileForm

    def post(self, request, *args, **kwargs):
        profile_form = ProfileForm(request.POST or None)
        if profile_form.is_valid():
            profile = Profile.objects.get(user=request.user)
            profile.semester, profile.phone = request.POST['semester'], request.POST['phone']
            profile.major, profile.interview_date = request.POST['major'], request.POST['interview_date']
            messages.success(request, '회원 정보 수정 완료')
            return HttpResponseRedirect(reverse('main'))
        else:
            messages.warning(request, '회원 정보 수정에 실패했습니다.')
            return HttpResponseRedirect(reverse('main'))

def signin(request):#로그인 기능
    start = datetime.strptime("2020-03-10 20:34:00", '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime("2020-03-10 20:34:10", '%Y-%m-%d %H:%M:%S')
    now = timezone.localtime()
    if request.method == "GET":
        return render(request, 'registration/login.html', {'f':SigninForm(),'start':start, 'end':end, 'now':now} )

    elif request.method == "POST":
        form = SigninForm(request.POST)
        id = request.POST.get('username')
        pw = request.POST.get('password')
        u = authenticate(username=id, password=pw)
        if u: #u에 특정 값이 있다면
            login(request, user=u) #u 객체로 로그인해라
            return HttpResponseRedirect(reverse('main', {'start':start, 'end':end, 'now':now}))
        else:
            return render(request, 'registration/login.html',{'f':form, 'error':'아이디나 비밀번호가 일치하지 않습니다.'})


from django.contrib.auth import logout #logout을 처리하기 위해 선언

def signout(request): #logout 기능
    logout(request) #logout을 수행한다.
    return HttpResponseRedirect(reverse('main'))

def guide(request):
    return render(request, 'guide.html')

def faq(request):
    return render(request, 'faq.html')
