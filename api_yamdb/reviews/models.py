from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from collections import namedtuple

from api.constants import (
    LEN_OF_SYMBL, MAX_LENGTH_DESCRIPTION, MAX_LENGTH_NAME, MAX_LENGTH_SLUG
)
from api.validators import validator_year_title


Role = namedtuple('Role', ('role_value', 'widget_value'))
admin = Role('admin', 'Администратор')
moderator = Role('moderator', 'Модератор')
auth_user = Role('user', 'Пользователь')


class User(AbstractUser):
    ROLE_CHOICES = (
        (*admin,),
        (*moderator,),
        (*auth_user,)
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=auth_user.role_value,
        max_length=50,
        verbose_name='Роль',
        blank=True
    )

    bio = models.CharField(
        blank=True,
        max_length=500,
        verbose_name='Биография'
    )

    confirmation_code = models.CharField(
        blank=True,
        null=True,
        default=None,
        max_length=255
    )

    @property
    def is_admin(self):
        return self.role == admin.role_value

    class Meta:
        ordering = ('-id',)


# @receiver(post_save, sender=User)
# def post_save(instance, created, **kwargs):
#     if created:
#         confirmation_code = '1235'
#         instance.confirmation_code = confirmation_code
#         instance.save()


class Title(models.Model):
    """Модель для Произведений."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Произведение',
        help_text='Название произведения',
    )
    description = models.TextField(
        blank=True,
        null=True,
        max_length=MAX_LENGTH_DESCRIPTION,
        verbose_name='Описание произведения',
        help_text='Опишите вкратце ваше произведение'
    )
    genre = models.ManyToManyField(
        'Genre',
        blank=True,
        # null=True,
        related_name='titles',
        verbose_name='Жанр',
        help_text='К какому жанру относится произведение',
    )
    category = models.ForeignKey(
        'Category',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        help_text='Название категории произведения'
    )
    year = models.PositiveSmallIntegerField(
        validators=[validator_year_title,],
        verbose_name='Год произведения',
    )

    class Meta:
        ordering = ('-year', 'name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:LEN_OF_SYMBL]


class Genre(models.Model):
    """Модель для Жанров произведений."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Жанр',
        help_text='К какому жанру относится произведение'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        verbose_name='Слаг жанра',
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.'),
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Жанр',
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name[:LEN_OF_SYMBL]


class Category(models.Model):
    """Модель для Категорий произведений."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Категория',
        help_text='Название категории произведения',
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        verbose_name='Слаг категории',
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.'),
    )

    class Meta:
        ordering = ('name',)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name[:LEN_OF_SYMBL]
