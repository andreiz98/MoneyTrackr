from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for x in self.fields:
            print(x)
            self.fields[x].widget.attrs['class'] = 'form-control'
            self.fields[x].widget.attrs['placeholder'] = 'Please enter your {}'.format(x).replace('_',' ')

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for x in self.fields:
            print(x)
            self.fields[x].widget.attrs['class'] = 'form-control'
            self.fields[x].widget.attrs['placeholder'] = 'Please enter your {}'.format(x).replace('_',' ')