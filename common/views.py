from django.views.generic import FormView
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate  
from common.forms import ProfileCreationForm, ProfileEditForm ,UserCreationFormNew
from django.http.response import HttpResponseRedirect  
from django.urls import reverse_lazy  
from allauth.socialaccount.models import SocialAccount

from django.contrib.auth.models import User


def index(request):  
    context = {}  
    if request.user.is_authenticated:  
        print(request.user)
        context['username'] = request.user.username
        if not  request.user.set_unusable_password:
            context['github_url'] = SocialAccount.objects.get(provider='github', user=request.user).extra_data['html_url']
        else:
            context['github_url'] = 'local'
    return render(request, 'index.html', context)  
  
  



  
  
class RegisterView(FormView):  
  
    form_class = UserCreationFormNew  



    def form_valid(self, form):  
        form.save()  
        username = form.cleaned_data.get('username')  
        raw_password = form.cleaned_data.get('password1')  
        login(self.request, authenticate(username=username, password=raw_password))  
        return super(RegisterView, self).form_valid(form)  
  
  
class CreateUserProfile(FormView):  
  
    form_class = ProfileCreationForm
    template_name = 'profile-create.html'
    success_url = reverse_lazy('common:index')
  
    def dispatch(self, request, *args, **kwargs):  
        if self.request.user.is_anonymous:  
            return HttpResponseRedirect(reverse_lazy('common:login'))  
        return super(CreateUserProfile, self).dispatch(request, *args, **kwargs)  
  
    def form_valid(self, form):  
        instance = form.save(commit=False)  
        instance.user = self.request.user  
        instance.save()  
        return super(CreateUserProfile, self).form_valid(form)


def EditProfile(request):
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            return render(request, 'profile.html', {'form': form, 'btn': 'Редактировать','msg': 'Успешное редактирование'})
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'profile.html', {'form': form, 'btn': 'Редактировать'})
