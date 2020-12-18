from django.contrib import admin
from apps.comments.models import *


class CommentReplyInline(admin.TabularInline):
    model = CommentReply
    extra = 0

class CommentImagesInline(admin.TabularInline):
    model = CommentImages
    extra = 0

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentReplyInline, CommentImagesInline]
    list_display = ['product', 'text', 'created']
    

class QuestionReplyInline(admin.TabularInline):
    model = QuestionReply
    extra = 0

@admin.register(Question)
class CommentAdmin(admin.ModelAdmin):
    inlines = [QuestionReplyInline]