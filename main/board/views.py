from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView,  DeleteView
from django.db.models import Count
from .models import Post, Category


class HomeView(ListView):
    model = Post
    template_name = 'board/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        return super().get_queryset()[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects \
            .annotate(number_post=Count('post')) \
            .filter(number_post__gt=0) \
            .order_by('-number_post')[:4]
        context['popular_posts'] = Post.objects.all() \
            .annotate(number_message=Count('message')) \
            .filter(number_message__gt=0) \
            .order_by('-number_message')[:4]
        context['popular_users'] = User.objects.all() \
            .annotate(number_post=Count('post')) \
            .filter(number_post__gt=0) \
            .order_by('-number_post')[:4]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post.html'
    context_object_name = 'post'