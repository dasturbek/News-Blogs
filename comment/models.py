from django.db import models
from accounts.models import AccountModel
from blog.models import BlogModel

# Create your models here.

class CommentModel(models.Model):
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=False)
    user = models.ForeignKey(AccountModel, on_delete=models.CASCADE)
    