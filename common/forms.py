from django import forms  
from common.models import UserProfile 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm


class UserCreationFormNew(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationFormNew, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'form-control'}
        self.fields['password1'].widget.attrs = {'class': 'form-control'}
        self.fields['password2'].widget.attrs = {'class': 'form-control'}
  
class ProfileCreationForm(forms.ModelForm):  
  
    class Meta:  
        model = UserProfile  
        fields = '__all__'



class ProfileEditForm(forms.ModelForm):  


    class Meta:  
        model = User  
        fields = ['username','first_name','last_name', 'email' ]

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'form-control'}
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['first_name'].widget.attrs = {'class': 'form-control'}
        self.fields['last_name'].widget.attrs = {'class': 'form-control'}
        self.fields['email'].widget.attrs = {'class': 'form-control'}