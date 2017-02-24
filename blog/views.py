from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Phone


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # lte means less than or equal
    phones = Phone.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts, 'phones': phones})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})