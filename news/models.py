from django.db import models
from accounts.models import AccountModel, Author
from django.urls import reverse

# Create your models here.

class ContactModel(models.Model):
    message = models.TextField()
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=False)
    subject = models.CharField(max_length=250)
    
    def __str__(self):
        return self.subject

class CategoryModel(models.Model):
    name = models.CharField(max_length=50, default='other')
    description = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name
    
class NewsModel(models.Model):
    date_posted = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='./img/news_images/', blank=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.DO_NOTHING, related_name='news')
    status = models.PositiveIntegerField(default=0, blank=True) #admin buning qiymatini beradi va shu orqali viewda ishlatildi
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='news')
    upvote_users = models.ManyToManyField(AccountModel, related_name='upvoted_posts', blank=True)

    def __str__(self):
        return self.title

    def get_no_of_upvote(self):
        return self.upvote_users.count()
    
    def get_absolute_url(self):
        return reverse('articles', args=[str(self.pk)])
    