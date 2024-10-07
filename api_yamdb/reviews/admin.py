from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title, User

# Глобально переопределяем в админке отображение NULL.
admin.site.empty_value_display = '-пока пусто-'


class GenreAndCategory(admin.ModelAdmin):
    """Заготовка для админок Жанры и Категории."""

    list_display = (
        'name',
        'slug',
    )
    list_display_links = (
        'name',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Переопределяем настройки интерфейса админки раздела Пользователь."""

    list_display = (
        'username',
        'role',
        'email',
        'confirmation_code',
    )
    list_display_links = (
        'username',
    )
    search_fields = (
        'username',
    )
    list_filter = (
        'role',
    )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Переопределяем настройки интерфейса админки раздела Произведения."""

    list_display = (
        'name',
        'description',
        'category',
        'year',
    )
    list_display_links = (
        'name',
    )
    search_fields = (
        'name',
        'description',
    )
    list_filter = (
        'category',
        'year',
    )


@admin.register(Genre)
class GenreAdmin(GenreAndCategory):
    """Переопределяем настройки интерфейса админки раздела Жанры."""


@admin.register(Category)
class CategoryAdmin(GenreAndCategory):
    """Переопределяем настройки интерфейса админки раздела категории."""



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Переопределяем настройки интерфейса админки раздела Отзывы."""

    list_display = (
        'text',
        'author',
        'title',
        'score',
        'pub_date',
    )
    list_display_links = (
        'text',
    )
    search_fields = (
        'text',
        'author__username',
    )
    list_filter = (
        'author__username',
        'pub_date',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Переопределяем настройки интерфейса админки раздела Комментарии."""

    list_display = (
        'text',
        'author',
        'review',
        'pub_date',
    )
    list_display_links = (
        'text',
    )
    search_fields = (
        'text',
        'author__username',
    )
    list_filter = (
        'author__username',
        'pub_date',
    )