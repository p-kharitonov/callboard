
import os
import re
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    content = models.TextField(max_length=1000, verbose_name='Текст')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    is_active = models.BooleanField(verbose_name="Статус", default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'post/{self.pk}'

    @property
    def images(self):
        return Image.objects.filter(post__pk=self.pk)

    @property
    def videos(self):
        return Video.objects.filter(post__pk=self.pk)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-pk']


class Image(models.Model):
    alt = models.CharField(max_length=255, verbose_name='Описание изображения')
    url = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='URL')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Объявление')

    def __str__(self):
        return self.alt

    @property
    def path(self):
        return os.path.join(settings.MEDIA_URL, str(self.url))

    class Meta:
        verbose_name = 'Изобржение'
        verbose_name_plural = 'Изобржения'
        ordering = ['-pk']


class Video(models.Model):
    url = models.URLField(verbose_name='Ссылка на Youtube',
                          help_text='Например: https://www.youtube.com/watch?v=jNQXAC9IVRw')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Видео')

    def __str__(self):
        return self.url

    @property
    def code(self):
        re_code = r'youtube.com\/watch\?v=([-a-zA-Z0-9]+)'
        code = re.findall(re_code, str(self.url))
        if code:
            return code[0]
        else:
            return ''

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Объявление')
    content = models.TextField(max_length=500, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_accept = models.BooleanField(verbose_name="Подтвержден", default=False)
    is_active = models.BooleanField(verbose_name="Статус", default=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
