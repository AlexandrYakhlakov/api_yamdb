from collections import namedtuple

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import (
    LEN_OF_SYMBL, MAX_LENGTH_NAME, MAX_LENGTH_SLUG
)
from reviews.validators import validate_username, validate_year

MIN_SCORE = 1
MAX_SCORE = 10

Role = namedtuple('Role', ('role', 'widget'))
ADMIN = Role('admin', 'Администратор')
MODERATOR = Role('moderator', 'Модератор')
AUTH_USER = Role('user', 'Пользователь')


class User(AbstractUser):
    USERNAME_LENGTH = 150
    EMAIL_LENGTH = 254
    CONFIRMATION_CODE_LENGTH = 5
    ROLE_LENGTH = 9

    ROLE_CHOICES = (
        (*ADMIN,),
        (*MODERATOR,),
        (*AUTH_USER,)
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=AUTH_USER.role,
        max_length=ROLE_LENGTH,
        verbose_name='Роль',
        blank=True
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    confirmation_code = models.CharField(
        blank=True,
        null=True,
        default=None,
        max_length=CONFIRMATION_CODE_LENGTH,
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
        ordering = ('-date_joined',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


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
        validators=(validate_year,),
        verbose_name='Год произведения',
    )

    class Meta:
        ordering = ('-year', 'name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:LEN_OF_SYMBL]


class CommonData(models.Model):
    """Абстрактный класс."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.'),
    )

    class Meta:
        abstract = True
        ordering = ('name', )

    def __str__(self) -> str:
        return self.name[:LEN_OF_SYMBL]


class Genre(CommonData):
    """Модель для Жанров произведений."""

    class Meta(CommonData.Meta):
        verbose_name = 'Жанр',
        verbose_name_plural = 'Жанры'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_name = self._meta.get_field('name')
        field_slug = self._meta.get_field('slug')
        field_name.verbose_name = 'Жанр'
        field_name.help_text = 'К какому жанру относится произведение'
        field_slug.verbose_name = 'Слаг жанра'


class Category(CommonData):
    """Модель для Категорий произведений."""

    class Meta(CommonData.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_name = self._meta.get_field('name')
        field_slug = self._meta.get_field('slug')
        field_name.verbose_name = 'Категория'
        field_name.help_text = 'Название категории произведения'
        field_slug.verbose_name = 'Слаг категории'


class ContentBase(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='%(class)ss',
    )

    def __str__(self):
        return self.text[:LEN_OF_SYMBL]

    class Meta:
        abstract = True
        ordering = ('-pub_date', )


class Review(ContentBase):
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE)
        ],
        verbose_name='Рейтинг произведения'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    class Meta(ContentBase.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )


class Comment(ContentBase):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta(ContentBase.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
