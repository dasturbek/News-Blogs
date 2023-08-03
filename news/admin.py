from django.contrib import admin
from .models import NewsModel, CategoryModel
# Register your models here.

admin.site.register(NewsModel)
admin.site.register(CategoryModel)