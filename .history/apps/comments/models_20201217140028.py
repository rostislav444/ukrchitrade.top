from django.db import models
from apps.core.models.models__images import Image
from django.utils import timezone
from apps.catalogue.models import Product


# COMMENTS
class Comment(models.Model):
    product =     models.ForeignKey('catalogue.Product', on_delete=models.CASCADE, related_name='comments', verbose_name="Продукт")
    user =        models.ForeignKey('user.CustomUser', blank=False, on_delete=models.CASCADE, related_name='comments', verbose_name="Пользователь")
    # order =       models.ForeignKey('order.Order', blank=True, null=True, on_delete=models.SET_NULL, related_name='comments')
    rate =        models.PositiveIntegerField(blank=False, default=5, verbose_name="Оценка")
    text =        models.TextField(blank=True, null=True)
    advantages =   models.TextField(blank=True, null=True)
    disadvantages =  models.TextField(blank=True, null=True)
    created =     models.DateTimeField(default=timezone.now, verbose_name="Время")
    plus =        models.PositiveIntegerField(blank=True, default=0)
    minus =       models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        rate = {
            1 : '*....',
            2 : '**...',
            3 : '***..',
            4 : '****.',
            5 : '*****',
        }
        return str(self.product.name) + ' ' + rate[self.rate] + ' - ' + self.created.strftime("%H:%M  %a %d.%m.%Y")

    class Meta:
        ordering = ['-created']
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'


class CommentLike(models.Model):
    like =     models.BooleanField(default=True)
    parent =   models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user =     models.ForeignKey('user.CustomUser', blank=False, on_delete=models.CASCADE, related_name='likes')

    def save(self):
        super(CommentLike, self).save()
        Comment.objects.filter(pk=self.parent.pk).update(
            plus =  len(CommentLike.objects.filter(parent=self.parent, like=True)),
            minus = len(CommentLike.objects.filter(parent=self.parent, like=False)),
        )


class CommentImages(Image):
    parent =  models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Фото комментария'
        verbose_name_plural = 'Фотографии комментариев'


class CommentReply(models.Model):
    parent =  models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replys')
    user =    models.ForeignKey('user.CustomUser', blank=False, on_delete=models.CASCADE, related_name='comments_replys')
    # order =   models.ForeignKey('order.Order', blank=True, null=True, on_delete=models.SET_NULL, related_name='comments_replys')
    text =    models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now, verbose_name="Время")

    class Meta:
        ordering = ['-created']
        verbose_name = 'Ответы на комментарии'
        verbose_name_plural = 'Ответы на комментарии'


# QUESTIONS
class Question(models.Model):
    product = models.ForeignKey('catalogue.Product', on_delete=models.CASCADE, related_name='questions')
    user =    models.ForeignKey('user.CustomUser', blank=False, on_delete=models.CASCADE, related_name='questions')
    # order =   models.ForeignKey('order.Order', blank=True, null=True, on_delete=models.SET_NULL, related_name='questions')
    text =    models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now, verbose_name="Время")

    def __str__(self):

        return str(self.product.name) + ' ' + self.created.strftime("%H:%M  %a %d.%m.%Y")

    class Meta:
        ordering = ['-created']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class QuestionReply(models.Model):
    parent =  models.ForeignKey(Question, on_delete=models.CASCADE, related_name='replys')
    user =    models.ForeignKey('user.CustomUser', blank=False, on_delete=models.CASCADE, related_name='questions_replys')
    # order =   models.ForeignKey('order.Order', blank=True, null=True, on_delete=models.SET_NULL, related_name='questions_replys')
    text =    models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now, verbose_name="Время")

    class Meta:
        ordering = ['-created']
       



  

