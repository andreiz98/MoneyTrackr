from django.urls import path

from register import views

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='register_user'),
]