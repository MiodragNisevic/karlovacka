from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Phone
from .forms import PostForm
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    # lte means less than or equal
    phones = Phone.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts, 'phones': phones})


# def post_list(request):
    # phones = Phone.objects.all()
    #
    # posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # paginator = Paginator(posts_list, 3)
    #
    # page = request.GET.get('page')
    # try:
    #     posts = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     posts = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     posts = paginator.page(paginator.num_pages)
    #
    # return render(request, 'blog/post_list.html', {'posts': posts, 'phones': phones})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()  #ovaj red bi odmah publishovao post
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now() #ovaj red bi odmah publishovao post
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
