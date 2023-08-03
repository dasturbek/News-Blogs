from django.urls import path
from .views import blogView, create_post, details_post, delete_post, edit_post

urlpatterns = [
    path('', blogView, name='blog'),
    path('create_post/', create_post, name='create_post'),
    path('<int:pk>/', details_post, name='post_details'),
    path('edit_post/<int:pk>/', edit_post, name='edit_post'),
    path('delete_post/<int:pk>/', delete_post, name='delete_post'),
]