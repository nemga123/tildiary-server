from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import LogInView, SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("login/", LogInView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]
