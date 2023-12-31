# Generated by Django 4.2.7 on 2023-11-29 16:39

from django.db import migrations, models
import django.db.models.deletion
import django_linkedin_posts.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "urn",
                    models.CharField(
                        blank=True, editable=False, max_length=64, null=True
                    ),
                ),
                (
                    "response_code",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="Response code",
                    ),
                ),
                (
                    "response_text",
                    models.TextField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="Response text",
                    ),
                ),
                (
                    "text",
                    models.TextField(blank=True, default="Comment text", null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Poll",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "urn",
                    models.CharField(
                        blank=True, editable=False, max_length=64, null=True
                    ),
                ),
                (
                    "response_code",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="Response code",
                    ),
                ),
                (
                    "response_text",
                    models.TextField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="Response text",
                    ),
                ),
                ("comment", models.CharField(default="", max_length=140)),
                ("question_text", models.CharField(max_length=140)),
                (
                    "duration",
                    models.CharField(
                        choices=[
                            ("ONE_DAY", "Poll is open for 1 day"),
                            ("THREE_DAYS", "Poll is open for 3 days"),
                            ("SEVEN_DAYS", "Poll is open for 7 days"),
                            ("FOURTEEN_DAYS", "Poll is open for 14 days"),
                        ],
                        default="THREE_DAYS",
                        max_length=32,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "urn",
                    models.CharField(
                        blank=True, editable=False, max_length=64, null=True
                    ),
                ),
                (
                    "response_code",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="Response code",
                    ),
                ),
                (
                    "response_text",
                    models.TextField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="Response text",
                    ),
                ),
                ("text", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="PostImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "urn",
                    models.CharField(
                        blank=True, editable=False, max_length=64, null=True
                    ),
                ),
                (
                    "response_code",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="Response code",
                    ),
                ),
                (
                    "response_text",
                    models.TextField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="Response text",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True, default="Image title", max_length=64, null=True
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=django_linkedin_posts.models.image_path,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_linkedin_posts.post",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PollOption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=30)),
                (
                    "poll",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_linkedin_posts.poll",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CommentImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "urn",
                    models.CharField(
                        blank=True, editable=False, max_length=64, null=True
                    ),
                ),
                (
                    "response_code",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="Response code",
                    ),
                ),
                (
                    "response_text",
                    models.TextField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="Response text",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=django_linkedin_posts.models.comment_image_path,
                    ),
                ),
                (
                    "comment",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_linkedin_posts.comment",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="django_linkedin_posts.post",
            ),
        ),
    ]
