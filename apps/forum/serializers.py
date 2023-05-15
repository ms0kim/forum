from rest_framework import serializers
from .models import *


class FilteredReplySerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(is_show=True)
        return super(FilteredReplySerializer, self).to_representation(data)


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilteredReplySerializer
        model = ForumReply
        fields = ["id", "user", "comment", "forum", "reg_date"]


class ForumLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumLike
        fields = ["id", "user", "forum"]


class ForumCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumCategory
        fields = ["id", "name"]


class ForumSerializer(serializers.ModelSerializer):
    reply = ReplySerializer(many=True, read_only=True)
    category = ForumCategorySerializer(read_only=True)
    likes_count = serializers.IntegerField(
        source="likes.count", read_only=True)
    # likes_count = serializers.SerializerMethodField()
    # likes = serializers.SerializerMethodField()

    class Meta:
        model = Forum
        fields = [
            "id",
            "user",
            "category",
            "title",
            "text",
            "views",
            "likes_count",
            "is_notice",
            "reg_date",
            "reply",
        ]
        read_only_fields = [
            "reply",
            # "likes",
            "views",
            "reg_date",
        ]
        depth = 1

    # def likes_count(self, obj) :
    #     return obj.likes.count()


class ForumListSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(
        source="likes.count", read_only=True)

    class Meta:
        model = Forum
        fields = [
            "id",
            "user",
            "category",
            "title",
            "views",
            # "likes",
            "likes_count",
            "is_notice",
            "reg_date",
        ]
        depth = 1
