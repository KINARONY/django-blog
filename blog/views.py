from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm

from .models import Article
from .forms import ArticleForm


def article_list(request):
    articles = Article.objects.all().order_by('-created_on')
    return render(request, 'blog/article_list.html', {'articles': articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'blog/article_detail.html', {'article': article})


@login_required
def article_create(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        return redirect('article_detail', pk=article.pk)
    return render(request, 'blog/article_form.html', {'form': form})


@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.author != request.user:
        return HttpResponseForbidden("Нельзя редактировать чужую статью")

    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect('article_detail', pk=article.pk)

    return render(request, 'blog/article_form.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.author != request.user:
        return HttpResponseForbidden("Нельзя удалить чужую статью")

    if request.method == 'POST':
        article.delete()
        return redirect('article_list')

    return render(request, 'blog/article_confirm_delete.html', {'article': article})
