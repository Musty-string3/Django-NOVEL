from django.db import models
from accounts.models import CustomUser

class Novel(models.Model):
    """小説モデル"""
    title = models.CharField(verbose_name="タイトル", max_length=50, null=False, blank=False)
    created_by = models.ForeignKey(CustomUser, verbose_name="作成者", on_delete=models.CASCADE, null=False, blank=False)
    is_public = models.BooleanField(verbose_name='公開・非公開', default=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta():
        verbose_name_plural = "小説"
        db_table = 'novel'

    def __str__(self):
        return self.title