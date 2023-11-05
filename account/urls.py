from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.LoginSignupViews.signup, name='register'),
    path('login/', views.LoginSignupViews.login, name='login'),
    path('profile/view/', views.ProfileViews.get_profile, name='profile'),
    path('profile/edit/', views.ProfileViews.edit_profile, name='update_profile'),
]
