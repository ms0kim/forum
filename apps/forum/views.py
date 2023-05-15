import json
import datetime
import logging
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import *
from .serializers import *

from gdfutil.kcloak import userInfoByToken


logger = logging.getLogger("django")


@api_view(["GET"])
def forumCategoryView(request):
    category = ForumCategory.objects.all()
    serializer = ForumCategorySerializer(category, many=True)
    return Response(serializer.data)


class ForumListView(APIView):
    def get(self, request):
        forums = Forum.objects.filter(is_show=True).order_by("-reg_date")
        serializer = ForumListSerializer(forums, many=True)
        resp = serializer.data
        return Response(resp)


class ForumDetailView(APIView):
    def get_forum(self, fid):
        try:
            return Forum.objects.get(id=fid, is_show=True)
        except Exception as e:
            logger.error(e)
            print(e)
            raise Http404()

    def add_view_count(self, forum):
        forum.views += 1
        forum.save()

    # Load Specific Forum
    def get(self, request, fid):
        headers = request.headers
        auth = headers.get("Authorization")
        forum = self.get_forum(fid)
        have_liked = 0
        if not forum.is_show:
            logger.error("This Forum Cannot Be Shown")
            raise Http404()
        serializer = ForumSerializer(forum)
        self.add_view_count(forum)
        resp = serializer.data

        likes = ForumLike.objects.filter(forum=forum)
        # resp['likes']=likes.count()
        if auth:
            user = userInfoByToken(headers.get("Authorization"))
            have_liked = likes.filter(user=user.get('sub')).count()
        resp["have_liked"] = bool(have_liked)
        return Response(resp)


class ForumWriteView(APIView):
    def get_category(self, category):
        try:
            return ForumCategory.objects.get(id=category)
        except:
            try:
                return ForumCategory.objects.get(name=category)
            except Exception as e:
                self.logger.error(e)
                raise Http404()

    # User 정보 불러오기
    def get_user(self, token):
        userinfo = userInfoByToken(token)
        return userinfo.get("sub")

    def get_forum(self, fid, user):
        try:
            return Forum.objects.get(id=fid, user=user)
        except Exception as e:
            logger.error(e)
            raise Http404()

    # Forum Write
    def post(self, request):
        """
        "category",
        "title",
        "text",
        """
        data = request.data
        headers = request.headers
        category = self.get_category(data.get("category"))
        user = self.get_user(headers.get("Authorization"))
        serializer = ForumSerializer(data=data)
        if serializer.is_valid():
            serializer.save(category=category, user=user)
            return Response({"status": "success"})
        else:
            err = serializer.errors
            print(err)
            return Response({"status": "errors"})

    def delete(self, request):
        """
        fid
        """
        data = request.data
        fid = data.get("fid")
        headers = request.headers
        user = self.get_user(headers.get("Authorization"))
        forum = self.get_forum(fid, user)
        forum.is_show = False
        forum.save()
        return Response({"status": "success"})


class ForumCommentView(APIView):
    # User 정보 불러오기
    def get_user(self, token):
        userinfo = userInfoByToken(token)
        return userinfo.get("sub")

    def get_forum(self, fid):
        try:
            return Forum.objects.get(id=fid)
        except Exception as e:
            logger.error(e)
            raise Http404()

    def get_replies(self, forum):
        try:
            return ForumReply.objects.filter(forum=forum)
        except Exception as e:
            logger.error(e)
            raise Http404()

    def save(self, comment, user, forum):
        serializer = ReplySerializer(
            data={"comment": comment, "forum": forum.id})
        if serializer.is_valid():
            return serializer.save(user=user)
        print(serializer.errors)

    def get(self, request):
        params = request.GET
        fid = params.get("fid")
        forum = self.get_forum(fid)
        replies = self.get_replies(forum)
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        "fid",
        "comment"
        """
        data = request.data
        headers = request.headers
        user = self.get_user(headers.get("Authorization"))
        fid = data.get("fid")
        comment = data.get("comment")
        forum = self.get_forum(fid)
        self.save(comment, user, forum)
        replies = self.get_replies(forum)
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)


class ForumLikeView(APIView):
    def get_forum(self, data):
        try:
            return Forum.objects.get(id=data.get("fid"))
        except Exception as e:
            logger.error(e)
            raise e

    def check_liked(self, forum, user):
        return ForumLike.objects.get_or_create(forum=forum, user=user)

    def get_likes(self, forum):
        return ForumLike.objects.filter(forum=forum).count()

    def post(self, request):
        headers = request.headers
        data = request.data
        user = self.get_user(headers.get("Authorization"))
        forum = self.get_forum(data)
        self.check_liked(forum, user)
        return Response(
            {"likes": self.get_likes(
                forum), "have_liked": bool(forum is not None)}
        )
