from django.contrib import admin
from .models import *

# # Register your models here.


class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in ForumCategory._meta.get_fields() if field.concrete
    ]


admin.site.register(ForumCategory, ForumCategoryAdmin)


class ForumAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Forum._meta.get_fields() if field.concrete]
    list_display.append("likes")

    def likes(self, obj):
        return ForumLike.objects.filter(forum=obj).count()


admin.site.register(Forum, ForumAdmin)


class ForumLikeAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in ForumLike._meta.get_fields() if field.concrete
    ]


admin.site.register(ForumLike, ForumLikeAdmin)


class ForumReplyAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in ForumReply._meta.get_fields() if field.concrete
    ]


admin.site.register(ForumReply, ForumReplyAdmin)

# @admin.register(Forum)
# class ForumAdmin(admin.ModelAdmin):

#     # def date_kor(self, obj):
#     #     return obj.reg_date.strftime("%Y-%m-%d %H:%M")
#     # date_kor.admin_order_field = 'reg_date'
#     # date_kor.short_description = '등록일시'

#     # list_display = ('__str__', 'room', 'school', 'teacher', 'date_kor')
#     # list_filter = ('school',)
#     # search_fields = ['school__name']
#     fields = ['uid', 'category', 'title', 'text', 'is_show']

# @admin.register(Reply)
# class ReplyAdmin(admin.ModelAdmin):
#     fields = ['uid', 'forum', 'commnet', 'is_show']


# admin.site.register(Forum)
# admin.site.register(Forum, ForumAdmin)
# admin.site.register(Reply)
# admin.site.register(Reply, ReplyAdmin)
