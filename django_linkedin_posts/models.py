from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from linkedin_posts.posts import share_post, delete_post
from linkedin_posts.images import upload_image
from linkedin_posts.polls import share_poll
from linkedin_posts.comments import comment_in_a_post

from .exceptions import PollOptionsError


def image_path(obj, filename):
    n = timezone.now()
    return f"linkedin-posts/{n.year}/{n.month}/{n.day}/{obj.id}/{filename}"


def comment_image_path(obj, filename):
    n = timezone.now()
    return f"linkedin-posts/{n.year}/{n.month}/{n.day}/{obj.post.id}/comment_{obj.id}/{filename}"


LINKEDIN_SECRETS = {
    "access_token": settings.LINKEDIN_ACCESS_TOKEN,
    "author_id": settings.LINKEDIN_AUTHOR_ID,
    "author_type": settings.LINKEDIN_AUTHOR_TPYE,
}


class AbstractLinkedinObject(models.Model):
    created_at = models.DateTimeField(("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(("updated_at"), auto_now=True)
    urn = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        editable=False,
    )

    response_code = models.PositiveSmallIntegerField(
        _("Response code"),
        null=True,
        blank=True,
        editable=False,
    )

    response_text = models.TextField(
        _("Response text"),
        null=True,
        blank=True,
        editable=False,
    )

    def linkedin_delete(self):
        r = delete_post(settings.LINKEDIN_ACCESS_TOKEN, self.urn)
        save_response_in_object(r, self)

    class Meta:
        abstract = True


def save_response_in_object(response, obj, urn=None):
    try:
        obj.urn = response.headers["x-restli-id"]
    except KeyError:
        pass

    if urn:
        obj.urn = urn
    obj.response_code = response.status_code
    obj.response_text = response.text
    obj.save()
    return obj


class Post(AbstractLinkedinObject):
    text = models.TextField()

    def build_content(self):
        images = self.postimage_set.exclude(urn__isnull=True)

        if len(images) == 1:
            return {"media": {"title": images[0].title, "id": images[0].urn}}
        elif len(images) > 1:
            multi = [{"id": i.urn, "altText": i.title} for i in images]
            return {"multiImage": {"images": multi}}

    def share(
        self,
        visibility: str = "PUBLIC",
        feed_distribution: str = "MAIN_FEED",
        container: str | dict = None,
    ):
        response = share_post(
            **LINKEDIN_SECRETS,
            comment=self.text,
            feed_distribution=feed_distribution,
            container=container,
            content=self.build_content(),
            visibility=visibility,
        )

        save_response_in_object(response, self)

    def upload_images_and_share(self):
        images = self.postimage_set.all()
        for image in images:
            image.upload()
        self.share()

    def __str__(self):
        return self.text


class PostImage(AbstractLinkedinObject):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        default=_("Image title"),
    )

    image = models.ImageField(
        upload_to=image_path,
        null=True,
        blank=True,
    )

    def upload(self):
        response, urn = upload_image(**LINKEDIN_SECRETS, file=self.image.read())
        save_response_in_object(response, self, urn=urn)

    def __str__(self):
        return self.title


class Poll(AbstractLinkedinObject):
    DURATIONS = (
        ("ONE_DAY", _("Poll is open for 1 day")),
        ("THREE_DAYS", _("Poll is open for 3 days")),
        ("SEVEN_DAYS", _("Poll is open for 7 days")),
        ("FOURTEEN_DAYS", _("Poll is open for 14 days")),
    )

    VOTING_TYPES = (
        ("SINGLE_VOTE", _("Single-select vote.")),
        ("MULTIPLE_VOTE", _("Multiple-select vote (To be supported later in future)")),
    )

    comment_text = models.TextField(max_length=140, default="")
    question_text = models.TextField(max_length=140)
    duration = models.CharField(max_length=32, choices=DURATIONS, default="THREE_DAYS")

    @cached_property
    def option_list(self):
        return [o.text for o in self.polloption_set.all()]

    @cached_property
    def option_count(self):
        return len(self.option_list)

    def share(
        self,
        visibility: str = "PUBLIC",
        feed_distribution: str = "MAIN_FEED",
        container: str | dict = None,
    ):
        # check if poll has options (min 2, max 4)
        if self.option_count < 2 or self.option_count > 4:
            raise PollOptionsError

        response = share_poll(
            **LINKEDIN_SECRETS,
            options=self.option_list,
            question=self.question_text,
            comment=self.comment_text,
            visibility=visibility,
            feed_distribution=feed_distribution,
            container=container,
        )

        save_response_in_object(response, self)

    def __str__(self):
        return self.question_text


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=30)

    def __str__(self):
        return self.text


class Comment(AbstractLinkedinObject):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True)

    def share(self):
        if self.post is not None:
            r_post = comment_in_a_post(
                **LINKEDIN_SECRETS,
                post_urn=self.post.urn,
                message_text=self.text,
                content=self.build_content(),
            )
            save_response_in_object(r_post, self)
            return
        if self.poll is not None:
            r_poll = comment_in_a_post(
                **LINKEDIN_SECRETS,
                post_urn=self.poll.urn,
                message_text=self.text,
                content=self.build_content(),
            )
            save_response_in_object(r_poll, self)

    def build_content(self):
        try:
            return ([{"entity": {"image": self.commentimage.urn}}],)
        except Exception:
            pass

    def upload_image_and_share(self):
        self.commentimage.upload()
        self.share()

    def __str__(self):
        return self.text


class CommentImage(AbstractLinkedinObject):
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=comment_image_path, null=True)

    def upload(self):
        response, urn = upload_image(**LINKEDIN_SECRETS, file=self.image.read())
        save_response_in_object(response, self, urn=urn)

    def __str__(self):
        return f"Image ({str(self.comment)})"


def create_poll_with_options(
    comment: str,
    question: str,
    options: list,
    duration: str = "THREE_DAYS",
):
    p = Poll.objects.create(
        comment_text=comment,
        question_text=question,
        duration=duration,
    )

    for option in options:
        PollOption.objects.create(poll=p, text=option)

    return p
