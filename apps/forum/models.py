from django.db import models


class ForumCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Forum(models.Model):
    user = models.CharField(max_length=100)
    category = models.ForeignKey(
        ForumCategory, to_field="name", on_delete=models.PROTECT
    )
    title = models.CharField(max_length=80)
    text = models.TextField()
    views = models.IntegerField(default=0)
    is_show = models.BooleanField(default=True)
    is_notice = models.BooleanField(default=False)
    reg_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["reg_date"]
        # db_table = 'forum_items'

    def __str__(self):
        return self.title


class ForumLike(models.Model):
    forum = models.ForeignKey(
        Forum, on_delete=models.CASCADE, related_name="likes")
    user = models.CharField(max_length=100)


class ForumReply(models.Model):
    user = models.CharField(max_length=100)
    forum = models.ForeignKey(
        Forum, on_delete=models.CASCADE, related_name="reply")
    comment = models.TextField()
    is_show = models.BooleanField(default=True)
    reg_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # db_table = 'forum_reply'
        verbose_name_plural = "replies"
        ordering = ["reg_date"]

    def __str__(self):
        return f"{self.comment[:20]} > {self.forum}"
