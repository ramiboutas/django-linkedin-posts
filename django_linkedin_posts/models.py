from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from linkedin_posts.posts import share_post
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


class BaseLinkedinObject(object):
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

    def save_response_in_object(self, response, urn=None):
        try:
            self.urn = response.headers["x-restli-id"]
        except KeyError:
            pass

        if urn:
            self.urn = urn
        self.response_code = response.status_code
        self.response_text = response.text
        self.save()
        return self

    def share(
        self,
        visibility: str = "PUBLIC",
        feed_distribution: str = "MAIN_FEED",
        container: str | dict = None,
    ):
        response = None

        # Poll object
        if self._meta.model_name == "poll":
            # check if poll has options (min 2, max 4)
            if self.option_count < 2 or self.option_count > 4:
                raise PollOptionsError

            response = share_poll(
                settings.LINKEDIN_ACCESS_TOKEN,
                author_id=settings.LINKEDIN_AUTHOR_ID,
                author_type=settings.LINKEDIN_AUTHOR_TPYE,
                options=self.option_list,
                visibility=visibility,
                feed_distribution=feed_distribution,
                container=container,
            )
        elif self._meta.model_name == "post":
            response = share_post(
                settings.LINKEDIN_ACCESS_TOKEN,
                author_id=settings.LINKEDIN_AUTHOR_ID,
                author_type=settings.LINKEDIN_AUTHOR_TPYE,
                comment=self.text,
                feed_distribution=feed_distribution,
                container=container,
                content=self.build_content(),
                visibility=visibility,
            )
        elif self._meta.model_name == "postcomment":
            response = comment_in_a_post(
                settings.LINKEDIN_ACCESS_TOKEN,
                author_id=settings.LINKEDIN_AUTHOR_ID,
                author_type=settings.LINKEDIN_AUTHOR_TPYE,
                post_urn=self.post.urn,
                message_text=self.text,
                content=self.build_content(),
            )

        self.save_response_in_object(response)

    def upload(self):
        response, urn = upload_image(
            settings.LINKEDIN_ACCESS_TOKEN,
            author_id=settings.LINKEDIN_AUTHOR_ID,
            author_type=settings.LINKEDIN_AUTHOR_TPYE,
            file=self.image.read(),
        )
        return self.save_response_in_object(response, urn=urn)


class Post(models.Model, BaseLinkedinObject):
    text = models.TextField()

    def build_content(self):
        images = self.post_image_set.exclude(urn__isnull=True)

        if len(images) == 1:
            return {"media": {"title": images[0].title, "id": images[0].urn}}
        elif len(images) > 1:
            multi = [{"id": i.urn, "altText": i.title} for i in images]
            return {"multiImage": {"images": multi}}

    @cached_property
    def url(self):
        if self.urn:
            return f"https://www.linkedin.com/feed/update/{self.urn}/"


class PostImage(models.Model, BaseLinkedinObject):
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


class Comment(models.Model, BaseLinkedinObject):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )

    text = models.TextField(
        null=True,
        blank=True,
        default=_("Comment text"),
    )

    def build_content(self):
        if self.commentimage is not None:
            return ([{"entity": {"image": self.commentimage.urn}}],)


class CommentImage(models.Model, BaseLinkedinObject):
    comment = models.OneToOneField(
        Comment,
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        upload_to=comment_image_path,
        null=True,
        blank=True,
    )


class Poll(models.Model, BaseLinkedinObject):
    POLL_DURATIONS = (
        ("ONE_DAY", _("Poll is open for 1 day")),
        ("THREE_DAYS", _("Poll is open for 3 days")),
        ("SEVEN_DAYS", _("Poll is open for 7 days")),
        ("FOURTEEN_DAYS", _("Poll is open for 14 days")),
    )

    SELECTION_TYPE = (
        ("SINGLE_VOTE", _("Single-select vote.")),
        ("MULTIPLE_VOTE", _("Multiple-select vote (To be supported later in future)")),
    )

    comment = models.CharField(max_length=140, default="")
    question_text = models.CharField(max_length=140)
    duration = models.CharField(
        max_length=32,
        choices=POLL_DURATIONS,
        default="THREE_DAYS",
    )

    @cached_property
    def option_list(self):
        return [o.text for o in self.poll_option_set.all()]

    @cached_property
    def option_count(self):
        return len(self.option_list)


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=30)
