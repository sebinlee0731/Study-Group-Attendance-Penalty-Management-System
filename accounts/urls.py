from django.urls import path
from .views import UserMeView

urlpatterns = [
    path('users/me/', UserMeView.as_view()),
]