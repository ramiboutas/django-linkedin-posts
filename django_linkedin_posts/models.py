from django.db import models
from django.utils import timezone
from django.conf import settings

from django.utils.translation import gettext_lazy as _

from linkedin_posts.posts import share_post
from linkedin_posts.posts import share_post_with_media
from linkedin_posts.images import upload_image


def _get_image_upload_path(instance, filename):
    now = timezone.now()
    return "linkedin-posts/%s/%s/%s/%s", (now.year, now.month, now.day, filename)


class Post(models.Model):
    comment = models.TextField()

    post_urn = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        editable=False,
    )

    image = models.ImageField(
        upload_to=_get_image_upload_path,
        null=True,
        blank=True,
    )

    image_title = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    image_urn = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        editable=False,
    )
    image_code = models.PositiveSmallIntegerField(
        _("Response code when uploading image"),
        null=True,
        blank=True,
        editable=False,
    )
    post_code = models.PositiveSmallIntegerField(
        _("Response code when posting"), null=True, blank=True, editable=False
    )

    def upload_image(self):
        if self.image is None:
            return self

        response, image_urn = upload_image(
            settings.LINKEDIN_ACCESS_TOKEN,
            author_id=settings.LINKEDIN_AUTHOR_ID,
            author_type=settings.LINKEDIN_AUTHOR_TPYE,
            file=self.image.read(),
        )
        self.image_urn = image_urn
        self.image_code = response.code
        self.save()
        return self

    def share(self):
        if self.image_urn:
            response = share_post_with_media(
                settings.LINKEDIN_ACCESS_TOKEN,
                author_id=settings.LINKEDIN_AUTHOR_ID,
                author_type=settings.LINKEDIN_AUTHOR_TPYE,
                comment=self.comment,
                media_id=self.image_urn,
            )

        else:
            response = share_post(
                settings.LINKEDIN_ACCESS_TOKEN,
                author_id=settings.LINKEDIN_AUTHOR_ID,
                author_type=settings.LINKEDIN_AUTHOR_TPYE,
                comment=self.comment,
            )
        self.post_urn = response.getheader("x-restli-id")
        self.post_code = response.code
        self.save()
        return self


class PostShare(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    share = models.BooleanField(default=False)
    upload_image = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.upload_image:
            self = self.upload_image()
        if self.share:
            self.post.share()
        super(PostShare, self).save(*args, **kwargs)
