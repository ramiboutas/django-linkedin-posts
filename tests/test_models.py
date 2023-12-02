from django.test import TestCase

from django_linkedin_posts.models import (
    Post,
    PostImage,
    Poll,
    PollOption,
    Comment,
    CommentImage,
)


class PostTests(TestCase):
    def test_share_and_delete_text_post(self):
        p = Post.objects.create(
            text="Hello friends, this is just a test from my Python package django-linkedin-posts"
        )
        p.share()
        self.assertEqual(201, p.response_code)

        p.linkedin_delete()
        self.assertEqual(204, p.response_code)


class PollTests(TestCase):
    def test_share_and_delete_poll(self):
        # Poll create in the db
        p = Poll.objects.create(
            question_text="Do you like this package?",
            comment_text="Check out this poll!",
        )
        PollOption.objects.create(poll=p, text="No")
        PollOption.objects.create(poll=p, text="Yes")

        # Poll share
        p.share()
        self.assertEqual(201, p.response_code)

        ## Create comment to poll
        c = Comment.objects.create(
            poll=p, text="I do not want to respond to this poll, just to comment here!"
        )
        c.share()

        self.assertEqual(201, c.response_code)

        # Poll delete
        p.linkedin_delete()
        self.assertEqual(204, p.response_code)
