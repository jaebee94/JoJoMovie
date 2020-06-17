from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

# Create your views here.
def index(request):
    search_key = request.GET.get('search_key', None)
    search_type = request.GET.getlist('search_type', None)
    selected_val = None
    articles = Article.objects.order_by('-pk')
    if search_key:
        if 'title' in search_type:
            articles = articles.filter(title__contains=search_key)
            selected_val = 'title'
        elif 'content' in search_type:
            articles = articles.filter(content__contains=search_key)
            selected_val = 'content'
    else:
        articles = Article.objects.order_by('-pk')
        
    paginator = Paginator(articles, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'articles': articles,
        'page_obj': page_obj,
        'selected_val' : selected_val,
    }
    return render(request, 'community/index.html', context)

@login_required
def create(request):
    if request.method=='POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('community:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'community/form.html', context)

def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm()
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'community/article_detail.html', context)

@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user==article.user:
        if request.method=='POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                article = form.save(commit=False)
                article.user = request.user
                article.save()
                return redirect('community:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
        context = {
            'article': article,
            'form': form
        }
        return render(request, 'community/form.html', context)
    return redirect('community:detail', article.pk)

@login_required
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user==article.user:
        article.delete()
    else:
        return redirect('community:detail', article.pk)
    return redirect('movies:index')

@require_POST
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.article = article
        comment.save()
    return redirect('community:detail', article.pk)

@login_required
def comment_delete(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user==comment.user:
        comment.delete()
    return redirect('community:detail', article_pk)

@login_required
def comment_update(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user==comment.user:
        if request.method=='POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.save()
                return redirect('community:detail', article.pk)
        else:
            form = CommentForm(instance=comment)
        context = {
            'form': form
        }
        return render(request, 'community/form.html', context)
    return redirect('community:detail', article.pk)