from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic import CreateView, FormView

from register.forms import UserForm


# Create your views here.

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    model = User
    form_class = UserForm
    success_url = '/login/'

    def form_valid(self, form):
        user = form.save(commit=False)

        subject = f'Welcome to MoneyTrackr {user.username}'
        message = f'''Hello {user.username},
                    Your account was successfully created.
                
                    You can login here:
                    http://127.0.0.1:8000/login/
                    
                    MoneyTrackr Team'''

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        user.save()

        return redirect("login")
