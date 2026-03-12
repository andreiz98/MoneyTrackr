from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class AuthForm(AuthenticationForm):
    username = forms.CharField(label="Email or Username", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email or Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            if '@' in username_or_email:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    username = user_obj.username
                except User.DoesNotExist:
                    raise forms.ValidationError("User with this email does not exist")
            else:
                username = username_or_email

            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for x in self.fields:
            print(x)
            self.fields[x].widget.attrs['class'] = 'form-control'
            self.fields[x].widget.attrs['placeholder'] = 'Please enter your {}'.format(x).replace('_',' ')


    def clean(self):
        cleaned_data = self.cleaned_data

        check_email = User.objects.filter(email=cleaned_data.get('email'))
        if check_email.exists():
            self.add_error('email', 'Email already registered')

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        check_name = User.objects.filter(first_name=first_name, last_name=last_name)
        if check_name.exists():
            self.add_error('first_name', 'First name already registered')
            self.add_error('last_name', 'Last name already registered')

        return cleaned_data