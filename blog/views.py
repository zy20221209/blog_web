# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Post, Tag
from .forms import PostForm
from django.contrib import messages
from django.db.models import Q
# 文章列表


def post_list(request):
     # 获取搜索关键词
    query = request.GET.get('q', '').strip()

    # 修改这里：使用 is_published 而不是 published
    post_list = Post.objects.filter(is_published=True).order_by('-created_at')
    
    if query:
        post_list=post_list.filter(
            Q(title__icontains=query)
        )

    paginator = Paginator(post_list, 5)  # 每页 5 篇
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 非整数页码，跳转到第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # 超出范围（如999），跳转到最后一页
    except:
        page_obj = paginator.page(1)  # 兜底处理


    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'query':query
    })

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

# @login_required
# def add_comment(request, pk):
#     post = get_object_or_404(Post, pk=pk, is_published=True)
    
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = request.user
#             comment.save()
#             messages.success(request, "评论已发布！")
#             return redirect('blog:post_detail', pk=post.pk)
#         else:
#             # 如果表单无效，仍然返回到详情页（通常在模板中显示错误）
#             messages.error(request, "评论发布失败，请检查内容。")
#     else:
#         form = CommentForm()
    
#     # 通常，评论表单直接在 post_detail 模板中渲染，所以这里可能不需要单独渲染
#     # 更常见的做法是：POST 失败时，带着表单错误重定向回详情页
#     return redirect('blog:post_detail', pk=post.pk)

def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=True)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')  # 或返回错误
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "评论已发布！")
            return redirect('blog:post_detail', pk=post.pk)
        # 如果失败，继续往下走，渲染页面并显示错误
        else:
            print("表单验证失败")
            print(form.errors)
            messages.error(request,"评论发布失败，请检查内容")
    else:
        form = CommentForm()

    # 渲染详情页，包含文章、评论列表、评论表单
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'form': form,
    })
