# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Tag
from .forms import PostForm
from django.contrib import messages

# 文章列表
def post_list(request):
    posts = Post.objects.filter(is_published=True).select_related('author').prefetch_related('tags')
    print("posts:",posts)
    paginator = Paginator(posts, 5)  # 每页5篇文章
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

# blog/views.py
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()  # 确保传递
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comment_form': comment_form
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # 保存多对多关系（标签）
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

from .models import Comment
from .forms import CommentForm

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=True)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "评论已发布！")
            return redirect('blog:post_detail', pk=post.pk)
        else:
            # 如果表单无效，仍然返回到详情页（通常在模板中显示错误）
            messages.error(request, "评论发布失败，请检查内容。")
    else:
        form = CommentForm()
    
    # 通常，评论表单直接在 post_detail 模板中渲染，所以这里可能不需要单独渲染
    # 更常见的做法是：POST 失败时，带着表单错误重定向回详情页
    return redirect('blog:post_detail', pk=post.pk)