from django.urls import path
from .views import (homeView,
                    aboutView,
                    contactView,
                    categoryView,
                    detailView,
                    create_article,
                    edit_article, 
                    delete_article,
                    categoriesView,
                    search
                    )

urlpatterns = [
    path('', homeView, name='home'),
    path('about/', aboutView, name='about'),
    path('contact/', contactView, name='contact'),
    path('article/<int:pk>/', detailView, name='articles'),
    path('create_article/', create_article, name='create_article'),
    path('article/<int:pk>/edit/', edit_article, name='edit_article'),
    path('article/<int:pk>/delete/', delete_article, name='delete_article'),
    path('article/categorys/', categoryView, name='category'),
    path('article/categorys/<str:c_name>/', categoriesView, name='categories'),
    path('search_results/', search, name='search_results') 
]