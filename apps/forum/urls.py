from django.urls import path
from .views import *

urlpatterns = [
    path("v1/forum/category/", forumCategoryView),
    path("v1/forum/all/", ForumListView.as_view()),
    path("v1/forum/", ForumWriteView.as_view()),  # category, title, text / fid
    path("v1/forum/reply/", ForumCommentView.as_view()),  # fid, comment
    path("v1/forum/like/", ForumLikeView.as_view()),  # fid
    path("v1/forum/detail/<slug:fid>/", ForumDetailView.as_view()),
]
