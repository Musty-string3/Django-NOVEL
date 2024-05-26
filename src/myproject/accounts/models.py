from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name='メールアドレス', max_length=50, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta():
        verbose_name_plural = 'ユーザー'
        db_table = 'user'

    def __str__(self):
        return self.username