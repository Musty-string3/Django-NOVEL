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


class Character(models.Model):
    """キャラクターモデル"""
    name = models.CharField(verbose_name='名前', max_length=50, null=False, blank=False)
    icon = models.ImageField(verbose_name='アイコン', upload_to='images/%Y/%m/%d/') # 保存先はMEDIA_ROOT直下
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta():
        verbose_name_plural = 'キャラクター'
        db_table = 'character'

    def __str__(self):
        return self.name

class Sentence(models.Model):
    """文章モデル"""
    text = models.CharField(verbose_name='文章', max_length=255, null=False, blank=False)
    speaker = models.ManyToManyField(Character, verbose_name='発言者', blank=False)
    novel = models.ForeignKey(Novel, verbose_name='小説', on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta():
        verbose_name_plural = '文章'
        db_table = 'sentence'

    def __str__(self):
        return self.text