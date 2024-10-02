from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

from collections import namedtuple

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
    pass

class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг произведения'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.OneToOneField(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'



class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
