from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from apps.user.models import CustomUser



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'data-error': 'Введите Email корректно',
        'placeholder' : 'Введите Email'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder' : 'Пароль'
    }))

    class Meta:
        model = CustomUser
        fields = ['username','password']


    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.label=""
            field.widget.attrs['id'] = f'login_form_{name}'
        
       
class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']
     

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.label=""
            field.widget.attrs['id'] = f'registration_form_{name}'
    