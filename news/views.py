from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, CreateForm
from accounts.decorators import authentication_required, author_create
from .decorators import article_owner
from .models import NewsModel, CategoryModel
from accounts.models import AccountModel

from blog.forms import B_Post

from django.http import QueryDict
# Create your views here.

def homeView(request):
    if request.user.is_authenticated:
        person = AccountModel.objects.get(username=request.user)
    else:
        person = None
    # status=4 bu asosiy 1 ta news $yuqori
    # status=3 bu asosiy 3 news $o'rta
    # status=2 esa asosiyga yordamchi $quyi
    # status=1 esa saytga tegishli yangilik
    one_article = NewsModel.objects.filter(status=4).order_by('-date_posted')[:1]
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    articles = NewsModel.objects.filter(status=2).order_by('-date_posted')[:5]
    for_you_article = NewsModel.objects.filter(status=4).order_by('-date_posted')[1:8]
    weekly_top_news = NewsModel.objects.filter(status=3).order_by('-date_posted')[0:8]
    return render(request=request, template_name='index.html', context={
        'person':person,
        'articles':articles,
        'weekly_top_news':weekly_top_news,
        'for_you_article':for_you_article,
        'three_article':three_article,
        'one_article':one_article})

def contactView(request):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    if request.user.is_authenticated:
        name = request.user.last_name + ' ' + request.user.first_name
        email = request.user.email
    else:
        name = request.POST.get('name')
        email = request.POST.get('email')
    fields = {'name':name, 'email':email}
    contextC = {'alo':"", 'three_article':three_article,}
    
    if request.POST:
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        fields['message'] = message
        fields['subject'] = subject
        fields['csrfmiddlewaretoken'] = request.POST.get('csrfmiddlewaretoken')
        query_dict = QueryDict('', mutable=True)
        query_dict.update(fields)
        form = ContactForm(query_dict)
        if form.is_valid():      
            form.save()   
            contextC['alo'] = "Xabaringiz tez kunda ko'rib chiqiladi"
        else:
            print(form.errors)
        
    return render(request=request, template_name='contact.html', context=contextC)

def aboutView(request):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    return render(request=request, template_name='about.html', context={'three_article':three_article})

def detailView(request, pk):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    article = get_object_or_404(NewsModel, pk=pk)
    categories = CategoryModel.objects.all()
    return render(request=request, template_name='./news/article_details.html', context={'three_article':three_article,'article':article, 'categories':categories})

@authentication_required
@author_create
def create_article(request):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    bpost= B_Post()
    categories = CategoryModel.objects.all()
    if request.POST:
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.category = CategoryModel.objects.get(name=request.POST.get('category'))
            article.author = request.user
            article.save()
            return redirect(article.get_absolute_url())        
    return render(request=request, template_name='./news/create_article.html', context={
        'three_article':three_article, 
        'categories':categories,
        'bpost':bpost})

@authentication_required
@article_owner
def edit_article(request, pk):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    article = get_object_or_404(NewsModel, pk=pk)
    bpost= B_Post({'content': article.content})
    if request.POST:
        if request.FILES.get('image') != None:
            article.image = request.FILES.get('image')
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.save()
        return redirect(article.get_absolute_url())
    return render(request=request, template_name='./blogs/create_post.html', context={
        'abc':'Edit Post',
        'post':article,
        'three_article':three_article,
        'bpost':bpost})

@article_owner
def delete_article(request, pk):
    NewsModel.objects.get(pk=pk).delete()
    return redirect('home')

def categoryView(request):    
    articles = NewsModel.objects.all().order_by('-date_posted')  
    weekly_top_news = NewsModel.objects.filter(status=3).order_by('-date_posted')[0:8]
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    return render(request=request, template_name='category.html', context={'three_article':three_article, 'articles':articles, 'weekly_top_news':weekly_top_news})

def categoriesView(request, c_name):
    articles = NewsModel.objects.filter(category__name=c_name).order_by('-date_posted')
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    weekly_top_news = NewsModel.objects.filter(status=3).order_by('-date_posted')[0:8]
    return render(request=request, template_name='category.html', context={'three_article':three_article,'articles':articles, 'c_name':c_name, 'weekly_top_news':weekly_top_news})

def search(request):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    if request.POST:
        print(request.POST.get('searcher'))
    return render(request, template_name='search.html', context={'three_article':three_article,})
