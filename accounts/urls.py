from django.urls import path
from .views import (
    user_login, 
    register, 
    personal_articles, 
    personal_posts, 
    personal_settings, 
    personal_details,
    details,
    phone_number,
    change_password,
    change_email
    )
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('signup/', register, name = 'sign_up'),
    path('signin/', user_login, name = 'sign_in'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('<str:username>/articles/', personal_articles, name='personal_articles'),
    path('<str:username>/posts/', personal_posts, name='personal_posts'),
    path('settings/', personal_settings, name='settings_profile'),
    path('<str:username>/', personal_details, name='account'),
    
    path('settings/details/', details, name='details'),
    path('settings/phone/', phone_number, name='phone_number'),
    path('settings/change_email/', change_email, name='change_email'),
    path('settings/change_password/', change_password, name='change_password'),
]
