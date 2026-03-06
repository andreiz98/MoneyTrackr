from django.contrib.auth.models import User
from django.views.generic import CreateView

from register.forms import UserForm


# Create your views here.

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    model = User
    form_class = UserForm
    success_url = '/login/'

