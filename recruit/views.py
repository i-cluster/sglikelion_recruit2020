from django.shortcuts import render, get_object_or_404, reverse
from django.utils import timezone
from .models import Application, Profile, User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import ApplicationForm, ProfileForm, SignupForm
from django.views.generic import ListView, CreateView, UpdateView
from django.http.response import HttpResponseRedirect
from datetime import datetime
from django.contrib.auth import logout


class NewView(CreateView):
    form_class = ApplicationForm
    template_name = 'new.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, '먼저 로그인을 해 주세요.')
            return HttpResponseRedirect(reverse('main'))
        return super().get(request, *args, **kwargs)

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
    context_object_name = 'new_context'

    def get_queryset(self):
        new_queryset = {}
        application = Application.objects.get(created_by=self.request.user)
        new_queryset['art'] = application
        return new_queryset

    def get_context_data(self, **kwargs):
        new_context = super().get_context_data(**kwargs)
        new_context['start'] = datetime.strptime("2020-03-16 10:00:00", '%Y-%m-%d %H:%M:%S')
        new_context['end'] = datetime.strptime("2020-03-22 22:00:00", '%Y-%m-%d %H:%M:%S')
        new_context['now'] = timezone.localtime()
        return new_context


class EditView(UpdateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'edit.html'

    def get(self, request, *args, **kwargs):
        if request.user != Application.objects.get(id=kwargs['pk']).created_by:
            messages.error(request, '수정 권한이 없습니다.')
            return HttpResponseRedirect(reverse('main'))
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, '임시 저장되었습니다.')
        return reverse('show')


class CustomLoginView(LoginView):
    context_object_name = 'new_context'

    def get_context_data(self, **kwargs):
        new_context = super().get_context_data(**kwargs)
        new_context['start'] = datetime.strptime("2020-03-16 10:00:00", '%Y-%m-%d %H:%M:%S')
        new_context['end'] = datetime.strptime("2020-03-22 22:00:00", '%Y-%m-%d %H:%M:%S')
        new_context['now'] = timezone.localtime()
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


class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = SignupForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, '이미 로그인 되어있습니다.')
            return HttpResponseRedirect(render('main'))
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        profile_form = ProfileForm(self.request.POST or None)
        profile = profile_form.save(commit=False)
        profile.user = self.object
        profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, '회원가입 완료. 로그인 해 주세요.')
        return reverse('main')


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


def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))


def guide(request):
    return render(request, 'guide.html')


def faq(request):
    return render(request, 'faq.html')

def notice(request):
    return render(request, 'notice.html')
