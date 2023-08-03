from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import authentication_required
from .decorators import post_owner
from .forms import CreateForm, B_Post
from .models import BlogModel
from django.db.models import Count
from news.models import NewsModel
from comment.models import CommentModel

# Create your views here.
 
def blogView(request):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    posts = BlogModel.objects.all()
    best_posts = BlogModel.objects.annotate(upvote=Count('upvote_users')).order_by('-upvote')[:10]
    # best_posts = best_posts.order_by('date_posted'    
    return render(request=request, template_name='blog.html', context={'three_article':three_article, 'posts':posts, 'best_posts':best_posts})

def details_post(request, pk):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    best_posts = BlogModel.objects.annotate(upvote=Count('upvote_users')).order_by('-upvote')[:10]
    post = get_object_or_404(BlogModel, pk=pk)
    
    if request.method == 'POST': 
        text = request.POST.get('comment')   
        if text:      
            comment=CommentModel()
            comment.content = text
            comment.blog = post
            comment.user = request.user
            comment.save()
            return redirect(post.get_absolute_url())

    return render(request=request, template_name='./blogs/post_details.html', context={'three_article':three_article, 'post':post, 'best_posts':best_posts})

@authentication_required
def create_post(request):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    bpost= B_Post()
    if request.POST:
        form = CreateForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(post.get_absolute_url())        
    return render(request=request, template_name='./blogs/create_post.html', context={
        'three_article':three_article, 
        'abc':'Create Post',
        'bpost':bpost})

@authentication_required
@post_owner
def edit_post(request, pk):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    e_post = BlogModel.objects.get(pk=pk)
    bpost= B_Post({'content': e_post.content})
    if request.POST:
        if request.FILES.get('image') != None:
            e_post.image = request.FILES.get('image')
        e_post.title = request.POST.get('title')
        e_post.content = request.POST.get('content')
        e_post.save()
        return redirect(e_post.get_absolute_url())
    return render(request=request, template_name='./blogs/create_post.html', context={
        'three_article':three_article,
        'abc':'Edit Post', 
        'post':e_post,
        'bpost':bpost})

@post_owner
def delete_post(request, pk):
    BlogModel.objects.get(pk=pk).delete()
    return redirect('blog')

