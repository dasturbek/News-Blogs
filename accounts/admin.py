from django.contrib import admin
from .models import Author, User, AccountModel
# Register your models here.

admin.site.register(AccountModel)
admin.site.register(Author)
admin.site.register(User)