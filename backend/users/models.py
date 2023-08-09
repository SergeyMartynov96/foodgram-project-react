from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Создаю класс для собственной модели пользователя"""
    username = models.CharField(verbose_name='Имя пользователя',
                                max_length=settings.MAX_LENGTH, unique=True)
    email = models.EmailField(verbose_name='Электронная почта',
                              max_length=settings.MAX_LENGTH_EM, unique=True)
    first_name = models.CharField(verbose_name='Имя',
                                  max_length=settings.MAX_LENGTH)
    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=settings.MAX_LENGTH)
    password = models.CharField(verbose_name='Пароль',
                                max_length=settings.MAX_LENGTH)

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Создаю класс для подписки пользователей на авторов"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Пользователь',
                             )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор',
                               )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            ),
            models.CheckConstraint(
                check=~models.Q(
                    author=models.F("user")),
                name="\nНельзя подписаться на себя\n"
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'
