import functools
from django.shortcuts import redirect,get_object_or_404
from .models import BlogModel

def post_owner(view_func, redirect_url="blog"):
    @functools.wraps(view_func)
    def innner(request, pk, *args, **kwargs):
        e_post = get_object_or_404(BlogModel, pk=pk)
        if request.user == e_post.author:
            return view_func(request, pk, *args, **kwargs)
        return redirect(redirect_url)
    return innner


