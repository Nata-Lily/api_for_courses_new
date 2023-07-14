from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=150,
        null=True
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=USER
    )

    class Meta:
        ordering = ('username',)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username[:15]

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_user(self):
        return self.role == User.USER


class Course(models.Model):
    name = models.CharField(max_length=255, blank=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(max_length=500)

    class Meta:
        ordering = ['start_date']
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self) -> str:
        return self.name[:15]


class Participant(models.Model):
    course_name = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='course_name',
        verbose_name='название_курса')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='записавшийся'
    )
    send_notification = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.course_name}, {self.user}'
