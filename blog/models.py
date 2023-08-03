from django.db import models
from accounts.models import AccountModel
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget

# Create your models here.

class BlogModel(models.Model):
    date_posted = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, blank=False)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="./img/blogs_images/", blank=False)
    author = models.ForeignKey(AccountModel, on_delete=models.CASCADE, related_name='blogs')
    upvote_users = models.ManyToManyField(AccountModel, related_name='upvoted', blank=True)

    def __str__(self):
        return self.title

    def get_no_of_upvote(self):
        return self.upvote_users.count()
    
    def get_absolute_url(self):
        return reverse('post_details', args=[str(self.pk)])
        
    