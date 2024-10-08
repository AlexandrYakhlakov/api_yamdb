from collections import namedtuple

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.constants import (
    LEN_OF_SYMBL, MAX_LENGTH_DESCRIPTION,
    MAX_LENGTH_NAME, MAX_LENGTH_SLUG
)
from reviews.validators import validate_username, validate_year
from . constants import MIN_SCORE, MAX_SCORE


Role = namedtuple('Role', ('role', 'widget'))
ADMIN = Role('admin', 'Администратор')
MODERATOR = Role('moderator', 'Модератор')
AUTH_USER = Role('user', 'Пользователь')


class User(AbstractUser):
    USERNAME_LENGTH = 150
    EMAIL_LENGTH = 254
    ROLE_CHOICES = (
        (*ADMIN,),
        (*MODERATOR,),
        (*AUTH_USER,)
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=AUTH_USER.role,
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
        max_length=36,
    )

    email = models.EmailField(
        max_length=EMAIL_LENGTH,
        blank=False,
        unique=True
    )

    username = models.CharField(
        max_length=USERNAME_LENGTH,
        unique=True,
        validators=(validate_username,)
    )

    @property
    def is_admin(self):
        return self.role == ADMIN.role or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR.role

    class Meta:
        ordering = ('-id',)


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
        related_name='titles',
        verbose_name='Жанр',
        help_text='К какому жанру относится произведение'
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
        validators=[validate_year],
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
        help_text=(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        ),
    )

    class Meta:
        ordering = ('name',)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name[:LEN_OF_SYMBL]


class ReviewCommentBase(models.Model):
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    def __str__(self):
        return self.text[:LEN_OF_SYMBL]

    class Meta:
        abstract = True
        ordering = ('-pub_date', )
        default_related_name = '%(class)ss'


class Review(ReviewCommentBase):
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(MIN_SCORE),
                    MaxValueValidator(MAX_SCORE)
        ],
        verbose_name='Оценка'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta(ReviewCommentBase.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )


class Comment(ReviewCommentBase):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta(ReviewCommentBase.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
