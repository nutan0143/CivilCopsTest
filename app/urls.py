from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()


urlpatterns = [
	path("signup", UserRegistrationView.as_view()),
	path("login", LoginView.as_view()),
	path("user_interest", UserInterestView.as_view()),
]
