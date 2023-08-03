from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db.models import Q

# Create your models here.

user_types = [
        ("A",'Author'),
        ("U",'User')
    ]
class AccountModel(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    status = models.PositiveIntegerField(default=0, blank=True)
    phone_number = models.CharField(blank=True, default='', max_length=25)
    image = models.ImageField(upload_to="./img/accounts_images/", blank=True)
    role = models.CharField(choices=user_types, max_length=50, default='U')
    job = models.CharField(max_length=100, default='Human')
    staj = models.PositiveIntegerField(blank=True, default=0)
    birthday = models.DateField(null=True)
    bio = models.CharField(max_length=250, default='', blank=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = ("Account")
        verbose_name_plural = ("Accounts")
    
    def get_absolute_url(self):
        return reverse('account', args=[str(self.username)])
    
class UserManager(models.Manager):
    def get_queryset(self):
        return super(UserManager, self).get_queryset().filter(Q(role='A') | Q(role='U'))

class AuthorManager(models.Manager):
    def get_queryset(self):
        return super(AuthorManager, self).get_queryset().filter(role='A')

class User(AccountModel):
    objects = UserManager()
    class Meta:
        proxy = True

class Author(AccountModel):
    objects = AuthorManager()
    class Meta:
        proxy = True
        
