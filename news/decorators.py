import functools
from django.shortcuts import redirect, get_object_or_404
from .models import NewsModel

def article_owner(view_func, redirect_url="home"):
    @functools.wraps(view_func)
    def innner(request, pk, *args, **kwargs):
        article = get_object_or_404(NewsModel, pk=pk)
        if request.user == article.author:
            return view_func(request, pk, *args, **kwargs)
        return redirect(redirect_url)
    return innner


